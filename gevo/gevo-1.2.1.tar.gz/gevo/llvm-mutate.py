import sys
import subprocess
import inspect
import os

import gevo
from gevo._llvm import __llvm_version__

os.path.dirname(inspect.getfile(gevo))
LLVM_MUTATE_LIBRARY_PATH=f'{os.path.dirname(inspect.getfile(gevo))}/Mutate.so.{__llvm_version__}'

def invoke_llvm_mutate(input_encstr, arguments):
    base_opt_args = [f'opt-{__llvm_version__}', '-load', LLVM_MUTATE_LIBRARY_PATH]

    opt_proc = subprocess.Popen(
        base_opt_args.extend(arguments),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE )
    bytestr_out, bytestr_err = opt_proc.communicate(input=input_encstr)
    return opt_proc.returncode, bytestr_out, bytestr_err

def decode_w_llvmdis(input_bytestr):
    llvmdis_proc = subprocess.Popen(
        [ f'llvm-dis-{__llvm_version__}'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE )
    llvmdis_stdout, llvmdis_stderr = llvmdis_proc.communicate(input=input_bytestr)
    if llvmdis_proc.returncode != 0:
        print(f"llvm-mutate: llc error in \"{' '.join(opt_proc.args)} | {' '.join(llvmdis_proc.args)}\"")
        print(llvmdis_stderr.decode())
        sys.exit(-1)

    print(llvmdis_stdout.decode(), file=args.output_file, end='')
