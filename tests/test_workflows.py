"""Guards for the security rules in docs/SECURITY.md. Plain text checks, no YAML dependency."""
import glob
import os
import re
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
FILES = sorted(glob.glob(os.path.join(ROOT, ".github", "workflows", "*.yml")))


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


class WorkflowRules(unittest.TestCase):
    def test_there_are_workflows_to_check(self):
        self.assertGreaterEqual(len(FILES), 4)

    def test_every_action_is_pinned_to_a_full_commit_sha(self):
        for path in FILES:
            for line in read(path).splitlines():
                m = re.match(r"\s*-?\s*uses:\s*(\S+)", line)
                if m:
                    with self.subTest(os.path.basename(path) + " " + m.group(1)):
                        self.assertRegex(m.group(1), r"@[0-9a-f]{40}$")

    def test_no_dangerous_triggers(self):
        for path in FILES:
            text = read(path)
            with self.subTest(os.path.basename(path)):
                self.assertNotIn("pull_request_target", text)
                self.assertNotIn("workflow_run", text)

    def test_permissions_are_declared_and_never_broader_than_needed(self):
        for path in FILES:
            text = read(path)
            with self.subTest(os.path.basename(path)):
                self.assertRegex(text, r"(?m)^permissions:")
                self.assertNotIn("write-all", text)
                self.assertNotRegex(text, r"(?m)^\s+(issues|pull-requests|actions|packages|id-token): write")

    def test_untrusted_expressions_never_reach_a_shell_script(self):
        """Event data and inputs may only be used in env, with or if lines, never inline in run scripts."""
        for path in FILES:
            in_run = False
            indent = 0
            for n, line in enumerate(read(path).splitlines(), 1):
                stripped = line.strip()
                cur = len(line) - len(line.lstrip())
                if re.match(r"\s*-?\s*run:\s*[|>]", line):
                    in_run, indent = True, cur
                    continue
                if in_run and stripped and cur <= indent:
                    in_run = False
                if in_run and "${{" in line:
                    with self.subTest("%s:%d" % (os.path.basename(path), n)):
                        self.fail("expression inside a run script: " + stripped)

    def test_nothing_ever_pushes_to_main_or_develop(self):
        for path in FILES:
            with self.subTest(os.path.basename(path)):
                self.assertNotRegex(read(path), r"git push (origin )?(main|develop)")

    def test_workflows_only_publish_to_the_output_branch(self):
        """A push goes to `output`, or to a variable TARGET that the workflow restricts to a choice of
        `output` and `output-preview`. Nothing else is allowed."""
        for path in FILES:
            text = read(path)
            for line in text.splitlines():
                if "git push" in line:
                    with self.subTest(os.path.basename(path) + " " + line.strip()):
                        stripped = line.strip()
                        if stripped == 'git push origin "$TARGET"':
                            self.assertRegex(text, r"options:\n\s+- output\n\s+- output-preview\n(?!\s+- )")
                            self.assertIn("type: choice", text)
                        else:
                            self.assertEqual(stripped, "git push origin output")

    def test_the_season_input_is_only_passed_through_the_environment(self):
        text = read(os.path.join(ROOT, ".github", "workflows", "seasons.yml"))
        self.assertIn("SEASON: ${{ inputs.season || '' }}", text)
        self.assertEqual(text.count("inputs.season"), 1)
        self.assertNotRegex(text, r"run:.*\$\{\{")

    def test_the_seasonal_workflow_tests_and_builds_before_publishing(self):
        text = read(os.path.join(ROOT, ".github", "workflows", "seasons.yml"))
        order = [text.index(s) for s in ("unittest discover", "build_seasonal.py", "git push")]
        self.assertEqual(order, sorted(order))
        self.assertNotIn("secrets.", text)                 # it needs no token beyond the built in one


if __name__ == "__main__":
    unittest.main()
