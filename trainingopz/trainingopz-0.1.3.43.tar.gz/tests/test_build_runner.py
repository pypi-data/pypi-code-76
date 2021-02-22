# Modifications © 2020 Hashmap, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import pathlib
import shutil
import unittest

from trainingopz.builders_and_generators.director import Director


@unittest.skip
class TestBuildRunner(unittest.TestCase):
    """
    Test Builder Class
    """

    def setUp(self) -> None:

        self.__path = pathlib.Path(__file__).parent.absolute()
        self._builder = Director(path=os.path.join(self.__path, 'ml_qookeys'))

    def tearDown(self) -> None:
        del self._builder

    @unittest.skip('for now')
    def test_flow_is_present(self):

        self.assertTrue(self._builder.check_if_flow_is_present())

    @unittest.skip('for now')
    def test_flow_is_not_present(self):
        #Copy and remove target file
        _to_remove = os.path.join(self.__path, 'ml_qookeys/workflows/flows.yml')
        _copy_to = os.path.join(self.__path, 'ml_qookeys/workflows/flows_bup.yml')
        shutil.copyfile(_to_remove, _copy_to)
        os.remove(_to_remove)

        # Test existence of non-existent file
        self.assertFalse(self._builder.check_if_flow_is_present())

        # Repair existence of file
        shutil.copyfile(_copy_to, _to_remove)
        os.remove(_copy_to)

    @unittest.skip('for now')
    def test_read_flows(self):
        flows = self._builder.read_flows()

        self.assertIsInstance(flows, dict)

    @unittest.skip('for now')
    def test_read_flows_fail(self):

        # Copy and remove target file for backup
        _to_remove = os.path.join(self.__path, 'ml_qookeys/workflows/flows.yml')
        _copy_to = os.path.join(self.__path, 'ml_qookeys/workflows/flows_bup.yml')
        shutil.copyfile(_to_remove, _copy_to)
        os.remove(_to_remove)

        # Create temp empty file
        with open(_to_remove, 'w') as fh:
            fh.write('')

        try:
            with self.assertRaises(ValueError):
                self._builder.read_flows()
        finally:
            # Remove temp file
            os.remove(_to_remove)

            # Repair existence of file
            shutil.copyfile(_copy_to, _to_remove)
            os.remove(_copy_to)

    @unittest.skip('Not implemented')
    def test_validate_flows_fail(self):

        # Need to create scenarios of bad flows and test against them
        self.assertTrue(True, False)

    @unittest.skip('Not implemented')
    def test_remove_inactive_pipelines(self):

        # Need version with and without inactive and make sure inactive are removed,
        # but nothing is done when all are active.
        self.assertEqual(True, False)

    @unittest.skip('Not implemented')
    def test_missing_pipelines(self):
        self.assertEqual(True, False)

    @unittest.skip('Not implemented')
    def test_pipelines_do_not_exist(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
