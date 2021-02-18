# Loading Animator

import time
import sys
import threading


class Loading:

    LOAD_FRAMES = [
        "[      ]",
        "[=     ]",
        "[==    ]",
        "[ ==   ]",
        "[  ==  ]",
        "[   == ]",
        "[    ==]",
        "[     =]",
    ]

    def __init__(self, input_str, init_retcode=-1, input_prestr=""):
        self.instr = input_str
        self.prestr = input_prestr
        self.retcode = init_retcode
        self.anim_done = False
        t = threading.Thread(target=self.display)
        t.start()

    def display(self):
        # Replace tabs with 8 spaces in prestr
        self.prestr = self.prestr.replace('\t', 8 * ' ')
        time.sleep(0.1)

        while self.retcode == -1:
            for l in self.LOAD_FRAMES:
                if self.retcode != -1:
                    break
                sys.stdout.write((len(self.LOAD_FRAMES[0]) + len(self.instr + self.prestr) + 1) * "\b")
                sys.stdout.write(self.prestr + l + " " + self.instr)
                sys.stdout.flush()
                time.sleep(0.1)
        if self.retcode == 0:
            sys.stdout.write((len(self.LOAD_FRAMES[0]) + len(self.prestr + self.instr) + 1) * "\b")
            sys.stdout.flush()
            print(self.prestr + "[ \033[92m OK \033[0m ]" + " " + self.instr)
        if self.retcode > 0:
            sys.stdout.write((len(self.LOAD_FRAMES[0]) + len(self.prestr + self.instr) + 1) * "\b")
            sys.stdout.flush()
            print(self.prestr + "[\033[91m FAIL \033[0m]" + " " + self.instr + " --> return code " + str(self.retcode))
        if self.retcode == -2:
            sys.stdout.write((len(self.LOAD_FRAMES[0]) + len(self.prestr + self.instr) + 1) * "\b")
            sys.stdout.flush()
            print(self.prestr + "[ \033[93m >> \033[0m ]" + " " + self.instr)
        if self.retcode == -3:
            sys.stdout.write((len(self.LOAD_FRAMES[0]) + len(self.prestr + self.instr) + 1) * "\b")
            sys.stdout.flush()
            print(self.prestr + "[ \033[93m ?? \033[0m ]" + " " + self.instr)
        self.anim_done = True

    def chain(self, new_instr, new_prestr="", end_rcode=0):
        # Terminate old thread
        self.retcode = end_rcode
        while not self.anim_done:
            time.sleep(0.1)

        # Start new thread
        self.anim_done = False
        self.instr = new_instr
        self.prestr = new_prestr
        self.retcode = -1
        t = threading.Thread(target=self.display)
        t.start()

    def end(self, rcode):
        self.retcode = rcode
        while not self.anim_done:
            time.sleep(0.1)
