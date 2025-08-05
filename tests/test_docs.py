import unittest
from unittest.mock import patch, MagicMock, call
from invoke import Context
from src.docs import collect_items, collect_project_data, setup_docs, generate_docs
from src.config import Config

class TestDocs(unittest.TestCase):
    @patch('builtins.input', side_effect=['feature1', 'feature2', 'done'])
    def test_collect_items_list_features(self, mock_input):
        result = collect_items("Enter project features -> ", "list_features")
        self.assertEqual(result, "- feature1\n- feature2")

    @patch('builtins.input', side_effect=['badge1', 'badge2', 'done'])
    def test_collect_items_list_badges(self, mock_input):
        result = collect_items("Enter softwares used in the project -> ", "list_badges")
        self.assertEqual(result, "`badge1` `badge2`")

    @patch('builtins.input', side_effect=['Title', 'Description', 'f1', 'done', 'b1', 'done'])
    def test_collect_project_data(self, mock_input):
        data = collect_project_data()
        self.assertEqual(data["title"], "Title")
        self.assertEqual(data["description"], "Description")
        self.assertEqual(data["features"], "- f1")
        self.assertEqual(data["list_badges"], "`b1`")

    @patch('src.docs.download_file', return_value=True)
    @patch('src.docs.generate_file')
    @patch('src.docs.collect_project_data', return_value={'title': 'Test Title'})
    def test_setup_docs(self, mock_collect_project_data, mock_generate_file, mock_download_file):
        ctx = MagicMock(spec=Context)
        setup_docs(ctx)
        self.assertEqual(mock_download_file.call_count, len(Config.DOCS_FILES))
        self.assertEqual(mock_generate_file.call_count, len(Config.DOCS_FILES))

    def test_generate_docs(self):
        ctx = MagicMock(spec=Context)
        ctx.run = MagicMock()
        generate_docs(ctx)
        ctx.run.assert_called_once_with(f"python {Config.DOC_GEN_FILE} .")

if __name__ == "__main__":
    unittest.main()
