#! /usr/bin/python3
# -*- coding: utf-8 -*- 
# @File     :components.py
# @Time     :2021/2/1
# @Author   :jiawei.li
# @Software :PyCharm
# @Desc     :None

import pandas as pd
from sklearn.model_selection import train_test_split
import time
import os
import joblib
import json
from ETAES.utils.mapping import mapping as mapping
from ETAES import TASK_ID
import mlflow
mlflow.set_experiment(str(TASK_ID))
SAVED = False



class Component(object):
    def __init__(self, kwargs, inputs):
        self.inputs = inputs
        self.output_schema_path = kwargs["basic"]["paths"]["output_schemas_path"].format(task_id=TASK_ID)
        self.name = self.__class__.__name__
        self.basic_configs = kwargs['basic']
        if self.name in kwargs['layers'].keys():
            self.components = kwargs['layers'][self.name]
        else:
            self.components = None


class ExampleGen(Component):
    def __init__(self, kwargs, inputs):
        super(ExampleGen, self).__init__(kwargs, inputs)

    def excute(self):
        outputs = None
        if self.basic_configs['status'] == 'online' and 'js' in self.basic_configs.keys():
            js = self.basic_configs['js']
            df_req = pd.concat((pd.json_normalize(d) for d in js), axis=0)
            outputs = df_req
        else:
            if isinstance(self.inputs, str) and str(self.inputs).endswith('.csv'):
                df = pd.read_csv(self.inputs)
                if "Unnamed: 0" in df.columns.values:
                    df.drop(['Unnamed: 0'], axis=1, inplace=True)
                outputs = df
            else:
                outputs = None
        if self.basic_configs['status'] == 'offline' and outputs is not None:
            outputs.to_csv(f'{self.output_schema_path}/{self.name}.csv', index=False)
        return outputs


# TODO(jiawei.li@shopee.com) : Statistic part of data
# TODO： 添加在线数据源（离线是csv,在线json string）
class StatisticsGen(Component):
    def __init__(self, kwargs, inputs):
        super(StatisticsGen, self).__init__(kwargs, inputs)

    def excute(self):
        outputs = self.inputs
        if self.components is not None:
            for component, params in self.components.items():
                parameters = params['params'] if params['params'] is not None else dict()
                parameters['inputs'] = self.inputs
                result = mapping(component)(**parameters)
                if self.basic_configs['status'] == 'offline':
                    if 'mode' in params.keys() and result is not None:
                        mode = params['mode']
                        if mode == 'schema':
                            path = f'{self.output_schema_path.replace("schemas","stat/schemas")}/{component}.csv'
                            result.to_csv(path)
                        elif mode == 'plot':
                            path = f'{self.output_schema_path.replace("schemas","stat/figs")}/{component}.png'
                            result.savefig(path)
                        else:
                            pass
        return outputs


# TODO(jiawei.li@shopee.com) : Create Schema of standard dataset
class SchemaGen(Component):
    def __init__(self, kwargs, inputs):
        super(SchemaGen, self).__init__(kwargs, inputs)

    def excute(self):
        outputs = self.inputs

        if self.components is not None:
            for component, params in self.components.items():
                if component != 'excepts':
                    parameters = params['params']
                    parameters['inputs'] = self.inputs
                    outputs = mapping(component)(**parameters)
            else:
                if 'excepts' in self.components.keys():
                    except_cols = self.components['excepts']
                    if except_cols is not None:
                        for col in except_cols:
                            if col in outputs:
                                print(f'{col} have been excepted!')
                                outputs.drop([col], axis=1, inplace=True)
                            else:
                                print(f'{col} not in columns!')
            if self.basic_configs['status'] == 'offline':
                outputs.to_csv(f'{self.output_schema_path}/{self.name}.csv', index=False)
        return outputs


# TODO(jiawei.li@shopee.com) : Check if data is unusual
class ExampleValidator(Component):
    def __init__(self, kwargs, inputs):
        super(ExampleValidator, self).__init__(kwargs, inputs)

    def excute(self):
        outputs = self.inputs
        if self.components is not None:
            for component, params in self.components.items():
                parameters = params['params']
                component_mapping = component.split('_')[0].strip()
                cols = params.pop('cols')
                for col in cols:
                    if 'astype' in params.keys():
                        outputs[col] = outputs[col].astype('object')
                    if col in outputs.columns.values:
                        col_values = outputs[col].values.reshape(-1, 1)
                        col_values_handled = mapping(component_mapping)(**parameters).fit_transform(col_values)
                        outputs[col] = col_values_handled
        if self.basic_configs['status'] == 'offline':
            outputs.to_csv(f'{self.output_schema_path}/{self.name}.csv', index=False)
        return outputs



# TODO(jiawei.li@shopee.com) : Transform data & feature engineering
class Transform(Component):
    def __init__(self, kwargs, inputs):
        super(Transform, self).__init__(kwargs, inputs)

    def excute(self):
        outputs = self.inputs
        if self.components is not None:
            for component, params in self.components.items():
                if '_' in component:
                    component = component.split('_')[0]
                if params is not None:
                    if 'params' in params:
                        parameters = params['params']
                    else:
                        parameters = None
                    cols = params['cols']
                    if parameters is not None:
                        for col in cols:
                            parameters['inputs'] = self.inputs
                            parameters['cols'] = cols
                            control_outputs = mapping(component)(**parameters)
                            outputs[col] = control_outputs
                    else:
                        for col in cols:
                            control_outputs = mapping(component)().fit_transform(outputs[col].values.reshape(-1, 1))
                            outputs[col] = control_outputs
                    del control_outputs
            if self.basic_configs['status'] == 'offline':
                outputs.to_csv(f'{self.output_schema_path}/{self.name}.csv', index=False)
        return outputs


