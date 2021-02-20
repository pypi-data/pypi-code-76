from SidekickAI.Modules import test as moduletest
from SidekickAI.Data import test as datatest
from SidekickAI.Utilities import test as utilitiestest
import time, os

# Class for printing colors and bold
class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

if __name__ == "__main__":
    # Run all tests
    print(color.BOLD + "|RUNNING FULL SIDEKICK AI TESTS|" + color.END)
    start_time = time.time()
    total, passed, skipped, failed, errors = 0, 0, 0, 0, 0
    print(color.BOLD + "|TESTING MODULES|" + color.END)
    test_total, test_passed, test_skipped, test_failed, test_errors = moduletest.test()
    total, passed, skipped, failed, errors = total + test_total, passed + test_passed, skipped + test_skipped, failed + test_failed, errors + test_errors
    print(color.BOLD + "|TESTING DATA|" + color.END)
    test_total, test_passed, test_skipped, test_failed, test_errors = datatest.test()
    total, passed, skipped, failed, errors = total + test_total, passed + test_passed, skipped + test_skipped, failed + test_failed, errors + test_errors
    print(color.BOLD + "|TESTING UTILITIES|" + color.END)
    test_total, test_passed, test_skipped, test_failed, test_errors = utilitiestest.test()
    total, passed, skipped, failed, errors = total + test_total, passed + test_passed, skipped + test_skipped, failed + test_failed, errors + test_errors

    rows, columns = os.popen('stty size', 'r').read().split()
    print(color.BOLD + ("_" * int(columns)) + color.END)
    print(color.BOLD + "Full Tests Completed in " + str(round(time.time() - start_time, 2)) + "s" + color.END)
    print(color.BOLD + str(total) + color.END + " Ran ")
    print(color.GREEN + color.BOLD + str(passed) + color.END + color.GREEN + " Passed ")
    print(color.YELLOW + color.BOLD + str(skipped) + color.END + color.YELLOW + " Skipped ")
    print(color.RED + color.BOLD + str(failed) + color.END + color.RED + " Failed ")
    print(color.RED + color.BOLD + str(errors) + color.END + color.RED + " Errors")