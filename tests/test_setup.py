import unittest
from unittest.mock import patch, MagicMock, call
from invoke import Context
from pathlib import Path
from src.setup import init_project
from src.config import Config


class TestSetup(unittest.TestCase):
    @patch("os.path.exists", return_value=False)
    @patch("os.makedirs")
    @patch("pathlib.Path.touch")
    @patch("src.setup.download_file", return_value=True)
    @patch("logging.info")
    def test_init_project(
        self,
        mock_logging_info,
        mock_download_file,
        mock_touch,
        mock_makedirs,
        mock_exists,
    ):
        ctx = MagicMock(spec=Context)
        ctx.run = MagicMock()

        init_project.body(ctx)

        # Test directory creation
        makedirs_calls = [call(d) for d in Config.PROJECT_DIRS]
        mock_makedirs.assert_has_calls(makedirs_calls, any_order=True)
        self.assertEqual(mock_makedirs.call_count, len(Config.PROJECT_DIRS))

        # Test file creation
        touch_calls = [call() for _ in Config.PROJECT_FILES]
        mock_touch.assert_has_calls(touch_calls, any_order=True)
        self.assertEqual(mock_touch.call_count, len(Config.PROJECT_FILES))

        # Test community file download
        download_calls = []
        for file in Config.COMMUNITY_FILES:
            download_calls.append(call(f"{Config.REPO_DOCS}/{Path(file).name}", file))
        mock_download_file.assert_has_calls(download_calls, any_order=True)
        self.assertEqual(mock_download_file.call_count, len(Config.COMMUNITY_FILES))

        # Test uv init
        ctx.run.assert_called_once_with("uv init")

        # Test logging
        self.assertIn(
            call("Project initialized successfully."), mock_logging_info.call_args_list
        )


if __name__ == "__main__":
    unittest.main()
