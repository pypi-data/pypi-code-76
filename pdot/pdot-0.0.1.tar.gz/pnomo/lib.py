import sys

class app():
    def __repr__(self):
        self.run()
        return 'efe'
    def __call__(self):
        self.run()
    def run(self):
        ON = True
        while ON:
            ans = input('tell me something, you moron... ')
            if ans == 'you suck':
                ON = False
                print('but you more!')
            elif ans == 'treasure':
                print('A&P<3')

def holi():
    x, y = input(), input()
    print(int(x) + int(y))

def walala():
    print(int(sys.argv[1]) + int(sys.argv[2]))

run = app()
def corre(): print(run)
print('lel')

#ned
