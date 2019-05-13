import os
import tempfile
import unittest

import toolshed.shed as shed


class ShedTestCase(unittest.TestCase):

    def setUp(self):
        self.home_dir = tempfile.TemporaryDirectory()
        self.the_shed = shed.Shed(self.home_dir.name)

    def tearDown(self):
        self.the_shed.close()
        self.home_dir.cleanup()

    def test_shed_makes_home_dir_if_not_exists(self):
        # Setup
        home_dir = os.path.join(self.home_dir.name, 'test_home')
        assert not os.path.isdir(home_dir)

        # Execute: calling the Shed constructor should make the directory
        shed.Shed(home_dir)

        # Assert
        self.assertTrue(os.path.isdir(home_dir))

    def test_shed_makes_copy(self):
        # Setup
        script = tempfile.NamedTemporaryFile()
        _, tmp_filename = os.path.split(script.name)
        # Execute
        self.the_shed.make(script.name, None, None)

        # Assert
        self.assertTrue(os.path.isfile(os.path.join(self.home_dir.name, tmp_filename)))


if __name__ == '__main__':
    unittest.main()
