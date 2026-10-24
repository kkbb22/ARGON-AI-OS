import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "runtime" / "argon_runtime.py"
spec = importlib.util.spec_from_file_location("argon_runtime", MODULE_PATH)
runtime = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runtime)


class RuntimeTests(unittest.TestCase):
    def test_accepts_safe_text_write(self):
        plan = {"task": "demo", "actions": [
            {"type": "write_text", "path": "demo.txt", "content": "hello"}
        ]}
        self.assertTrue(runtime.validate_plan(plan))

    def test_rejects_path_traversal(self):
        plan = {"task": "demo", "actions": [
            {"type": "write_text", "path": "../outside.txt", "content": "x"}
        ]}
        with self.assertRaises(ValueError):
            runtime.validate_plan(plan)

    def test_rejects_unknown_action(self):
        plan = {"task": "demo", "actions": [
            {"type": "run_shell", "path": "x", "content": "del *"}
        ]}
        with self.assertRaises(ValueError):
            runtime.validate_plan(plan)

    def test_rejects_extra_keys(self):
        plan = {"task": "demo", "actions": [], "approved": True}
        with self.assertRaises(ValueError):
            runtime.validate_plan(plan)

    def test_digest_changes_when_plan_changes(self):
        a = {"task": "demo", "actions": [
            {"type": "write_text", "path": "a.txt", "content": "one"}
        ]}
        b = {"task": "demo", "actions": [
            {"type": "write_text", "path": "a.txt", "content": "two"}
        ]}
        self.assertNotEqual(runtime.plan_digest(a), runtime.plan_digest(b))


if __name__ == "__main__":
    unittest.main(verbosity=2)
