from helloworld import say_hello

def test_hello_world_no_params():
    assert say_hello() == "Hello, World!"

def test_hello_world_with_params():
    assert say_hello("Everyone") == "Hello, Everyone!"