"""Library 'list_resources' method test module"""

from .test_library import TestLibrary


class TestLibraryListResources(TestLibrary):
    """Test class for library 'list_resources' method"""

    def test_str_arg_type_invalid(self):
        """Test provided built-in Python type object instances trigger a TypeError"""

        for type_ in {int, float, str, tuple, set, list, dict}:
            type_instance = type_()

            with self.assertRaises(TypeError) as ctx:
                self.client.list_resources(type_instance)

            error_msg = ctx.exception.__str__()
            print(error_msg)

            self.assertEqual(error_msg,
                             f'Resource argument expected, got {type(type_instance).__name__}')
