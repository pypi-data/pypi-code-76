""" This is the module-level summary of the hello_world test.
"""

import os
import time
import random

from spintop_openhtf import TestPlan, PhaseResult

import openhtf as htf

from openhtf.plugs.user_input import UserInput, PromptType, SecondaryOptionOccured
from openhtf.util import conf

""" Test Plan """

plan = TestPlan('examples.hello_world')
# plan.define_top_level_component('nets.yml')

HERE = os.path.abspath(os.path.dirname(__file__))

FORM_LAYOUT = {
    'schema':{
        'title': "Todo",
        'type': "object",
        'required': [],
        'properties': {
            'title': {
                'type': "string", 
                'title': "Title"
            },
            'done': {'type': "boolean", 'title': "Done?", 'default': False}
        }
    },
    'layout':[
        "done",
        {
            'key': "title",
            'type': "section",
        }
    ]
}

spinsuite_image_url = plan.file_provider.create_url(os.path.join(HERE, 'spinhub-app-icon.png'))

@plan.testcase('Hello-World')
@htf.plugs.plug(prompts=UserInput)
@htf.PhaseOptions(requires_state=True)
def hello_world(state, prompts):
    """Says Hello World !
    
# Hello World Test
    
Welcome to the **hello world** test.
    """
    try:
        prompts.prompt_form(FORM_LAYOUT, prompt_type=PromptType.PASS_FAIL)
        prompts.prompt('Cancel', prompt_type=PromptType.OKAY_CANCEL)
        prompts.prompt('PASS', prompt_type=PromptType.PASS_FAIL)
    except SecondaryOptionOccured:
        return PhaseResult.FAIL_AND_CONTINUE 
        
    state.logger.info('Hello World')
    prompts.prompt("""
# {url}

This is **Awesome**

Please tell me more.
![My-Image]({url})
                    """.format(url=spinsuite_image_url))


@plan.testcase('Hello-World-2')
@htf.plugs.plug(prompts=UserInput)
def hello_world(test, prompts):
    """Says Hello World 2 !"""
    test.logger.info('Hello World 2')
    test.state['skip'] = True

sub_group = plan.sub_sequence('sub-group')

@sub_group.testcase('sub Hello', run_if=lambda state: not state.get('skip', False))
def hello_world(test):
    """Says Sub hello."""
    test.logger.info('Sub hello')

@sub_group.teardown('sub cleanup')
def hello_world(test):
    """Says Sub cleanup."""
    test.logger.info('Sub cleanup')
    
@plan.teardown('cleanup')
def cleanup(test):
    """Says Cleaned up."""
    test.logger.info('Cleaned up.')

if __name__ == '__main__':
    plan.run()




