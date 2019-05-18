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

    def test_take_returnsNamedScript(self):
        # Setup
        _, script_filename = self._make_named_temp_file()

        # Execute
        result = self.the_shed.take(script_filename)

        # Assert
        self.assertIsNotNone(result, 'shed.take should have returned a tool with script name "{}" but returned None '
                                     'instead.'.format(script_filename))
        self.assertEqual(script_filename, result.script, 'shed.take should have returned a tool with script name "{}" '
                                                         'but returned a script named "{}" '
                                                         'instead'.format(script_filename, result.script))

    def test_take_returnsNone_forNonexistentScript(self):
        # Setup
        bogus_filename = 'shouldnt_exist'

        # Execute
        result = self.the_shed.take(bogus_filename)

        # Assert
        self.assertIsNone(result, 'shed.take should have returned None for non-existent script "{}", but returned '
                                  '{} instead'.format(bogus_filename, repr(result)))

    def test_put_updatesExistingScript(self):
        # Setup
        _, script_filename = self._make_named_temp_file()
        tool = self.the_shed.take(script_filename)
        tags = ['test_tag']
        tool.tags = tags

        # Execute
        self.the_shed.put(tool)

        # Assert
        tool = self.the_shed.take(script_filename)
        self.assertSetEqual(set(tool.tags), set(tags), "shed.put should update tool {} to have tags {}, but instead "
                                                       "tags were {}".format(script_filename, tags, tool.tags))

    def test_put_updatesExistingText(self):
        # Setup
        _, script_filename = self._make_named_temp_file()
        tool = self.the_shed.take(script_filename)
        new_script = tempfile.NamedTemporaryFile()
        test_text = 'Test text for put update.'

        with open(new_script.name, 'w') as f:
            f.write(test_text)

        # Execute
        self.the_shed.put(tool, new_script.name)

        # Assert
        with open(os.path.join(self.home_dir.name, script_filename), 'r') as f:
            new_text = f.read()
        self.assertMultiLineEqual(new_text, test_text, 'Script text should have been {} but was {} '
                                                       'instead.'.format(repr(test_text), repr(new_text)))

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
