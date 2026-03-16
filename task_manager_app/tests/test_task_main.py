import unittest
import sys
import os 

current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, '..', 'src')
sys.path.insert(0, os.path.abspath(src_path))

from main import TaskManagerApp

class TestMainApp(unittest.TestCase):
    def test_app_initialization(self):
        app = TaskManagerApp()
        self.assertEqual(app.title, "Task Manager App")

if __name__ == "__main__":
    unittest.main()