
import pandas as pd
from phylodeep.encoding import encode_into_summary_statistics, encode_into_most_recent
from phylodeep.model_load import model_scale_load_ffnn, model_load_cnn

from ete3 import Tree

SUMSTATS = 'FFNN_SUMSTATS'
FULL = 'CNN_FULL_TREE'

select_model_options = ['BD_vs_BDEI', 'BD_vs_BDSS']
prediction_method_options = ['CNN_FULL_TREE', 'FFNN_SUMSTATS']
param_model_options = ['BD', 'BDEI', 'BDSS']

BD = 'BD'
BDEI = 'BDEI'
BDSS = 'BDSS'
BD_vs_BDEI = 'BD_vs_BDEI'
BD_vs_BDSS = 'BD_vs_BDSS'


def read_tree(newick_tree):
    """ Tries all nwk formats and returns an ete3 Tree

    :param newick_tree: str, a tree in newick format
    :return: ete3.Tree
    """
    tree = None
    for f in (3, 2, 5, 0, 1, 4, 6, 7, 8, 9):
        try:
            tree = Tree(newick_tree, format=f)
            break
        except:
            continue
    if not tree:
        raise ValueError('Could not read the tree {}. Is it a valid newick?'.format(newick_tree))
    return tree


def read_tree_file(tree_path):
    with open(tree_path, 'r') as f:
        nwk = f.read().replace('\n', '').split(';')
    if not nwk:
        raise ValueError('Could not find any trees (in newick format) in the file {}.'.format(tree_path))
    if len(nwk) > 1:
        raise ValueError('There are more than 1 tree in the file {}. Now, we accept only one tree per inference.'.format(tree_path))
    return read_tree(nwk + ';')


def check_tree_size(tre):
    """
    Verifies whether input tree is of correct size and determines the tree size range for models to use
    :param tre: ete3.Tree
    :return: int, tree_size
    """
    if 49 < len(tre) < 200:
        tre_size = 'SMALL'
    elif 199 < len(tre) < 501:
        tre_size = 'LARGE'
    else:
        raise ValueError('Your input tree is of incorrect size (either smaller than 50 tips or larger than 500 tips.')

    return tre_size


def annotator(predict, mod):
    """
    annotates the pd.DataFrame containing predicted values
    :param predict: predicted values
    :type: pd.DataFrame
    :param mod: model under which the parameters were estimated
    :type: str
    :return:
    """

    if mod == "BD":
        predict.columns = ["R_naught", "Infectious_period"]
    elif mod == "BDEI":
        predict.columns = ["R_naught", "Infectious_period", "Incubation_period"]
    elif mod == "BDSS":
        predict.columns = ["R_naught", "Infectious_period", "X_transmission", "Fraction_superspreaders"]
    elif mod == "BD_vs_BDEI":
        predict.columns = ["Probability_BDEI", "Probability_BD"]
    elif mod == "BD_vs_BDSS":
        predict.columns = ["Probability_BD", "Probability_BDSS"]
    return predict


def rescaler(predict, rescale_f):
    """
    rescales the predictions back to the initial tree scale (e.g. days, weeks, years)
    :param predict: predicted values
    :type: pd.DataFrame
    :param rescale_f: rescale factor by which the initial tree was scaled
    :type: float
    :return:
    """

    for elt in predict.columns:
        if "period" in elt:
            predict[elt] = predict[elt]/rescale_f

    return predict


def modeldeep(tree_file, proba_sampling, model='BD_vs_BDEI', vector_representation='CNN_FULL_TREE'):
    """
    Provides model selection between selected models for given tree.
    :param tree_file: path to a file with dated trees (in newick format)
    :type tree_file: str
    :param proba_sampling: presumed sampling probability for all input trees, value between 0.01 and 1
    :type proba_sampling: float
    :param model: option to choose, you can choose either 'BD_vs_BDEI' (model selection between basic birth-death model
     with incomplete sampling) or 'BD_vs_BDSS' (model selection between BD and BD with 'superspreading' individuals).
    :type model: str
    :param vector_representation: option to choose between 'FFNN_SUMSTATS' to select a network trained on summary statistics
    or 'CNN_FULL_TREE' to select a network trained on full tree representation, by default, we use 'CNN FULL TREE'
    :type vector_representation: str
    :return: pd.df, predicted parameter values or model selection
    """
    # check options
    if proba_sampling > 1 or proba_sampling < 0.01:
        raise ValueError('Incorrect value of \'sampling probability\' parameter')
    if vector_representation not in prediction_method_options:
        raise ValueError('Incorrect value of \'prediction method\' option.')

    # read trees
    tree = read_tree_file(tree_file)

    # check tree size
    tree_size = check_tree_size(tree)

    # encode the trees
    if vector_representation == SUMSTATS:
        encoded_tree, rescale_factor = encode_into_summary_statistics(tree, proba_sampling)
    elif vector_representation == FULL:
        encoded_tree, rescale_factor = encode_into_most_recent(tree, proba_sampling)

    # load model
    if vector_representation == SUMSTATS:
        model, scaler = model_scale_load_ffnn(tree_size, model)
    elif vector_representation == FULL:
        model = model_load_cnn(tree_size, model)

    # predict values:
    if vector_representation == SUMSTATS:
        encoded_tree = scaler.transform(encoded_tree)
        predictions = pd.DataFrame(model.predict(encoded_tree))
    elif vector_representation == FULL:
        predictions = pd.DataFrame(model.predict(encoded_tree))

    # annotate predictions:
    predictions = annotator(predictions, model)
    # if inferred paramater values: rescale back the rates
    predictions = rescaler(predictions, rescale_factor)

    return predictions


