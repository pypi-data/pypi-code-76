"""
This module makes it possible to batch execute almost every program that runs from command line 
on files in input directory and outputs those into output directory (include directory structure). 
Settings are taken from config.json file. In the future there will be new features added.
"""
import batchexec


if __name__ == '__main__':
    batch_executer = batchexec.UniversalBatchExecuter()

    batch_executer.run()
