class Person:
  def __init__(self):
    self.id = 1

  @property
  def a(self):
    return self.id

  @property
  def b(self):
    return 2

  @a.setter  # 此处 a, 下面 def 又是 a, 冗余
  def a(self, n):
    self.id += n

mulan = Person()
print(mulan.a + mulan.b)
mulan.a = 3
print(mulan.a)