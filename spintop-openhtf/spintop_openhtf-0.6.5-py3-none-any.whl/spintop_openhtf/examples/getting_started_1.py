import os

from openhtf.plugs.user_input import UserInput

from spintop_openhtf import TestPlan, conf
from spintop_openhtf.util.markdown import markdown

# This defines the name of the testbench.
plan = TestPlan('examples.getting_started', store_location='here')

HERE = os.path.abspath(os.path.dirname(__file__))

FORM_LAYOUT = {
    'schema':{
        'title': "First and Last Name",
        'type': "object",
        'required': ["firstname", "lastname"],
        'properties': {
            'firstname': {
                'type': "string", 
                'title': "First Name"
            },
            'lastname': {
                'type': "string", 
                'title': "Last Name"
            },
            'radio_choice': {
                'type': "string", 
                'default': "default",
                'title': "Radio Choice"
            },
            'checkbox': {
                'type': "boolean", 
                'default': False,
                'title': "Checkbox"
            },
            'dropdown': {
                'type': "string", 
                'default': "default",
                'title': "Dropdown"
            },
        }
    },
    'layout':[
        {
            "type": "help",
            "helpvalue": markdown("""
#Welcome to the Getting Started !

##Introduction

This test simply showcases the custom forms by asking information to the tester and then showing it to him.

##Image showcase

<img src="%s" width="200px" />

""" % plan.image_url(os.path.join(HERE, 'spinhub-app-icon.png'))
            )
        },
        "firstname",
        "lastname",
        {
            "key": "radio_choice",
            "type": "radiobuttons",
            "titleMap": [
                { "value": "One", "name": "One" },
                { "value": "Two", "name": "Two" }
            ]
        },
        "checkbox",
        {
            "key": "dropdown",
            "type": "select",
            "titleMap": [
                { "value": "One", "name": "One" },
                { "value": "Two", "name": "Two" }
            ]
        }
    ]
}

"""Custom Plugs"""

class GreetPlug(UserInput):
    def prompt_tester_information(self):
        self.__response = self.prompt_form(FORM_LAYOUT)
        return self.__response
    
    def greet_tester(self):
        try:
            self.prompt("""
Hello {firstname} {lastname} ! 

You chose "{radio_choice}" from the radio buttons.
You chose "{dropdown}" from the dropdown menu.

""".format(**self.__response)
            )
        except AttributeError:
            raise Exception("Cannot greet tester before prompt_information")

""" Test Plan """

@plan.trigger('Hello-World')
@plan.plug(greet=GreetPlug)
def hello_world(test, greet):
    """Says Hello World !
    
# Hello World Test
    
Welcome to the **hello world** test.
    """
    response = greet.prompt_tester_information()
    test.dut_id = response['firstname']
    
@plan.testcase('Greet the tester')
@plan.plug(greet=GreetPlug)
def greet_tester(test, greet):
    greet.greet_tester()

if __name__ == '__main__':
    plan.run()