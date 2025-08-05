import unittest
from unittest.mock import patch
from io import StringIO
from main import main

class TestMain(unittest.TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    def test_main(self, mock_stdout):
        main()
        self.assertEqual(mock_stdout.getvalue(), "Hello from task-runner-sdlc!\n")

if __name__ == '__main__':
    unittest.main()
