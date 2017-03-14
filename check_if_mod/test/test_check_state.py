import unittest
import os

os.chdir('..')
import check_state

TESTFILE = "test_files/text.txt"


class TestState(unittest.TestCase):

	def test_get_file_mtime(self):
		self.assertTrue(check_state.get_file_mtime(TESTFILE))

	def test_get_file_response(self):
		self.assertTrue(type(check_state.get_file_mtime(TESTFILE)), float)

