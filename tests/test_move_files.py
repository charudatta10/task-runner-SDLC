import unittest
from unittest.mock import patch, MagicMock, mock_open, call
import json
import shutil
import logging
from invoke import Context
from pathlib import Path
from src.tools.move_files import (
    organize_files,
    create_patterns_sample,
    clean_folder,
)
from src.tools.move_files import get_unique_filename
from src.tools.move_files import move_files_to_directory
from src.tools.move_files import ensure_directories_exist
from src.tools.move_files import validate_paths

class TestMoveFiles(unittest.TestCase):
    @patch('builtins.print')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_create_patterns_sample(self, mock_json_dump, mock_file_open, mock_print):
        ctx = MagicMock(spec=Context)
        create_patterns_sample.body(ctx, output_file="test_patterns.json")

        mock_file_open.assert_called_once_with("test_patterns.json", 'w', encoding='utf-8')
        mock_json_dump.assert_called_once()
        mock_print.assert_called_once_with("✅ Sample patterns file created at: test_patterns.json")

    @patch('src.tools.move_files.organize_files.body')
    def test_clean_folder(self, mock_organize_files_body):
        ctx = MagicMock(spec=Context)
        clean_folder.body(ctx, folder="./test_folder", patterns="my_patterns.json", destination="./dest_folder")
        mock_organize_files_body.assert_called_once_with(ctx, "./test_folder", "./dest_folder", "my_patterns.json")

    @patch('src.tools.move_files.organize_files.body')
    def test_clean_folder_default_destination(self, mock_organize_files_body):
        ctx = MagicMock(spec=Context)
        clean_folder.body(ctx, folder="./test_folder", patterns="my_patterns.json")
        mock_organize_files_body.assert_called_once_with(ctx, "./test_folder", "./test_folder", "my_patterns.json")

    @patch('src.tools.move_files.setup_logging')
    @patch('src.tools.move_files.shutil.move')
    @patch('src.tools.move_files.json.load')
    @patch('builtins.open', new_callable=mock_open)
    @patch('src.tools.move_files.validate_paths')
    @patch('src.tools.move_files.ensure_directories_exist')
    @patch('src.tools.move_files.move_files_to_directory')
    @patch('builtins.print')
    def test_organize_files(self, mock_print, mock_move_files_to_directory, mock_ensure_directories_exist, mock_validate_paths, mock_open, mock_json_load, mock_shutil_move, mock_setup_logging):
        # Setup mocks
        mock_source_path = MagicMock(spec=Path)
        mock_dest_path = MagicMock(spec=Path)
        mock_patterns_path = MagicMock(spec=Path)
        
        mock_validate_paths.return_value = (mock_source_path, mock_dest_path, mock_patterns_path)
        
        mock_logger = MagicMock()
        mock_setup_logging.return_value = mock_logger

        mock_json_load.return_value = {
            "Images": ["*.jpg", "*.png"],
            "Documents": ["*.pdf"]
        }

        mock_dest_path.name = 'destination'

        ctx = MagicMock(spec=Context)
        organize_files.body(ctx, "/source", "/destination", "/patterns.json")

        # Assertions
        mock_validate_paths.assert_called_once_with("/source", "/destination", "/patterns.json")
        mock_setup_logging.assert_called_once() # Argument depends on dest_path, so just check called
        mock_open.assert_called_once_with(mock_patterns_path, "r", encoding="utf-8")
        mock_json_load.assert_called_once()
        mock_ensure_directories_exist.assert_called_once() # Argument depends on category_dirs, so just check called
        mock_move_files_to_directory.assert_has_calls([
            call(mock_source_path, ["*.jpg", "*.png"], mock_dest_path / "Images", mock_logger),
            call(mock_source_path, ["*.pdf"], mock_dest_path / "Documents", mock_logger),
        ], any_order=True)

        mock_logger.info.assert_has_calls([
            call(f"Starting file organization from: {mock_source_path} to: {mock_dest_path}"),
            call(f"Loaded file patterns from: {mock_patterns_path}"),
            call("Created/verified 2 category directories"),
            call("Processing category: Images"),
            call("Processing category: Documents"),
            call("File organization completed. Total: 0 moved, 0 failed"), # Default return from mock_move_files_to_directory
        ], any_order=True)

        mock_print.assert_has_calls([
            call("🚀 Starting file organization"),
            call(f"📂 Source: {mock_source_path}"),
            call(f"📁 Destination: {mock_dest_path}"),
            call(f"📋 Loaded file patterns from: {mock_patterns_path}"),
            call("📁 Created/verified 2 category directories"),
            call("\n📁 Processing Images..."),
            call("\n📁 Processing Documents..."),
            call("\n✅ File organization completed!"),
            call("📊 Summary: 0 files moved, 0 failed"),
        ], any_order=True)

    @patch('src.tools.move_files.Path.exists')
    def test_get_unique_filename_no_duplicate(self, mock_exists):
        mock_exists.return_value = False
        destination_path = MagicMock(spec=Path)
        filename = 'file.txt'
        unique_filename = get_unique_filename(destination_path, filename)
        self.assertEqual(unique_filename, 'file.txt')

    @patch('src.tools.move_files.Path.exists')
    def test_get_unique_filename_with_duplicates(self, mock_exists):
        # Simulate file.txt exists, file_v1.txt exists, file_v2.txt does not
        mock_exists.side_effect = [True, True, False]
        destination_path = MagicMock(spec=Path)
        filename = 'file.txt'
        unique_filename = get_unique_filename(destination_path, filename)
        self.assertEqual(unique_filename, 'file_v2.txt')

    @patch('src.tools.move_files.Path.exists')
    def test_get_unique_filename_no_extension(self, mock_exists):
        # Simulate file exists, file_v1 does not
        mock_exists.side_effect = [True, False]
        destination_path = MagicMock(spec=Path)
        filename = 'file_no_ext'
        unique_filename = get_unique_filename(destination_path, filename)
        self.assertEqual(unique_filename, 'file_no_ext_v1')

    @patch('src.tools.move_files.Path.exists', return_value=True)
    @patch('src.tools.move_files.Path.is_dir', return_value=True)
    @patch('src.tools.move_files.Path.resolve', side_effect=lambda: MagicMock(spec=Path, exists=MagicMock(return_value=True), is_dir=MagicMock(return_value=True)))
    @patch('src.tools.move_files.Path.mkdir')
    def test_validate_paths_success(self, mock_mkdir, mock_resolve, mock_is_dir, mock_exists):
        source_path, dest_path, patterns_path = validate_paths("/source", "/destination", "/patterns.json")
        self.assertIsInstance(source_path, MagicMock)
        self.assertIsInstance(dest_path, MagicMock)
        self.assertIsInstance(patterns_path, MagicMock)
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

    @patch('src.tools.move_files.Path.exists', return_value=False)
    @patch('builtins.print')
    def test_validate_paths_source_not_found(self, mock_print, mock_exists):
        with self.assertRaises(FileNotFoundError):
            validate_paths("/nonexistent_source", "/destination", "/patterns.json")
        mock_print.assert_called_once()

    @patch('src.tools.move_files.Path.exists', return_value=True)
    @patch('src.tools.move_files.Path.is_dir', return_value=False)
    @patch('builtins.print')
    def test_validate_paths_source_not_directory(self, mock_print, mock_is_dir, mock_exists):
        with self.assertRaises(ValueError):
            validate_paths("/source_file", "/destination", "/patterns.json")
        mock_print.assert_called_once()

    @patch('src.tools.move_files.Path.exists', side_effect=[True, True, False]) # source exists, dest exists, patterns not exists
    @patch('src.tools.move_files.Path.is_dir', return_value=True)
    @patch('builtins.print')
    def test_validate_paths_patterns_not_found(self, mock_print, mock_is_dir, mock_exists):
        with self.assertRaises(FileNotFoundError):
            validate_paths("/source", "/destination", "/nonexistent_patterns.json")
        mock_print.assert_called_once()

    @patch('src.tools.move_files.get_unique_filename', side_effect=['file1.txt', 'file2_v1.txt'])
    @patch('shutil.move')
    @patch('builtins.print')
    @patch('logging.info')
    @patch('logging.error')
    def test_move_files_to_directory(self, mock_error, mock_info, mock_print, mock_shutil_move, mock_get_unique_filename):
        source_path = MagicMock(spec=Path)
        destination_path = MagicMock(spec=Path)
        destination_path.name = "dest_dir"
        logger = MagicMock()

        mock_file1 = MagicMock(spec=Path)
        mock_file1.name = "file1.txt"
        mock_file1.is_dir.return_value = False
        mock_file2 = MagicMock(spec=Path)
        mock_file2.name = "file2.txt"
        mock_file2.is_dir.return_value = False
        mock_file3_dir = MagicMock(spec=Path)
        mock_file3_dir.name = "dir1"
        mock_file3_dir.is_dir.return_value = True

        source_path.glob.side_effect = lambda pattern: {
            "*.txt": [mock_file1, mock_file2, mock_file3_dir]
        }.get(pattern, [])

        moved, skipped = move_files_to_directory(source_path, ["*.txt"], destination_path, logger)

        self.assertEqual(moved, 2)
        self.assertEqual(skipped, 0)
        mock_shutil_move.assert_has_calls([
            call(str(mock_file1), str(destination_path / 'file1.txt')),
            call(str(mock_file2), str(destination_path / 'file2_v1.txt')),
        ])
        mock_info.assert_has_calls([
            call("MOVED: file1.txt -> {}{}/".format(destination_path, 'file1.txt')),
            call("MOVED (renamed): file2.txt -> {}{} (renamed due to duplicate)".format(destination_path, 'file2_v1.txt')),
        ])
        mock_print.assert_has_calls([
            call("✓ Moved: file1.txt -> dest_dir/"),
            call("✓ Moved and renamed: file2.txt -> file2_v1.txt"),
        ])

    @patch('pathlib.Path.mkdir')
    def test_ensure_directories_exist(self, mock_mkdir):
        dir1 = MagicMock(spec=Path)
        dir2 = MagicMock(spec=Path)
        ensure_directories_exist(dir1, dir2)
        mock_mkdir.assert_has_calls([
            call(parents=True, exist_ok=True),
            call(parents=True, exist_ok=True),
        ])

if __name__ == "__main__":
    unittest.main()
