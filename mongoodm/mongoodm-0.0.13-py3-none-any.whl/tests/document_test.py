import unittest
import mongoodm

DEFAULT_SAVED_OBJ = {}

class TestDocument(unittest.TestCase):
    def setUp(self):
        self.db = mongoodm.MongoODM(provider="mongomock")
        class TestUser(self.db.Document):
            username = ""
            email = ""
        
        self.TestUser = TestUser

    def test_save_attribute(self):
        user = self.TestUser()
        new_username = "new_username"
        new_password = "averyunsecurepassword"
        user.username = new_username
        user.password = new_password
        pass

    def test_unsaved_attributes(self):
        user = self.TestUser()
        new_username = "new_username"
        new_password = "averyunsecurepassword"
        self.assertDictEqual(DEFAULT_SAVED_OBJ, user._unsavedItems)

        user.username = new_username
        user.password = new_password

        self.assertIn("username", user._unsavedItems)
        self.assertIn("password", user._unsavedItems)

    def test_unsaved_items(self):
        user = self.TestUser()
        new_username = "new_username"
        new_password = "averyunsecurepassword"
        self.assertDictEqual(DEFAULT_SAVED_OBJ, user._unsavedItems)

        user["username"] = new_username
        user["password"] = new_password

        self.assertIn("username", user._unsavedItems)
        self.assertIn("password", user._unsavedItems)

    def test_dictionary_functionality(self):
        user = self.TestUser()
        updates = {
            "foo": "bar",
            "baz": "bounty"
        }

        user.foo = "Macro"
        self.assertTrue(user.save(), "Saving to the DB was successful")

        user_first_state = {'id': user.id, 'foo': 'Macro'}

        self.assertDictEqual(DEFAULT_SAVED_OBJ, user._unsavedItems)
        self.assertDictEqual(user_first_state, dict(user))

        user.update(updates)
        self.assertDictEqual({**user_first_state, **updates}, dict(user))
        assert "baz" in user, "Couldn't find key baz in {user}"
        assert user["baz"] == updates["baz"], "'baz' not accessible via subscriptable methods"
        assert user.baz == updates["baz"], "'baz' not accessible via an attribute"



    def test_can_saved(self):
        pass

