"""Программа для замера скорости работы того или иного метода Python"""
import time
import sys

class decorattors:
    def clocker(func):
        """
        Так как декоратор может принимать один аргумент то ми берём и всовуваем в функцию вторую.

        Которая уже заберёт все аргументы функции.
        """

        def clock(*args):
            start_time = time.time()
            try:
                function = func(args)
            except:
                function = func()
            sys.stdout.write(f"[{time.time() - start_time}] {func.__name__}()")
        return clock
    def instruction(self):
        sys.stdout.write("Привет, меня зовут Иван. Ето моя первая библиотека и пока что она\nимеет только функцию @clocker.\nКак она используеться?\nПеред функцией пишеш @decorators.clocker")
    def __call__(self):
        return instruction()