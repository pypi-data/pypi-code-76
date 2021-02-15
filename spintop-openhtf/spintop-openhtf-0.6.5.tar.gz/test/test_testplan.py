import pytest
try:
    import tornado
    TORNADO_AVAILABLE = True
except ImportError:
    TORNADO_AVAILABLE = False
    
from spintop_openhtf import TestPlan, PhaseResult
from openhtf import Measurement

A_TEST_PLAN_NAME = 'test-plan'
A_TEST_NAME = 'Test1'

@pytest.fixture()
def test_plan():
    return TestPlan(A_TEST_PLAN_NAME, store_result=False)

def test_simple_testcase(test_plan):
    
    @test_plan.testcase(A_TEST_NAME)
    @test_plan.measures(Measurement('hello').equals('world'))
    def test_1(test): # pylint: disable=unused-variable
        test.measurements.hello = 'world'
    
    assert test_plan.phase_group.main and test_plan.phase_group.main[0].name == A_TEST_NAME

    test_plan.no_trigger()
    result = test_plan.run_console(once=True)

    assert result, "Test should pass."
    print(result)

@pytest.mark.skipif(not TORNADO_AVAILABLE, reason="Requires the GUI extras [server]")
def test_no_trigger_and_run_with_gui(test_plan):
    test_plan.no_trigger()
    executed = []
    
    assert not executed
    
    @test_plan.testcase(A_TEST_NAME)
    def test_1(test): # pylint: disable=unused-variable
        executed.append(True)
    
    test_plan.run_once(launch_browser=False)
    
    assert executed
    
def test_custom_trigger(test_plan):
    executed = []
    
    assert not executed
    
    @test_plan.trigger('trigger')
    def test_trigger(test):
        executed.append(True)
    
    @test_plan.testcase(A_TEST_NAME)
    def test_1(test): # pylint: disable=unused-variable
        executed.append(True)
    
    test_plan.execute()
    
    assert len(executed) == 2
    
def test_setup_fn(test_plan):
    test_plan.no_trigger()
    executed = []
    
    assert not executed
    
    @test_plan.setup('fail-setup')
    def test_fail_setup(test):
        executed.append(True)
        return PhaseResult.STOP 
    
    @test_plan.testcase(A_TEST_NAME)
    def test_1(test): # pylint: disable=unused-variable
        executed.append(True)
    
    test_plan.execute()
    
    assert len(executed) == 1
    
def test_sub_sequence(test_plan):
    test_plan.no_trigger()
    executed = []
    
    def my_test(test):
        executed.append(True)
        
    test_plan.testcase('test1')(my_test) # 1
    subseq = test_plan.sub_sequence('subseq')
    subseq.testcase('test2')(my_test) # 2
    subseq.testcase('test3')(my_test) # 3
    
    test_plan.execute()
    assert len(executed) == 3
        

def test_run_console():
    plan = TestPlan('empty')

    @plan.testcase('Nothing')
    def test_something(test):
        pass

    plan.no_trigger()
    plan.run_console(once=True)
    
    
    
    