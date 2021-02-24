from copy import copy
import random
import numpy

def train(datalist,*args, **kwargs):
    model = kwargs.get('model', {})
    for datadict in datalist:
        for key in datadict:
            keydata = datadict[key]
            if "options" in keydata:
                assert type(keydata["options"]) == list, "options parameter must be list"
                assert "choice" in keydata, "Must have choice parameter if you have options parameter"
                assert keydata["choice"] in keydata["options"], "Choice parameter must be item in options parameter"
            if key in model:
                update_key = copy(model[key])
            else:
                if "options" in keydata:
                    update_key = {"option_dict":{}}
                else:
                    update_key = {"count":0,"result_dict":{}}
            if "option_dict" in update_key:
                for x in keydata["options"]:
                    assert type(x) == str, "all options must be strings"
                    if x not in update_key["option_dict"]:
                        update_key["option_dict"].update({
                            x:{
                                "count":0,
                                "result_dict": {}
                            }
                        })
                if keydata["result"] not in update_key["option_dict"][keydata["choice"]]["result_dict"]:
                    update_key["option_dict"][keydata["choice"]]["result_dict"].update(
                        {keydata["result"]:0}
                    )
                update_key["option_dict"][keydata["choice"]]["count"] += 1
                update_key["option_dict"][keydata["choice"]]["result_dict"][keydata["result"]] += 1
            if "result_dict" in update_key:
                if keydata["result"] not in update_key["result_dict"]:
                    update_key["result_dict"].update(
                        {keydata["result"]:0}
                    )
                update_key["count"] += 1
                update_key["result_dict"][keydata["result"]] += 1                
            model.update({key:update_key})
    return model

def update(datalist,model):
    return train(datalist=datalist,model=model)

def classify(datalist,model):
    class_list = []
    for datadict in datalist:
        classifications = {}
        for key in datadict:
            desired_result = datadict[key]["desired_result"] 
            if "options" in datadict[key]:
                assert "desired_result" in datadict[key], "You must have a desired result if you are providing options"
                assert type(datadict[key]["options"]) == list, "Options must be a list"
                if key not in model:
                    choice = random.choice(datadict[key]["options"])
                else:
                    assert "option_dict" in model[key], "model does not support options for key - "+key
                    option_weights = []
                    for option in datadict[key]["options"]:
                        option_count = model[key]["option_dict"][option]["count"]
                        if datadict[key]["desired_result"] in model[key]["option_dict"][option]["result_dict"]:
                            result_count = model[key]["option_dict"][option]["result_dict"][desired_result]
                        else:
                            result_count = 0
                        option_weights.append((result_count+1.0)/(option_count+2.0))
                    choice = random.choices(datadict[key]["options"],option_weights,k=1)[0]
            else:
                assert "results" in datadict[key], "options or results must be specified"
                assert type(datadict[key]["results"]) == list, "results value must be a list"
                assert len(datadict[key]["results"]) > 0, "results value must have at least one element"
                if key not in model:
                    choice = random.choice(datadict[key]["results"])
                else:
                    assert "result_dict" in model[key], "model requires options for key - "+key
                    result_weights = []
                    total_count = model[key]["count"]
                    for result in datadict[key]["results"]:
                        if result in model[key]["result_dict"]:
                            result_count = model[key]["result_dict"][result]
                        else:
                            result_count = 0
                        result_weights.append((result_count+1.0)/(total_count+2.0))
                    choice = random.choices(datadict[key]["results"],result_weights,k=1)[0]
            classifications.update({key:choice})
        class_list.append(classifications)
    return class_list        

def test(datalist,model):
    loss = 0
    correct_class = 0.0
    total_class = 0
    for datadict in datalist:
        total_class += len(datadict)
        for key in datadict:
            keydict = datadict[key]
            keymodel = model[key]
            if "options" in keydict:
                assert "choice" in keydict, "all entries with 'options' must also have 'choice'"
                assert choice in keydict["options"], "'choice' must be in 'options' list"
                assert "option_dict" in keymodel, "model does not support options for key "+key
                choice = keydict["choice"]
                if choice in keymodel["option_dict"]:
                    total_count = keymodel["option_dict"][choice]["count"]
                    if keydict["result"] in keymodel["option_dict"][choice]["result_dict"]:
                        result_count = keymodel["option_dict"][choice]["result_dict"][keydict["result"]]
                    else:
                        result_count = 0
                    prob_result = float(result_count+1)/(total_count+2)
                else:
                    prob_result = 0.5
            else:
                assert "result_dict" in keymodel, "model requires options for key "+key
                result = keydict["result"]
                total_count = keymodel["count"]
                if result in keymodel["result_dict"]:
                    result_count = keymodel["result_dict"][result]
                else:
                    result_count = 0
                prob_result = float(result_count+1)/(total_count+2)
            loss += -1*numpy.log(prob_result)
            correct_class += prob_result
    accuracy = correct_class/total_class
    return {"accuracy":accuracy,"loss":loss}


