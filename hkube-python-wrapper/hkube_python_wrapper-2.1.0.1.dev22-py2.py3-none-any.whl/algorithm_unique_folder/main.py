def start(a,b):
        import json;
        print(json.dumps(a));
        myDict = dict();
        myDict.update({"value1":"hello"});
        myDict.update({"value2":5});
        myDict.update({"arr":[1,2]});
        return myDict;
