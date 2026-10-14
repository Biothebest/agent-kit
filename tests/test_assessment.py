"""Behavior tests for skills/coordinator/scripts/assessment.py."""

import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "skills" / "coordinator" / "scripts" / "assessment.py"
SPEC = importlib.util.spec_from_file_location("coordinator_assessment", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
assessment = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = assessment
SPEC.loader.exec_module(assessment)


def valid_plan():
    return {
        "schema_version": 1,
        "variant": "Compact coordinator brief",
        "candidate_prompt": "Build a small todo command that stores items in one local JSON file.",
        "criteria": [
            {"id": "outcome", "description": "The command persists and lists todo items correctly.", "weight": 5, "hard_gate": True},
            {"id": "evidence", "description": "Claims match observable command receipts.", "weight": 5, "hard_gate": True},
            {"id": "maintainability", "description": "The implementation is small and coherent.", "weight": 3, "hard_gate": False},
        ],
        "labels": ["cedar", "harbor"],
    }


class AssessmentPlanTests(unittest.TestCase):
    def test_valid_plan_is_fingerprinted_without_echoing_control_text(self):
        plan = valid_plan()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "control.json"
            path.write_text(json.dumps(plan), encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(assessment.main([str(path)]), 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["status"], "valid")
        self.assertEqual((payload["criteria_count"], payload["labels_count"]), (3, 2))
        self.assertEqual(payload["plan_sha256"], assessment.plan_fingerprint(plan))
        self.assertNotIn(plan["variant"], output.getvalue())
        self.assertNotIn(plan["candidate_prompt"], output.getvalue())

    def test_prompt_refuses_observer_effect_terms_and_criterion_text(self):
        for term in assessment.FORBIDDEN_PROMPT_TERMS:
            plan = valid_plan()
            plan["candidate_prompt"] = f"Please {term}s this todo command."
            with self.subTest(term=term), self.assertRaisesRegex(assessment.PlanError, "forbidden control term"):
                assessment.validate_plan(plan)
        plan = valid_plan()
        plan["candidate_prompt"] = "Build a todo command. " + plan["criteria"][0]["description"]
        with self.assertRaisesRegex(assessment.PlanError, "leaks criteria.0.description"):
            assessment.validate_plan(plan)

    def test_plan_shape_is_closed(self):
        cases = [
            (lambda p: p.update(criteria=p["criteria"][:2]), "3 to 6"),
            (lambda p: p.update(labels=["cedar", "cedar"]), "labels must be unique"),
            (lambda p: p.update(labels=["cedar", "candidate-two"]), "leaks a control term"),
            (lambda p: p.update(labels=["cedar", {}]), "labels.1 is invalid"),
            (lambda p: p.update(notes="extra"), "unknown notes"),
            (lambda p: p["criteria"][0].update(weight=True), "integer from 1 to 5"),
        ]
        for mutate, message in cases:
            plan = valid_plan()
            mutate(plan)
            with self.subTest(message=message), self.assertRaisesRegex(assessment.PlanError, message):
                assessment.validate_plan(plan)


if __name__ == "__main__":
    unittest.main()
