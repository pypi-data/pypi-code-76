import logging
from IPython.core.display import display, HTML
from expai.utils import generate_response

class ExpaiModelExplainer:
    def __init__(self, model_id: str, project_id: str, api_key: str, headers: dict, server_name: str, session, project):
        self.model_id = model_id
        self.project_id = project_id

        self.server_name = server_name
        self.api_key = api_key

        self.headers = headers
        
        self.sess = session
        self.project = project

    def _get_sample_id_from_name(self, sample_name: str = None):

        sample_list = self.project.sample_list()
        for sample in sample_list:
            if sample['sample_name_des'] == sample_name:
                return sample['sample_id']
        return None

    def raw_explanation(self, sample_name: str = None, sample_id: str = None, indexes: list = None, shap: bool = True, lime: bool = False):
        assert sample_name is not None or sample_id is not None, "You must provide a sample name or id for the explanation"
        if indexes is None:
            logging.warning("You will generate explanation for all entries in the file. This might consume many credits and time. Use it on your own risk")

        if sample_id is None:
            sample_id = self._get_sample_id_from_name(sample_name)

            if sample_id is None:
                logging.error(
                    "We could not find any sample matching that name. Please, try again or use sample_id as parameter")
                return None

        json = {
                    "sample_id": sample_id,
                    "shap": shap,
                    "lime": lime,
                    "indexes": indexes
                }

        response = self.sess.request("GET",
                                    self.server_name + "/api/explain/{}".format(self.model_id), headers=self.headers, json=json)

        return generate_response(response, 'shap_values')

    def explain_model(self, sample_name: str = None, sample_id: str = None, indexes: list = None, shap: bool = True, lime: bool = False):
        assert sample_name is not None or sample_id is not None, "You must provide a sample name or id for the explanation"
        if indexes is None:
            logging.warning("You will generate explanation for all entries in the file. This might consume many credits and time. Use it on your own risk.")

        if sample_id is None:
            sample_id = self._get_sample_id_from_name(sample_name)

            if sample_id is None:
                logging.error(
                    "We could not find any sample matching that name. Please, try again or use sample_id as parameter")
                return None

        json = {
                    "sample_id": sample_id,
                    "shap": shap,
                    "lime": lime,
                    "indexes": indexes
                }

        response = self.sess.request("GET",
                                    self.server_name + "/api/explain/{}/graphics".format(self.model_id), headers=self.headers, json=json)

        return generate_response(response, 'visualizations')

    def explain_sample(self, sample_name: str = None, sample_id: str = None, index: list = None, shap: bool = True, lime: bool = False):
        assert sample_name is not None or sample_id is not None, "You must provide a sample name or id for the explanation"
        assert index is not None, "You must specify the index of the sample you want to explain"

        if sample_id is None:
            sample_id = self._get_sample_id_from_name(sample_name)

            if sample_id is None:
                logging.error(
                    "We could not find any sample matching that name. Please, try again or use sample_id as parameter")
                return None

        json = {
                    "sample_id": sample_id,
                    "shap": shap,
                    "lime": lime,
                    "index": [index]
                }

        response = self.sess.request("GET",
                                    self.server_name + "/api/explain/{}/sample/graphics".format(self.model_id), headers=self.headers, json=json)

        if response.ok:
            return response.json()['visualizations']['single_force_plot']
        else:
            if 'error' in response.json().keys():
                logging.error("There was an error deleting the sample. Please, check the details below. \n {}".format(
                    response.json()['error']))
            else:
                logging.error("There was an error deleting the sample. Please, check the details below. \n {}".format(
                    response.json()['message']))
            return None


    def plot(self, plot_html):
        display(HTML(plot_html))

    def store_plot(self, plot_html, filepath: str):
        with open(filepath, 'w') as f:
            f.write(plot_html)

    def load_plot(self, filepath):
        with open(filepath, 'r') as f:
            return f.read()

    def what_if(self, original_sample: dict = None, modified_sample: dict = None, original_sample_display: dict = None, modified_sample_display: dict = None):
        assert original_sample is not None and modified_sample is not None, "You must provide an old and new sample to use this module"
        if original_sample_display is not None or modified_sample_display is not None:
            assert original_sample_display is not None and modified_sample_display is not None, "You must provide both display samples."

        # Ensure there are no integer keys in the dictionaries
        for dict_ in [x for x in [original_sample, modified_sample, original_sample_display, modified_sample_display] if x is not None]:
            for key, value in dict_.items():
                if isinstance(value, int):
                    dict_[key] = float(value)


        json = {
            "original_sample": original_sample,
            "modified_sample": modified_sample,
            "original_sample_display": original_sample_display,
            "modified_sample_display": modified_sample_display,
        }

        response = self.sess.request("GET",
                                    self.server_name + "/api/explain/{}/what_if".format(self.model_id), headers=self.headers, json=json)

        if response.ok:
            return response.json()['visualizations'], response.json()['shap_values']
        else:
            if 'error' in response.json().keys():
                logging.error("There was an error generating what if explanation. Please, check the details below. \n {}".format(
                    response.json()['error']))
            else:
                logging.error("There was an error generating what if explanation. Please, check the details below. \n {}".format(
                    response.json()['message']))
            return None



