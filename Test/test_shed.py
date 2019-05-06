import os
import unittest

import loggers
import shed


TEST_HOME_DIR = os.path.join(os.getcwd() + "tmp")


class ShedTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.makedirs(TEST_HOME_DIR, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        os.rmdir(TEST_HOME_DIR)
