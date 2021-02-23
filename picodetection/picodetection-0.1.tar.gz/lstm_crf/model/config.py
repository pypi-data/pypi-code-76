import os
from .general_utils import get_logger
from .data_utils import get_trimmed_glove_vectors, load_vocab, \
        get_processing_word

class Config():
    def __init__(self, load=True,train_file_path='',glove_path=''):
        """Initialize hyperparameters and load vocabs

        Args:
            load_embeddings: (bool) if True, load embeddings into
                np array, else None

        """
        # directory for training outputs
        if not os.path.exists(self.dir_output):
            os.makedirs(self.dir_output)
        os.makedirs(os.path.join(train_file_path,'data'),exist_ok=True)
        # create instance of logger
        self.logger = get_logger(self.path_log)
        dim_word = 200
        self.filename_glove = os.path.join(glove_path, "glove.6B/glove.6B.{}d.txt".format(dim_word))
        print(self.filename_glove)
        #change to PubMed
        #filename_glove = os.path.join(cwd, "../embeddings/PubMed-w2v.txt")

        # trimmed embeddings (created from glove_filename with build_data.py)
        self.filename_trimmed = os.path.join(train_file_path, "data/embeddings.{}d.trimmed.npz".format(dim_word))
        self.use_pretrained = True

        # dataset
        self.filename_dev = os.path.join(train_file_path,   "data/dev.txt")
        self.filename_test = os.path.join(train_file_path,  "data/gold.txt")
        self.filename_train = os.path.join(train_file_path, "data/train.txt")

        #filename_dev = filename_test = filename_train = "data/test.txt" # test

        self.max_iter = None # if not None, max number of examples in Dataset

        # vocab (created from dataset with build_data.py)
        self.filename_words = os.path.join(train_file_path, "data/words.txt")
        self.filename_tags = os.path.join(train_file_path, "data/tags.txt")
        self.filename_chars = os.path.join(train_file_path, "data/chars.txt")
        # load if requested (default)
        if load:
            self.load()


    def load(self):
        """Loads vocabulary, processing functions and embeddings

        Supposes that build_data.py has been run successfully and that
        the corresponding files have been created (vocab and trimmed GloVe
        vectors)

        """
        print(self.filename_words)
        # 1. vocabulary
        self.vocab_words = load_vocab(self.filename_words)
        self.vocab_tags  = load_vocab(self.filename_tags)
        self.vocab_chars = load_vocab(self.filename_chars)

        self.nwords     = len(self.vocab_words)
        self.nchars     = len(self.vocab_chars)
        self.ntags      = len(self.vocab_tags)

        # 2. get processing functions that map str -> id
        self.processing_word = get_processing_word(self.vocab_words,
                self.vocab_chars, lowercase=True, chars=self.use_chars)
        self.processing_tag  = get_processing_word(self.vocab_tags,
                lowercase=False, allow_unk=False)

        # 3. get pre-trained embeddings
        self.embeddings = (get_trimmed_glove_vectors(self.filename_trimmed)
                if self.use_pretrained else None)

    cwd = os.getcwd()
    #cwd = os.path.join(cwd,"models/lstm_crf")
    # general config
    dir_output = os.path.join(cwd, "results/test/")
    dir_model  = os.path.join(dir_output, "model.weights/")
    path_log   = os.path.join(dir_output, "log.txt")
 
    # embeddings
    dim_word = 200
    dim_char = 100

    # glove files


    # training
    train_embeddings = False
    nepochs          = 20
    dropout          = 0.7
    batch_size       = 20
    lr_method        = "adam"
    lr               = 0.001
    lr_decay         = 0.9
    clip             = -1 # if negative, no clipping
    nepoch_no_imprv  = 10

    # model hyperparameters
    hidden_size_char = 100 # lstm on chars
    hidden_size_lstm = 200 # lstm on word embeddings

    # NOTE: if both chars and crf, only 1.6x slower on GPU
    use_crf = True # if crf, training is 1.7x slower on CPU
    use_chars = True # if char embedding, training is 3.5x slower on CPU
