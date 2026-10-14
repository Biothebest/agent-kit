"""Behavior tests for the agent-kit CLI. Run: python3 -m unittest discover tests"""

import contextlib
import importlib.machinery
import importlib.util
import io
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]
loader = importlib.machinery.SourceFileLoader("agent_kit", str(KIT / "agent-kit"))
spec = importlib.util.spec_from_loader("agent_kit", loader)
kit = importlib.util.module_from_spec(spec)
loader.exec_module(kit)


def write_skill(root: Path, name: str, extra: str = "") -> Path:
    directory = root / name
    directory.mkdir(parents=True)
    (directory / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: Test skill {name}.\n{extra}---\nbody\n", encoding="utf-8"
    )
    return directory


class Sandbox(unittest.TestCase):
    """Isolated HOME and a disposable skill library for every test."""

    def setUp(self):
        self.temp = Path(tempfile.mkdtemp())
        self.home = self.temp / "home"
        self.home.mkdir()
        self.skills = self.temp / "kit" / "skills"
        self.skills.mkdir(parents=True)
        self.saved = (os.environ.get("HOME"), os.environ.get("PI_CONFIG_DIR"), kit.SKILLS)
        os.environ["HOME"] = str(self.home)
        os.environ.pop("PI_CONFIG_DIR", None)
        kit.SKILLS = self.skills

    def tearDown(self):
        home, config, skills = self.saved
        os.environ["HOME"] = home
        if config is not None:
            os.environ["PI_CONFIG_DIR"] = config
        kit.SKILLS = skills
        shutil.rmtree(self.temp)

    def run_kit(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            code = kit.main(list(argv))
        return code, out.getvalue()


class LinkTests(Sandbox):
    def test_link_exposes_every_skill_to_every_harness_and_is_idempotent(self):
        alpha = write_skill(self.skills, "alpha")
        write_skill(self.skills, "beta")
        code, _ = self.run_kit("link")
        self.assertEqual(code, 0)
        for relative in (".agents/skills", ".claude/skills"):
            entry = self.home / relative / "alpha"
            self.assertTrue(entry.is_symlink())
            self.assertEqual(entry.resolve(), alpha.resolve())
            self.assertTrue((self.home / relative / "beta" / "SKILL.md").is_file())
        code, output = self.run_kit("link")
        self.assertEqual(code, 0)
        self.assertNotIn("linked     ", output)
        self.assertEqual(output.count("unchanged"), 4)

    def test_link_never_replaces_a_foreign_skill(self):
        write_skill(self.skills, "alpha")
        foreign = write_skill(self.home / ".agents" / "skills", "alpha")
        code, output = self.run_kit("link", "--harness", "agents")
        self.assertEqual(code, 1)
        self.assertIn("CONFLICT", output)
        self.assertFalse(foreign.is_symlink())
        self.assertIn("Test skill alpha", (foreign / "SKILL.md").read_text())

    def test_link_repairs_kit_links_and_prunes_removed_kit_skills(self):
        write_skill(self.skills, "alpha")
        write_skill(self.skills, "beta")
        gone = write_skill(self.skills, "gone")
        self.run_kit("link", "--harness", "agents")
        shutil.rmtree(gone)
        root = self.home / ".agents" / "skills"
        (root / "alpha").unlink()
        (root / "alpha").symlink_to(self.skills / "beta")  # kit link aimed at the wrong skill
        code, output = self.run_kit("link", "--harness", "agents")
        self.assertEqual(code, 0)
        self.assertEqual((root / "alpha").resolve(), (self.skills / "alpha").resolve())
        self.assertFalse((root / "gone").is_symlink())
        self.assertIn("relinked", output)
        self.assertIn("pruned", output)

    def test_link_keeps_a_foreign_dangling_symlink(self):
        write_skill(self.skills, "alpha")
        root = self.home / ".agents" / "skills"
        root.mkdir(parents=True)
        foreign = self.temp / "unmounted" / "alpha"
        (root / "alpha").symlink_to(foreign)
        code, output = self.run_kit("link", "--harness", "agents")
        self.assertEqual(code, 1)
        self.assertIn("CONFLICT", output)
        self.assertEqual(Path(os.readlink(root / "alpha")), foreign)

    def test_invalid_skill_blocks_linking_entirely(self):
        write_skill(self.skills, "alpha")
        write_skill(self.skills, "beta", extra="bundle: private\n")
        code, output = self.run_kit("link")
        self.assertEqual(code, 2)
        self.assertIn("non-spec frontmatter keys: bundle", output)
        self.assertFalse((self.home / ".agents" / "skills" / "alpha").exists())

    def test_unlink_removes_only_kit_links(self):
        write_skill(self.skills, "alpha")
        self.run_kit("link")
        other = self.temp / "other-skill"
        other.mkdir()
        (self.home / ".claude" / "skills" / "mine").symlink_to(other)
        code, _ = self.run_kit("unlink")
        self.assertEqual(code, 0)
        self.assertFalse((self.home / ".agents" / "skills" / "alpha").is_symlink())
        self.assertFalse((self.home / ".claude" / "skills" / "alpha").is_symlink())
        self.assertTrue((self.home / ".claude" / "skills" / "mine").is_symlink())


class ValidationTests(Sandbox):
    def test_spec_violations_are_reported(self):
        cases = {
            "Upper": ("---\nname: Upper\ndescription: x\n---\n", "name must be 1-64"),
            "mismatch": ("---\nname: other\ndescription: x\n---\n", "does not match directory"),
            "long": ("---\nname: long\ndescription: " + "x" * 1025 + "\n---\n", "description must be 1-1024"),
        }
        for name, (text, message) in cases.items():
            (self.skills / name).mkdir()
            (self.skills / name / "SKILL.md").write_text(text)
            errors = kit.validate_skill(self.skills / name)
            self.assertTrue(any(message in error for error in errors), (name, errors))

    def test_quoted_and_nested_frontmatter_parses(self):
        skill = self.skills / "alpha"
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            '---\nname: alpha\ndescription: "Say \\"hi\\": now"\nmetadata:\n  source: x\n---\n'
        )
        self.assertEqual(kit.validate_skill(skill), [])
        meta = kit.frontmatter((skill / "SKILL.md").read_text())
        self.assertEqual(meta["description"], 'Say "hi": now')
        self.assertEqual(meta["metadata"], {"source": "x"})

    def test_every_shipped_skill_meets_the_spec(self):
        for name, path in {p.name: p for p in (KIT / "skills").iterdir() if p.is_dir()}.items():
            self.assertEqual(kit.validate_skill(path), [], name)


