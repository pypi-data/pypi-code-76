from pathlib import Path
import tensorflow as tf
import sys
import json
import re
tf.compat.v1.disable_eager_execution()

class FlagParser:
    def __init__(self):
        self.model_path = "assets"
        model = tf.saved_model.load(str(Path(__file__).parent.joinpath(self.model_path)))
        # print(model.signatures.keys())
        self.model = model.signatures["serving_default"]
        forex_path = "assets/forexlist.json"
        self.forex_data = json.loads(
            Path(__file__).parent.joinpath(forex_path).read_text())

    def detect_image(self, image_path):
        with open(image_path, 'rb') as img_file:
            data = img_file.read()
            y_pred = self.model(image_bytes = tf.constant([data]), key=tf.constant(["Placeholder:0"]))  
            with tf.compat.v1.Session():
                labels = (x.decode() for x in (y_pred['labels'].eval()[0]))
                potential = dict(zip(labels, y_pred["scores"].eval()[0]))
                result = list(filter(lambda x : x[1] > 0.7, potential.items()))
                if len(result) != 2:
                    return ""
                cur1 = result[0][0]
                cur2 = result[1][0]
                for tmp in self.forex_data:
                    if cur1 in tmp and cur2 in tmp:
                        return re.sub(r'\W+', '', tmp).upper()
                return ""
            