# TODO(jiawei.li@shopee.com) : Training step
class Trainer(Component):
    def __init__(self, kwargs, inputs):
        super(Trainer, self).__init__(kwargs, inputs)

    def excute(self):
        # mode in ['single','bagging','boosting','stacking']
        if self.components is not None:
            mode = self.components.pop('mode')
            output = {
                'mode': mode,
                'names': [],
                'clfs':[],
                'data':[]
            }
            for component, params in self.components.items():
                if mode == 'single':
                    label = self.basic_configs['label']
                    parameters = params['params']
                    X = self.inputs.drop([label], axis=1)
                    y = self.inputs[label]
                    for k, v in parameters.items():
                        mlflow.log_param(k, v)
                    X_train, X_test, y_train, y_test = train_test_split(X, y)
                    component_func = mapping(component)(**parameters)
                    output['names'].append(component)
                    component_func.fit(X=X_train, y=y_train)
                    output['clfs'].append(component_func)
                    output['data'].append((X_train, X_test, y_train, y_test))
            return output


# TODO(jiawei.li@shopee.com) : Evaluating step
class Evaluator(Component):
    def __init__(self, kwargs, inputs):
        super(Evaluator, self).__init__(kwargs, inputs)

    def excute(self):
        if self.inputs is not None:
            output = self.inputs
            output['evaluator'] = []
            clfs = self.inputs['clfs']
            (_, X_test, _, y_test) = self.inputs['data'][0]
            for component, params in self.components.items():
                params['estimator'] = clfs[0]
                params['X'] = X_test
                params['y'] = y_test
                mode = params.pop('mode')
                output['evaluator'].append({component:params})
                format_dic = {
                    'task_id': TASK_ID
                }
                if component == 'cross_validation':
                    if mode == 'schema':
                        scores = mapping(component)(**params)
                        score_df = pd.DataFrame(scores)
                    elif mode == 'plot':
                        pass
                else:
                    if mode == 'schema':
                        params['params']['y_pred'] = params['estimator'].predict(params['X'])
                        params['params']['y_true'] = y_test.values
                        score = mapping(component)(**params['params'])
                        score_df = pd.DataFrame({component:score})
                if score is not None:
                    mlflow.log_metrix(component, score)
                if score_df is not None and self.basic_configs['status'] == 'offline':
                    score_df.to_csv(
                        f'{self.basic_configs["paths"]["evaluation_schemas_path"]}/{component}.csv'.format(**format_dic))
            return output


# TODO(jiawei.li@shopee.com) : Model saver(save as .pkl)
class Pusher(Component):
    def __init__(self, kwargs, inputs):
        super(Pusher, self).__init__(kwargs, inputs)

    def excute(self):
        if self.inputs is not None:
            clfs = self.inputs['clfs']
            names = self.inputs['names']
            for idx, clf in enumerate(clfs):
                format_dict = {
                    'name': names[idx],
                    'dt': int(time.time()),
                    'task_id': TASK_ID,
                }

                path = (os.path.join(self.basic_configs['paths']['output_models_path'], self.components['format'])).format(**format_dict)
                joblib.dump(clf, path)
            return self.inputs

class Loader(Component):
    def __init__(self, kwargs, inputs):
        super(Loader, self).__init__(kwargs, inputs)

    def excute(self):
        outputs = {'data': self.inputs}
        if self.inputs is not None:
            task_id = self.basic_configs['task_id']
            outputs['task_id'] = task_id
            clf_dir = self.basic_configs['paths']['output_models_path'].format(**{'task_id':task_id})
            if os.path.exists(clf_dir):
                clfs = []
                for clf_path in os.listdir(clf_dir):
                    clf = joblib.load(os.path.join(clf_dir, clf_path))
                    assert clf is not None
                    clfs.append(clf)
                outputs['clfs'] = clfs
                return outputs

# TODO(jiawei.li@shopee.com) : Model predictor
class Predictor(Component):
    def __init__(self, kwargs, inputs):
        super(Predictor, self).__init__(kwargs, inputs)

    def excute(self):
        if self.inputs is not None:
            output = self.inputs
            clfs = self.inputs['clfs']
            for idx, clf in enumerate(clfs):
                if self.basic_configs['status'] == 'offline':
                    _, X_test, _, y_test = self.inputs['data'][idx]
                    X_test['predictions'] = clf.predict(X_test)
                    names = self.inputs['names']
                    format_dict = {
                        'task_id': TASK_ID,
                        'name': names[idx],
                        'dt': int(time.time()),
                    }
                    path = os.path.join(self.basic_configs['paths']['output_prediction_path'].format(**format_dict),
                                        self.components['format']).format(**format_dict)
                    X_test.to_csv(path, index=False)
                else:
                    X_test = self.inputs['data']
                    label_col = self.basic_configs['label']
                    if label_col in X_test.columns.values:
                        X_test.drop([label_col], axis=1, inplace=True)
                    X_test['predictions'] = clf.predict(X_test)
                output = X_test['predictions'].values
                print(output.shape)
            return output


###------------------------End Pipeline Component