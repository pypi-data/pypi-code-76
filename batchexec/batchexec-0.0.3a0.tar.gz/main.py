"""Execute app from config.json options with its arguments on all specified files in given input directory,
and put the result into the output directory maintaining its structure."""
import batchexec


if __name__ == '__main__':
    batch_executer = batchexec.UniversalBatchExecuter()

    batch_executer.run()
