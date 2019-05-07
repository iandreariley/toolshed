import os
import shutil
import unittest

import shed


TEST_HOME_DIR = os.path.join(os.getcwd() + "tmp")


class ShedTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.makedirs(TEST_HOME_DIR, exist_ok=True)

    def test_shed_makes_home_dir_if_not_exists(self):
        # Setup
        home_dir = os.path.join(TEST_HOME_DIR, 'test_home')
        assert not os.path.isdir(home_dir)

        # Execute: calling the Shed constructor should make the directory
        shed.Shed(home_dir)

        # Assert
        self.assertTrue(os.path.isdir(home_dir))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEST_HOME_DIR)


if __name__ == '__main__':
    unittest.main()
