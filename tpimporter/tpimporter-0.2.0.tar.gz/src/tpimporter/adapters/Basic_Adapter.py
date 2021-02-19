from typing import List, Dict


class Basic_Adapter:
    """
    abstract base class that needs to be subclassed for every special adapter
    each special class should have an instantiated transformer_dict in the following structure:
    {'db_field_name_for_program': 'key_from_tp_importer', ...}
    """
    transformer_dict = dict()

    def transform(self, tp_data: List[Dict], transformer_dict: dict = None) -> List[Dict]:
        """
        transforms the given dictionaries to a form defined in the class variable
        :param tp_data: a list of dictionaries coming from the TP-Importer
        :param transformer_dict: [OPTIONAL] a dictionary with the format {KEY_FOR_APP:KEY_FROM_TPIMPORTER} -
        used for separated importing of further data that is not covered within the original transformer_dict
        :return: List[Dict] (with adapted keys fitting the specific service)
        """
        if not transformer_dict:
            transformer_dict = self.transformer_dict
        tp_data_mam = []
        for title in tp_data:
            title_dict_mam = dict()
            for key_mam, key_tpimporter in transformer_dict.items():
                title_dict_mam[key_mam] = title.get(key_tpimporter)
            tp_data_mam.append(title_dict_mam)
        return tp_data_mam
