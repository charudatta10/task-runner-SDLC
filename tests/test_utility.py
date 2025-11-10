import unittest
from unittest.mock import patch, MagicMock
import json
import os
from src.utility import (
    run_command,
    download_file,
    load_json_file,
    save_json_file,
    generate_file,
)


class TestUtility(unittest.TestCase):
    def test_run_command_success(self):
        ctx = MagicMock()
        self.assertTrue(run_command(ctx, 'echo "test" ', "Success", "Error"))
        ctx.run.assert_called_once_with('echo "test" ')

    def test_run_command_failure(self):
        ctx = MagicMock()
        ctx.run.side_effect = Exception("Test Exception")
        self.assertFalse(run_command(ctx, "invalid_command", "Success", "Error"))

    @patch("urllib.request.urlretrieve")
    def test_download_file_success(self, mock_urlretrieve):
        self.assertTrue(download_file("http://example.com/file.txt", "file.txt"))
        mock_urlretrieve.assert_called_once_with(
            "http://example.com/file.txt", "file.txt"
        )

    @patch("urllib.request.urlretrieve", side_effect=Exception("Download Error"))
    def test_download_file_failure(self, mock_urlretrieve):
        self.assertFalse(download_file("http://example.com/file.txt", "file.txt"))

    def test_load_json_file_exists(self):
        with open("test.json", "w") as f:
            json.dump([{"key": "value"}], f)
        data = load_json_file("test.json")
        self.assertEqual(data, [{"key": "value"}])
        os.remove("test.json")

    def test_load_json_file_not_exists(self):
        data = load_json_file("non_existent_file.json")
        self.assertEqual(data, [])

    def test_save_json_file(self):
        data = [{"key": "value"}]
        save_json_file("test.json", data)
        with open("test.json", "r") as f:
            saved_data = json.load(f)
        self.assertEqual(saved_data, data)
        os.remove("test.json")

    def test_generate_file(self):
        template_content = "Hello, {name}!"
        with open("template.txt", "w") as f:
            f.write(template_content)
        config = {"name": "World"}
        generate_file("template.txt", config, "output.txt")
        with open("output.txt", "r") as f:
            content = f.read()
        self.assertEqual(content, "Hello, World!")
        os.remove("template.txt")
        os.remove("output.txt")


if __name__ == "__main__":
    unittest.main()
