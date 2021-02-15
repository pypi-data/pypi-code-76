import os

from openhtf.plugs.user_input import UserInput
from openhtf import conf

from spintop_openhtf import TestPlan

""" Test Plan """

plan = TestPlan('examples.spintop_integration')

@plan.testcase('Hello-World')
@plan.plug(prompts=UserInput)
def hello_world(test, prompts):
    """Says Hello World!"""
    test.logger.info('Hello World')

if __name__ == '__main__':
    plan.enable_spintop()
    conf.load(spintop_org_id='tackv')
    plan.run()
