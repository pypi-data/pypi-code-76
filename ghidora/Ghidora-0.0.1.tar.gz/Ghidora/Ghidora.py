import functools as fp
import time

class Fibonacci:
  def __init__(self, fibonacciNumber):
    self.fibonacciNumber = fibonacciNumber
  def process(fibonacciNumber):
    fibonacciProcess = lambda fibonacciNumber: fp.reduce(lambda x, y: [x[1], x[0]+x[1]], range(fibonacciNumber), [0, 1])[0]
    print(fibonacciProcess(fibonacciNumber))
  def fibonacci(self):
    Fibonacci.process(self.fibonacciNumber-1)
  def fibonacciArray(self):
    fibonacciProcess = lambda fibonacciNumber: fp.reduce(lambda x, _: x+[x[-1]+x[-2]], range(fibonacciNumber-2), [0, 1])
    print(fibonacciProcess(self.fibonacciNumber))

class Exponent:
  def __init__(self, base):
    self.base = base
  def process(base, exponent):
    powerProcess = lambda base, exponent: fp.reduce(lambda x, y: [x[0], x[1]*base], range(exponent), [base, 1])[1]
    print(powerProcess(base, exponent))
  def power(self, exponent):
    Exponent.process(self.base, exponent)

class Factorial:
  def __init__(self, factorialNumber):
    self.factorialNumber = factorialNumber
  def process(factorialNumber):
    factorialProcess = lambda fibonacciNumber: fp.reduce(lambda x, y: [x[0]+1, x[1]*(x[0]+1)], range(factorialNumber-1), [1, 1])[1] 
    print(factorialProcess(factorialNumber))
  def factorial(self):
    Factorial.process(self.factorialNumber)

class NaturalLogarithm:
	def __init__(self):
		self.precision = 10000000000.0
	def process(precision,number):
		findNLogarithm = lambda number: precision * ((number ** (1/precision)) - 1)
		print(findNLogarithm(number))
	def natualLogarithm(self, number):
		NaturalLogarithm.process(self.precision, number)

class Logarithm:
	def __init__(self, base):
		self.base = base
		self.precision = 10000000000.0
	def process(precision, base, number):
		findLogarithm = lambda precision, base, number: (precision * ((number ** (1/precision)) - 1))/(precision * ((base ** (1/precision)) - 1))
		print(findLogarithm(precision, base, number))
	def logarithm(self, number):
		Logarithm.process(self.precision, self.base, number)

class upcoming:
  def __init__(self):
    pass

'''
number = 5555556
new = Fibonacci(number)
new.fibonacci()

base = 3
power = 27
new = Exponent(base)
new.power(power)

baseFactortial = 1000
new = Factorial(baseFactortial)
new.factorial()

new = NaturalLogarithm()
new.natualLogarithm(1000)

new = Logarithm(10)
new.logarithm(1000)
'''s