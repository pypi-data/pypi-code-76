import os
import time

from openhtf.plugs.user_input import UserInput

from spintop_openhtf import TestPlan, conf, PhaseResult
from spintop_openhtf.util.markdown import markdown

# This defines the name of the testbench.
plan = TestPlan('empty')

@plan.testcase('Nothing')
def test_something(test):
    time.sleep(0.05)
    test.state['run_test'] = False

@plan.testcase('Skipped', run_if=lambda state: state['run_test'])
def test_something(test):
    pass

@plan.testcase('Fails')
def test_something(test):
    return PhaseResult.FAIL_AND_CONTINUE

@plan.testcase('Wait')
@plan.plug(user_input=UserInput)
def test_something(test, user_input):
    """MY incredibly long descriptionMY incredibly long descriptionMY incredibly long descriptionMY incredibly long descriptionMY incredibly long description

theresttheresttheresttheresttheresttheresttheresttheresttheresttheresttheresttheresttheresttheresttheresttheresttheresttheresttheresttheresttheresttheresttheresttheresttheresttheresttheresttheresttheresttherest
theresttheresttheresttheresttheresttheresttheresttheresttheresttheresttheresttheresttheresttheresttheresttheresttheresttheresttheresttheresttheresttheresttheresttherest

theresttheresttheresttheresttheresttheresttheresttheresttheresttheresttherest

    """
    user_input.prompt('Continue ?')

if __name__ == '__main__':
    plan.run()