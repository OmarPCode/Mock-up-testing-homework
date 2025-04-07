import unittest
from unittest.mock import patch, mock_open
import subprocess

from src.mockup_exercises import (
    read_data_from_file,
    execute_command,
    perform_action_based_on_time
)


class TestReadDataFromFile(unittest.TestCase):
    def test_read_file_success(self):
        mock_data = "Hello\nWorld"
        with patch("builtins.open", mock_open(read_data=mock_data)):
            result = read_data_from_file("dummy.txt")
            self.assertEqual(result, mock_data)

    def test_read_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            read_data_from_file("nonexistent.txt")


class TestExecuteCommand(unittest.TestCase):
    def test_execute_command_success(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.stdout = "output"
            result = execute_command(["echo", "Hello"])
            self.assertEqual(result, "output")

    def test_execute_command_error(self):
        with patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "cmd")):
            with self.assertRaises(subprocess.CalledProcessError):
                execute_command(["invalid_command"])


class TestPerformActionBasedOnTime(unittest.TestCase):
    def test_action_a(self):
        with patch("time.time", return_value=5):
            self.assertEqual(perform_action_based_on_time(), "Action A")

    def test_action_b(self):
        with patch("time.time", return_value=20):
            self.assertEqual(perform_action_based_on_time(), "Action B")
