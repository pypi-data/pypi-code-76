import os,sys,json
import shutil
sys.path.insert(0,os.getcwd())
import argparse
from build_data.build_corpus import DataBuild
from build_data.build_data import generate_model_data

# from lstm_crf import predict

def main():
    base_data = os.path.join(os.getcwd(),'base_data')
    os.makedirs(base_data,exist_ok=True)
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", 
    default=base_data,
    help="enter path for corpus")
    parser.add_argument("--raw_data_path", help="enter file name")
    parser.add_argument("--glove_path", help="enter glove file path")
    parser.add_argument("--operation", help="operation")
    parser.add_argument("--batch_type", default='hierarchical_labels', help="batch starting_spans or hirechical")
    parser.add_argument("--clean" , default=False ,help="test ?", action='store_true')
    args = parser.parse_args()

    def call_builds():
        data_build = DataBuild()   
        data_build.read_file(args.raw_data_path)
        data_build.build_data(args.data_dir)
        generate_model_data(data_prefix='p1_all', train_file_path=args.data_dir,
        batch_type=args.batch_type,glove_path=args.glove_path)
        sample = {'operation_type':args.batch_type}
        with open('operation_type.json','w') as fp:
            json.dump(sample, fp)
    if(args.operation=='build_data'):   
        if(args.clean):
            shutil.rmtree(base_data)
        call_builds()
    if(args.operation=='train'):
        from lstm_crf.train import main as train_main
        train_main(data_prefix='p1_all', train_file_path=args.data_dir)
        print('tran ..........')

if __name__ == "__main__":
    sys.exit(main())
