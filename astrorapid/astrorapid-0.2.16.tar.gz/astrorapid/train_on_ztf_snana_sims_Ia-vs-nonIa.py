import os
import astrorapid.get_training_data
import astrorapid.get_custom_data
from astrorapid.custom_classifier import create_custom_classifier


def main():
    """ Train Neural Network classifier """

    script_dir = os.path.dirname(os.path.abspath(__file__))

    create_custom_classifier(get_data_func=astrorapid.get_training_data.get_data_from_snana_fits,
                             data_dir=os.path.join(script_dir, '..', 'data/ZTF_20190512'),
                             class_nums=(1, 2, 12, 14, 3, 13, 41, 43, 51, 60, 64),
                             class_name_map={1: 'SNIa', 2: 'CC', 12: 'CC', 14: 'CC', 3: 'CC', 13: 'CC', 41: 'SNIa', 43: 'SNIa', 51: 'Other', 60: 'Other', 61: 'PISN', 62: 'ILOT', 63: 'CART', 64: 'Other', 70: 'AGN'},
                             reread_data=True,
                             contextual_info=('redshift',),
                             passbands=('g', 'r'),
                             retrain_network=False,
                             train_epochs=100,
                             zcut=0.5,
                             bcut=True,
                             ignore_classes=(61, 62, 63, 70),
                             nprocesses=1,
                             nchunks=10000,
                             otherchange='Ia_CC_Other',
                             training_set_dir=os.path.join(script_dir, '..', 'training_set_files'),
                             save_dir=os.path.join(script_dir, '..', 'data/saved_light_curves/other'),
                             fig_dir=os.path.join(script_dir, '..', 'training_set_files', 'Figures', 'Ia-Classifier-ZTF_with_redshift_2LSTM100_w_dropout0.0_epochs100'),
                             plot=True
                             )


if __name__ == '__main__':
    main()
