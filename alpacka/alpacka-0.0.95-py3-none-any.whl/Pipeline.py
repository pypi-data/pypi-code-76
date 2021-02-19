from alpacka.pipes.ncof_pipeline import ncof_pipeline
from alpacka.pipes.tfidf_pipeline import tfidf_pipeline

class Pipeline:
    def __init__(self, class_perspective = 1, num_words = None):
        self.ncof = ncof_pipeline(num_words, class_perspective)
        self.tfidf = tfidf_pipeline()


def main():
    pipe = Pipeline(class_perspective= 1, num_words= 10000)
    pipe.ncof.print_all_methods()
    pipe.tfidf.print_all_methods()

if __name__ == '__main__':

    main()
