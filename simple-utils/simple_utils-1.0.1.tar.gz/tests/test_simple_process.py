import simple_utils

def test_retry():
    # 성공한 경우
    assert simple_utils.process.retry(2, 2, lambda x: x+1, 5) == 6 
    # 실패한 경우
    assert simple_utils.process.retry(1, 2, lambda x: x+y, 5) == None

