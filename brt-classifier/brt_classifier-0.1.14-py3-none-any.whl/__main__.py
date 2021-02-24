import sys
from .classify import classify
from .generateProblems import generate
from .statistics import printStatistics
from .getProblem import getProblem, getProblems

if __name__ == "__main__":
  command = sys.argv[1]
  args = sys.argv[2:]

  if command == 'generate':
    generate(int(args[0]))
  elif command == 'classify':
    classify(args[0], len(args) > 1 and (args[1] == "--write" or args[1] == "-w"))
  elif command == 'statistics':
    printStatistics(args[0])
  elif command == 'find':
    problem = getProblem(['222', '221', '121', '212'])
    print(problem)
  elif command == 'finds':
    problem = getProblems([['111'], ['222', '221'], ['222', '221', '121'], ['222', '221', '121', '212'], ['222', '221', '121', '212', '211'], ['222', '221', '121', '212', '211', '111'], ['222', '221', '121', '212', '111'], ['222', '221', '121', '211'], ['222', '221', '121', '211', '111'], ['222', '221', '121', '111'], ['222', '221', '212'], ['222', '221', '212', '211'], ['222', '221', '212', '111'], ['222', '221', '211'], ['222', '221', '211', '111'], ['222', '221', '111'], ['222', '121'], ['222', '121', '212'], ['222', '121', '212', '211'], ['222', '121', '212', '111'], ['222', '121', '211'], ['222', '121', '111'], ['222', '212'], ['222', '212', '211'], ['222', '211'], ['222', '111'], ['221'], ['221', '121'], ['221', '121', '212'], ['221', '121', '212', '211'], ['221', '121', '211'], ['221', '212'], ['221', '211'], ['121'], ['121', '212']], 2)
    print(problem)
  else:
    print('The first argument needs to be the command. One of "generate", "classify", "statistics", "find"')