def paramdeep(tree_file, proba_sampling, model='BD', vector_representation='CNN_FULL_TREE'):
    """
    Provides model selection between selected models for given tree.
    :param tree_file: path to a file with dated trees (in newick format)
    :type tree_file: str
    :param proba_sampling: presumed sampling probability for all input trees, value between 0.01 and 1
    :type proba_sampling: float
    :param model: option to choose, you can choose 'BD' (basic birth-death model with incomplete sampling BD), 'BDEI'
    (BD with exposed class) or 'BDSS' (BD with 'superspreading' individuals).
    :type model: str
    :param vector_representation: option to choose between 'FFNN_SUMSTATS' to select a network trained on summary
    statistics or 'CNN_FULL_TREE' to select a network trained on full tree representation, by default, we use
    'CNN_FULL_TREE'
    :type vector_representation: str
    :return: pd.df, predicted parameter values or model selection
    """
    # check options
    if proba_sampling > 1 or proba_sampling < 0.01:
        raise ValueError('Incorrect value of \'sampling probability\' parameter')
    if model not in param_model_options:
        raise ValueError('Incorrect value of \'model\' option.')
    if vector_representation not in prediction_method_options:
        raise ValueError('Incorrect value of \'prediction_method\' option.')

    # read trees
    tree = read_tree_file(tree_file)

    # check tree size
    tree_size = check_tree_size(tree)

    # encode the trees
    if vector_representation == SUMSTATS:
        encoded_tree, rescale_factor = encode_into_summary_statistics(tree, proba_sampling)
    elif vector_representation == FULL:
        encoded_tree, rescale_factor = encode_into_most_recent(tree, proba_sampling)

    # load model
    if vector_representation == SUMSTATS:
        model, scaler = model_scale_load_ffnn(tree_size, model)
    elif vector_representation == FULL:
        model = model_load_cnn(tree_size, model)

    # predict values:
    if vector_representation == SUMSTATS:
        encoded_tree = scaler.transform(encoded_tree)
        predictions = pd.DataFrame(model.predict(encoded_tree))
    elif vector_representation == FULL:
        predictions = pd.DataFrame(model.predict(encoded_tree))

    # annotate predictions:
    predictions = annotator(predictions, model)
    # if inferred paramater values: rescale back the rates
    predictions = rescaler(predictions, rescale_factor)
    return predictions


def main():
    """
    Entry point, calling :py:func:`phylodeep.phylodeep.paramdeep` or `phylodeep.phylodeep.modeldeep`  with command-line
     arguments.
    :return: void
    """
    import argparse

    parser = argparse.ArgumentParser(description="Ancestral character reconstruction and visualisation "
                                                 "for rooted phylogenetic trees.", prog='pastml')

    tree_group = parser.add_argument_group('tree-related arguments')
    tree_group.add_argument('-t', '--tree', help="input tree(s) in newick format (must be rooted).",
                            type=str, required=True)
    tree_group.add_argument('-p', '--proba_sampling', help="presumed sampling probability for removed tips. Must be "
                                                           "between 0.01 and 1",
                            type=float, required=True)

    prediction_group = parser.add_argument_group('neural-network-prediction arguments')
    prediction_group.add_argument('-s', '--selection', choices=[True, False], required=False, type=bool, default=False,
                                  help="If model selection is required, set this option to True, by default paramater"
                                       " inference is performed False.")
    prediction_group.add_argument('-m', '--model', choices=[BD, BDEI, BDSS, BD_vs_BDEI, BD_vs_BDSS],
                                  required=True, type=str, default=None,
                                  help="Choose one of the models to be inferred for the tree. For parameter inference,"
                                       " you can choose either BD (basic birth-death with incomplete sampling), "
                                       " BDEI (BD with exposed-infectious) or BDSS (BD with superspreading individuals)"
                                       ". For model selection you can choose either BD_vs_BDEI (selection between BD "
                                       "and BDEI) or BD_vs_BDSS (selection between BD and BDSS).")

    prediction_group.add_argument('-v', '--vector_representation', choices=[FULL, SUMSTATS], required=False, type=str,
                                  default=FULL,
                                  help="Choose neural networks: either FULL: CNN trained on full tree representation or"
                                       "SUMSTATS: FFNN trained on summary statistics. By default set to FULL.")

    params = parser.parse_args()

    if params[2]:
        params.pop(2)
        modeldeep(**vars(params))
    else:
        params.pop(2)
        paramdeep(**vars(params))


if '__main__' == __name__:
    main()