class ProfileTests(Sandbox):
    def test_init_writes_baseline_without_overwriting_existing_settings(self):
        agent = self.home / ".omp" / "profiles" / "work" / "agent"
        agent.mkdir(parents=True)
        (agent / "config.yml").write_text("theme: mine\n")
        code, output = self.run_kit("profile", "init", "work")
        self.assertEqual(code, 0)
        self.assertEqual((agent / "config.yml").read_text(), "theme: mine\n")
        self.assertIn("kept", output)
        for name in ("models.yml", "lsp.json"):
            self.assertEqual(
                (agent / name).read_bytes(), (KIT / "profile" / name).read_bytes()
            )

    def test_default_profile_and_invalid_names(self):
        code, _ = self.run_kit("profile", "init", "default")
        self.assertEqual(code, 0)
        self.assertTrue((self.home / ".omp" / "agent" / "config.yml").is_file())
        code, output = self.run_kit("profile", "init", "../escape")
        self.assertEqual(code, 2)
        self.assertIn("invalid profile name", output)
        self.assertFalse((self.home / ".omp" / "escape").exists())


class AuditTests(Sandbox):
    def setUp(self):
        super().setUp()
        terms = self.temp / "terms.txt"
        terms.write_text("# comment\nacme ?corp\n")
        os.environ[kit.PRIVATE_TERMS_ENV] = str(terms)
        self.addCleanup(os.environ.pop, kit.PRIVATE_TERMS_ENV, None)
        self.root = self.temp / "repo"
        (self.root / "skills" / "a").mkdir(parents=True)
        (self.root / "skills" / "a" / "SKILL.md").write_text("Nothing to see.\n")

    def audit(self, pre_push=None):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = kit.audit(self.root, pre_push=pre_push)
        return code, out.getvalue()

    def git(self, *args):
        return subprocess.run(
            ["git", "-C", str(self.root), "-c", "user.name=t", "-c", "user.email=t@users.noreply.github.com", *args],
            check=True, capture_output=True, text=True,
        ).stdout.strip()

    def test_content_terms_and_credential_shapes_are_found(self):
        self.assertEqual(self.audit()[0], 0)
        home_path = "/" + "Users" + "/someone/notes"
        (self.root / "skills" / "a" / "SKILL.md").write_text(f"Built for Acme Corp.\nSee {home_path}\n")
        code, output = self.audit()
        self.assertEqual(code, 1)
        self.assertIn("private term", output)
        self.assertIn("absolute home path", output)

    def test_paths_link_targets_cache_dirs_and_binary_files_are_not_skipped(self):
        (self.root / "acme corp notes.md").write_text("clean\n")
        (self.root / "link").symlink_to("/" + "Users" + "/someone/secret")
        (self.root / "__pycache__").mkdir()
        (self.root / "__pycache__" / "x.txt").write_text("acme corp\n")
        (self.root / "blob.bin").write_bytes(b"acme corp \xff\xfe")
        code, output = self.audit()
        self.assertEqual(code, 1)
        self.assertIn("acme corp notes.md (path)", output)
        self.assertIn("link (link target)", output)
        self.assertIn("__pycache__/x.txt:1: private term", output)
        self.assertIn("blob.bin: not UTF-8 text", output)

    def test_pre_push_scans_outgoing_commits_not_the_working_tree(self):
        self.git("init", "-q", "-b", "main")
        leak = self.root / "skills" / "a" / "SKILL.md"
        leak.write_text("Built for Acme Corp.\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "first")
        leak.write_text("Nothing to see.\n")  # cleaned only in the working tree
        head = self.git("rev-parse", "HEAD")
        # Another remote already holding this history must not exempt a first push.
        self.git("update-ref", "refs/remotes/private/main", head)
        code, output = self.audit(pre_push=f"refs/heads/main {head} refs/heads/main {'0' * 40}\n")
        self.assertEqual(code, 1)
        self.assertIn(f"{head[:7]}:skills/a/SKILL.md:1: private term", output)
        self.git("commit", "-q", "-am", "clean")
        code, output = self.audit()  # full audit still sees the leak in history
        self.assertEqual(code, 1)
        self.assertIn("private term", output)
        self.assertEqual(self.audit(pre_push=f"refs/heads/main {self.git('rev-parse', 'HEAD')} refs/heads/main {head}\n")[0], 0)

    def test_staged_content_is_scanned_even_when_deleted_from_disk(self):
        self.git("init", "-q", "-b", "main")
        staged = self.root / "notes.md"
        staged.write_text("Built for Acme Corp.\n")
        self.git("add", "notes.md")
        staged.unlink()
        code, output = self.audit()
        self.assertEqual(code, 1)
        self.assertIn("notes.md (staged):1: private term", output)


if __name__ == "__main__":
    unittest.main()
