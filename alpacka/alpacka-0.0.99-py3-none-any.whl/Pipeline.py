from alpacka.pipes.ncof_pipeline import ncof_pipeline
from alpacka.pipes.tfidf_pipeline import tfidf_pipeline

class Pipeline:
    def __init__(self, class_perspective = 1, num_words = None, verbose = True):
        self.ncof = ncof_pipeline(num_words=num_words, class_perspective= class_perspective, verbose= verbose)
        self.tfidf = tfidf_pipeline(num_words= num_words, class_perspective= class_perspective, verbose= verbose)


def main():
    pipe = Pipeline(class_perspective= 1, num_words= 10000)
    pipe.ncof.print_all_methods()
    pipe.tfidf.print_all_methods()
    return pipe
if __name__ == '__main__':

    pipe = main()
