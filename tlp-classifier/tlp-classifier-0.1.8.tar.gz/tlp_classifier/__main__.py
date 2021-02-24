import sys, getopt, json
from .problem_set import Problem_set
from .file_help import import_data_set, store, store_json
from .classifier import classify
from .generator import generate
from .complexity import Complexity, complexity_name
from .api import get_problem

def classifyAndStore(min_degree, max_degree):
    problems,relaxations,restrictions = import_data_set(min_degree,max_degree,Problem_set.Unclassified)
    classify(problems,relaxations,restrictions, min_degree, max_degree)

    store(min_degree,max_degree,(problems,relaxations,restrictions),Problem_set.Classified)

    json_dict = dict()
    for complexity in Complexity:
        classifiedSubset = [x.to_tuple() for x in problems if x.get_complexity() == complexity]
        print(complexity_name[complexity] + " : " + str(len(classifiedSubset)), " problems")
        json_dict[complexity_name[complexity]] = classifiedSubset

    store_json(min_degree, max_degree, json_dict)

def generateAndStore(min_degree, max_degree):
    p = generate(min_degree,max_degree)
    store(min_degree,max_degree,p,Problem_set.Unclassified)

def usage():
    print('python -m tlp-classifier classify/generate -w <whitedegree> -b <blackdegree>')

def main(argv):
    white_degree = -1
    black_degree = -1
    s = False
    try:
        command = argv[0]
        opts, args = getopt.getopt(argv[1:],"hw:b:",["wdegree=","bdegree="])
    except getopt.GetoptError:
        usage()
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-w", "--wdegree"):
            try :
                white_degree = int(arg)
            except ValueError:
                print("The white degree is not an int")
                sys.exit(1)
        elif opt in ("-b", "--bdegree"):
            try :
                black_degree = int(arg)
            except ValueError:
                print("The black degree is not an int")
                sys.exit(1)

    if (white_degree <= 1 or black_degree <= 1):
        print("A degree must be superior or equal to 2")
        sys.exit(1)
        
    min_degree = min([white_degree,black_degree])
    max_degree = max([white_degree,black_degree])

    if command == 'classify':
        classifyAndStore(min_degree, max_degree)
    elif command == 'generate':
        generateAndStore(min_degree, max_degree)
    else:
        usage()
        sys.exit(1)

if __name__ == "__main__":
   main(sys.argv[1:])
