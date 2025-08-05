import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from src.licenser import get_files, license_text, add_header
from src.config import Config

class TestLicenser(unittest.TestCase):
    @patch('pathlib.Path.rglob')
    def test_get_files(self, mock_rglob):
        mock_rglob.return_value = [
            Path("src/file1.py"),
            Path("src/file2.js"),
            Path("src/file3.txt"), # Should be ignored
        ]
        files = list(get_files("src"))
        self.assertEqual(len(files), 2)
        self.assertIn(Path("src/file1.py"), files)
        self.assertIn(Path("src/file2.js"), files)

    def test_license_text_py(self):
        text = license_text(".py")
        self.assertEqual(text, f"# {Config.LICENSE_HEADER}\n")

    def test_license_text_html(self):
        text = license_text(".html")
        self.assertEqual(text, f"<!-- {Config.LICENSE_HEADER}\n -->\n")

    @patch('src.licenser.get_files')
    def test_add_header_add(self, mock_get_files):
        mock_file = MagicMock()
        mock_file.suffix = ".py"
        mock_file.read_text.return_value = "existing content"
        mock_get_files.return_value = [mock_file]

        ctx = MagicMock()
        add_header.body(ctx, action="add")

        expected_text = f"# {Config.LICENSE_HEADER}\nexisting content"
        mock_file.write_text.assert_called_once_with(expected_text, encoding="utf-8")

    @patch('src.licenser.get_files')
    def test_add_header_remove(self, mock_get_files):
        mock_file = MagicMock()
        mock_file.suffix = ".py"
        license_header_with_comment = f"# {Config.LICENSE_HEADER}\n"
        mock_file.read_text.return_value = f"{license_header_with_comment}existing content"
        mock_get_files.return_value = [mock_file]

        ctx = MagicMock()
        add_header.body(ctx, action="remove")

        expected_text = "existing content"
        mock_file.write_text.assert_called_once_with(expected_text, encoding="utf-8")

if __name__ == "__main__":
    unittest.main()
