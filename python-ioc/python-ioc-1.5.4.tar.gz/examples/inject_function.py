import ioc


ioc.provide('TheRequirement', "Hello world!")


@ioc.inject('value', 'TheRequirement')
def f(value):
    print(value)
