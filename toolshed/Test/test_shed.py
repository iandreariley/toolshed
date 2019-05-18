import collections.abc
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
        tmp_filename = self._get_temp_file_name(script)

        # Execute
        self.the_shed.make(script.name, None, None)

        # Assert
        self.assertTrue(os.path.isfile(os.path.join(self.home_dir.name, tmp_filename)))

    def test_find_withNoArguments_returnsAllScripts(self):
        # Setup
        tag = 'test_tag'
        _, script_one_filename = self._make_named_temp_file(tags=[tag])
        _, script_two_filename = self._make_named_temp_file(tags=[tag])

        # expected result script names as set (ignore order)
        expected_results = {script_one_filename, script_two_filename}

        # Execute
        all_results = self.the_shed.find()

        # Assert
        self.assertResultsEqual(
            all_results, expected_results,
            'shed.find() should return all results: {}, but returned {} '
            'instead'.format(expected_results, all_results))

    def test_find_withTagArgument_returnsTaggedScripts(self):
        # Setup
        tag = 'test_tag'

        # Two files with the tag to be search for
        _, script_one_filename = self._make_named_temp_file(tags=[tag])
        _, script_two_filename = self._make_named_temp_file(tags=[tag])

        # ... and one script without.
        self._make_named_temp_file()

        # expected result script names as set (ignore order)
        expected_results = {script_one_filename, script_two_filename}

        # Execute
        tag_results = self.the_shed.find(tags=(tag,))

        # Assert
        self.assertResultsEqual(
            tag_results, expected_results,
            'shed.find(tags=["{}"]) should return the following scripts: {} but instead returned '
            '{}.'.format(tag, expected_results, tag_results))

    def test_find_withNameArgument_returnsNamedScript(self):
        # Setup
        tag = 'test_tag'
        script_path, script_filename = self._make_named_temp_file(tags=[tag])

        # Make one file with a different name to make sure it isn't returned.
        self._make_named_temp_file()

        # Execute
        name_results = self.the_shed.find(name=script_filename)

        # Assert
        self.assertResultsEqual(
            name_results, {script_filename},
            'shed.find(name="{0}") should return script with name "{0}". Instead it returned '
            '{1}'.format(script_filename, name_results))

    def test_toss_removes(self):
        # Setup
        _, script_filename = self._make_named_temp_file()

        # Execute
        self.the_shed.toss(script=script_filename)

        # Assert
        self.assertTrue(not os.path.exists(os.path.join(self.home_dir.name, script_filename)))

    def assertResultsEqual(self, actual_results, expected_results, message):
        self.assertSetEqual(set(a['script'] for a in actual_results), expected_results, message)

    @staticmethod
    def _get_temp_file_name(script: tempfile.NamedTemporaryFile):
        _, tmp_filename = os.path.split(script.name)
        return tmp_filename

    def _make_named_temp_file(self, tags: collections.abc.Iterable=tuple(), invocation: str=None):
        script = tempfile.NamedTemporaryFile()
        self.the_shed.make(script.name, tags=tags, invocation=invocation)
        _, tmp_filename = os.path.split(script.name)
        return script.name, tmp_filename


if __name__ == '__main__':
    unittest.main()
