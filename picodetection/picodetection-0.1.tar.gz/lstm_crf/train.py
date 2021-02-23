import os, sys
from lstm_crf.model.data_utils import CoNLLDataset
from lstm_crf.model.ner_model import NERModel
from lstm_crf.model.base_model import BaseModel
from lstm_crf.model.config import Config
print(os.getcwd())

def main(data_prefix = None,train_file_path=None,batch_type=None):
    # create instance of config
    config = Config(train_file_path=train_file_path)
    # build model
    model = NERModel(config)
    model.build()
    #model.restore_session("results/crf/model.weights/") # optional, restore weights
    # model.reinitialize_weights("proj")
    print("model loaded........")
    if data_prefix:
      cwd = train_file_path
      config.filename_dev   = os.path.join(cwd, 'data', data_prefix + '_' + os.path.basename(config.filename_dev))
      config.filename_test  = os.path.join(cwd, 'data', data_prefix + '_' + os.path.basename(config.filename_test))
      config.filename_train = os.path.join(cwd, 'data', data_prefix + '_' + os.path.basename(config.filename_train))

    # create datasets
    dev   = CoNLLDataset(config.filename_dev, config.processing_word,
                         config.processing_tag, config.max_iter)
    train = CoNLLDataset(config.filename_train, config.processing_word,
                         config.processing_tag, config.max_iter)

    # train model
    model.train(train, dev)

if __name__ == "__main__":
  try:
    data_prefix = sys.argv[1]
  except IndexError:
    data_prefix = None
  main(data_prefix)
