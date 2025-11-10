import unittest
from unittest.mock import patch, MagicMock, call
from invoke import Context
from src.manager import add_task, list_tasks, main
from src.config import Config


class TestManager(unittest.TestCase):
    @patch("src.manager.load_json_file", return_value=[])
    @patch("src.manager.save_json_file")
    @patch(
        "builtins.input", side_effect=["Test Title", "Test Description", "tag1,tag2"]
    )
    @patch("logging.info")
    def test_add_task(
        self, mock_logging_info, mock_input, mock_save_json_file, mock_load_json_file
    ):
        ctx = MagicMock(spec=Context)
        add_task.body(ctx)
        mock_load_json_file.assert_called_once_with(Config.TASKS_FILE)
        mock_save_json_file.assert_called_once()
        args, kwargs = mock_save_json_file.call_args
        self.assertEqual(args[0], Config.TASKS_FILE)
        self.assertEqual(args[1][0]["title"], "Test Title")
        self.assertEqual(args[1][0]["description"], "Test Description")
        self.assertEqual(args[1][0]["tags"], ["tag1", "tag2"])
        self.assertEqual(args[1][0]["status"], "todo")
        mock_logging_info.assert_called_once_with("Task added: Test Title")

    @patch(
        "src.manager.load_json_file",
        return_value=[
            {"id": 1, "title": "Task 1", "status": "todo"},
            {"id": 2, "title": "Task 2", "status": "done"},
        ],
    )
    @patch("builtins.print")
    def test_list_tasks(self, mock_print, mock_load_json_file):
        ctx = MagicMock(spec=Context)
        list_tasks.body(ctx)
        mock_load_json_file.assert_called_once_with(Config.TASKS_FILE)
        mock_print.assert_has_calls(
            [
                call("1: Task 1 - todo"),
                call("2: Task 2 - done"),
            ]
        )

    @patch("src.manager.run_command")
    def test_main_task(self, mock_run_command):
        ctx = MagicMock(spec=Context)
        main.body(ctx)
        mock_run_command.assert_called_once_with(
            ctx, "poe --list", "To select command type poe again and cmd", "fail"
        )


if __name__ == "__main__":
    unittest.main()
