from tests.helpers.testbase import TestBase
from cerami.request.search_attribute import (
    UpdateExpressionAttribute,
    UpdateAction)
from cerami.model import Model
from cerami.datatype import String

class FakeModel(Model):
    test = String()
    test2 = String()

class TestUpdateExpressionAttribute(TestBase):
    def setUp(self):
        self.attribute = UpdateExpressionAttribute()

    def test_add_new_action(self):
        """it adds a new key of the action to self.value dict"""

    def test_add(self):
        """it adds the expression to the array"""
        expression = FakeModel.test == 'test'
        update_action = UpdateAction('SET', expression)
        self.attribute.add(update_action)
        assert self.attribute.value['SET'] == [expression]

    def test_add_appends(self):
        """it appends to the existing value key"""
        expression1 = FakeModel.test == 'test'
        expression2 = FakeModel.test2 == 'test2'
        update_action1 = UpdateAction('SET', expression1)
        update_action2 = UpdateAction('SET', expression2)
        self.attribute.add(update_action1)
        self.attribute.add(update_action2)
        assert self.attribute.value['SET'] == [expression1, expression2]

    def test_build(self):
        """it returns all group actions comma separated"""
        self.attribute.value = {
            'SET': [
                'fakeExpression1',
                'fakeExpression2'],
            'REMOVE': [
                'fakeExpression3']}
        expected = 'SET fakeExpression1, fakeExpression2 REMOVE fakeExpression3'
        assert self.attribute.build() == expected

