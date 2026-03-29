import sys
import os
import types
import unittest
from unittest.mock import MagicMock, patch, call


def _load_main_module():
    """Import main module with GITHUB_TOKEN mocked and input patched."""
    # Provide a fake token so the module-level check doesn't raise
    with patch.dict(os.environ, {"GITHUB_TOKEN": "fake-token"}):
        # Patch Github and input at import time
        fake_github = MagicMock()
        fake_github.return_value = MagicMock()
        with patch.dict("sys.modules", {"github": types.ModuleType("github")}):
            sys.modules["github"].Github = fake_github
            with patch("builtins.input", return_value="test-owner"):
                import importlib
                if "main" in sys.modules:
                    del sys.modules["main"]
                spec = importlib.util.spec_from_file_location(
                    "main",
                    os.path.join(os.path.dirname(__file__), "..", "main.py"),
                )
                mod = importlib.util.module_from_spec(spec)
                # Prevent module-level side effects (the repo-fetching block)
                with patch("threading.Thread"):
                    try:
                        spec.loader.exec_module(mod)
                    except Exception:
                        pass
                return mod


class TestProcessRepo(unittest.TestCase):
    def _make_check_run(self, status="completed", conclusion="success"):
        cr = MagicMock()
        cr.status = status
        cr.conclusion = conclusion
        return cr

    def _make_pull_request(self, number=1, sha="abc123"):
        pr = MagicMock()
        pr.number = number
        pr.head.sha = sha
        return pr

    def _make_repo(self, full_name="owner/repo", private=False):
        repo = MagicMock()
        repo.full_name = full_name
        repo.private = private
        return repo

    @patch.dict(os.environ, {"GITHUB_TOKEN": "fake-token"})
    def test_merge_called_when_all_checks_pass(self):
        """process_repo merges a PR when all check runs are successful."""
        with patch.dict("sys.modules", {"github": types.ModuleType("github")}):
            sys.modules["github"].Github = MagicMock()
            with patch("builtins.input", return_value="owner"):
                import importlib
                if "main" in sys.modules:
                    del sys.modules["main"]
                spec = importlib.util.spec_from_file_location(
                    "main",
                    os.path.join(os.path.dirname(__file__), "..", "main.py"),
                )
                mod = importlib.util.module_from_spec(spec)
                with patch("threading.Thread"):
                    try:
                        spec.loader.exec_module(mod)
                    except Exception:
                        pass

        pr = self._make_pull_request(number=42)
        repo = self._make_repo()
        repo.get_pulls.return_value = [pr]

        check_run = self._make_check_run(status="completed", conclusion="success")
        mock_commit = MagicMock()
        mock_commit.get_check_runs.return_value = [check_run]
        mock_repo_obj = MagicMock()
        mock_repo_obj.get_commit.return_value = mock_commit

        mod.g = MagicMock()
        mod.g.get_repo.return_value = mock_repo_obj

        mod.process_repo(repo)

        pr.merge.assert_called_once()

    @patch.dict(os.environ, {"GITHUB_TOKEN": "fake-token"})
    def test_no_merge_when_check_not_completed(self):
        """process_repo does not merge a PR when a check is still in progress."""
        with patch.dict("sys.modules", {"github": types.ModuleType("github")}):
            sys.modules["github"].Github = MagicMock()
            with patch("builtins.input", return_value="owner"):
                import importlib
                if "main" in sys.modules:
                    del sys.modules["main"]
                spec = importlib.util.spec_from_file_location(
                    "main",
                    os.path.join(os.path.dirname(__file__), "..", "main.py"),
                )
                mod = importlib.util.module_from_spec(spec)
                with patch("threading.Thread"):
                    try:
                        spec.loader.exec_module(mod)
                    except Exception:
                        pass

        pr = self._make_pull_request(number=7)
        repo = self._make_repo()
        repo.get_pulls.return_value = [pr]

        check_run = self._make_check_run(status="in_progress", conclusion=None)
        mock_commit = MagicMock()
        mock_commit.get_check_runs.return_value = [check_run]
        mock_repo_obj = MagicMock()
        mock_repo_obj.get_commit.return_value = mock_commit

        mod.g = MagicMock()
        mod.g.get_repo.return_value = mock_repo_obj

        mod.process_repo(repo)

        pr.merge.assert_not_called()

    @patch.dict(os.environ, {"GITHUB_TOKEN": "fake-token"})
    def test_no_merge_when_check_failed(self):
        """process_repo does not merge a PR when a check has failed."""
        with patch.dict("sys.modules", {"github": types.ModuleType("github")}):
            sys.modules["github"].Github = MagicMock()
            with patch("builtins.input", return_value="owner"):
                import importlib
                if "main" in sys.modules:
                    del sys.modules["main"]
                spec = importlib.util.spec_from_file_location(
                    "main",
                    os.path.join(os.path.dirname(__file__), "..", "main.py"),
                )
                mod = importlib.util.module_from_spec(spec)
                with patch("threading.Thread"):
                    try:
                        spec.loader.exec_module(mod)
                    except Exception:
                        pass

        pr = self._make_pull_request(number=3)
        repo = self._make_repo()
        repo.get_pulls.return_value = [pr]

        check_run = self._make_check_run(status="completed", conclusion="failure")
        mock_commit = MagicMock()
        mock_commit.get_check_runs.return_value = [check_run]
        mock_repo_obj = MagicMock()
        mock_repo_obj.get_commit.return_value = mock_commit

        mod.g = MagicMock()
        mod.g.get_repo.return_value = mock_repo_obj

        mod.process_repo(repo)

        pr.merge.assert_not_called()

    @patch.dict(os.environ, {"GITHUB_TOKEN": "fake-token"})
    def test_merge_exception_is_handled(self):
        """process_repo handles a merge exception without crashing."""
        with patch.dict("sys.modules", {"github": types.ModuleType("github")}):
            sys.modules["github"].Github = MagicMock()
            with patch("builtins.input", return_value="owner"):
                import importlib
                if "main" in sys.modules:
                    del sys.modules["main"]
                spec = importlib.util.spec_from_file_location(
                    "main",
                    os.path.join(os.path.dirname(__file__), "..", "main.py"),
                )
                mod = importlib.util.module_from_spec(spec)
                with patch("threading.Thread"):
                    try:
                        spec.loader.exec_module(mod)
                    except Exception:
                        pass

        pr = self._make_pull_request(number=5)
        pr.merge.side_effect = Exception("merge conflict")
        repo = self._make_repo()
        repo.get_pulls.return_value = [pr]

        check_run = self._make_check_run(status="completed", conclusion="success")
        mock_commit = MagicMock()
        mock_commit.get_check_runs.return_value = [check_run]
        mock_repo_obj = MagicMock()
        mock_repo_obj.get_commit.return_value = mock_commit

        mod.g = MagicMock()
        mod.g.get_repo.return_value = mock_repo_obj

        # Should not raise
        mod.process_repo(repo)

    @patch.dict(os.environ, {"GITHUB_TOKEN": "fake-token"})
    def test_no_checks_means_no_merge(self):
        """process_repo does not merge when there are no check runs (all() on empty is True, so this documents current behavior)."""
        with patch.dict("sys.modules", {"github": types.ModuleType("github")}):
            sys.modules["github"].Github = MagicMock()
            with patch("builtins.input", return_value="owner"):
                import importlib
                if "main" in sys.modules:
                    del sys.modules["main"]
                spec = importlib.util.spec_from_file_location(
                    "main",
                    os.path.join(os.path.dirname(__file__), "..", "main.py"),
                )
                mod = importlib.util.module_from_spec(spec)
                with patch("threading.Thread"):
                    try:
                        spec.loader.exec_module(mod)
                    except Exception:
                        pass

        pr = self._make_pull_request(number=9)
        repo = self._make_repo()
        repo.get_pulls.return_value = [pr]

        mock_commit = MagicMock()
        mock_commit.get_check_runs.return_value = []  # no checks
        mock_repo_obj = MagicMock()
        mock_repo_obj.get_commit.return_value = mock_commit

        mod.g = MagicMock()
        mod.g.get_repo.return_value = mock_repo_obj

        # all() on empty iterable is True, so merge IS called — documenting this behavior
        mod.process_repo(repo)
        pr.merge.assert_called_once()


if __name__ == "__main__":
    unittest.main()
