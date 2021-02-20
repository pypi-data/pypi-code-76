import numpy as np

import torch
from transformers import BertForTokenClassification, BertTokenizer

class BertTokenTagger:
    def __init__(self, model_type, model_dir, tag_values, device="cpu"):
        
        if model_type == "bert-base-cased":
            do_lower_case = False
        elif model_type == "bert-base-uncased":
            do_lower_case = True
        else:
            raise NotImplementedError

        self.tokenizer = BertTokenizer.from_pretrained(model_type, do_lower_case=do_lower_case)
        self.model = BertForTokenClassification.from_pretrained(model_dir)
        self.device = device
        if self.device == "cuda":
            model.cuda()
        self.model.eval()
        self.tag_values = tag_values

    def __call__(self, line):
        
        inputs = self.tokenizer(line, return_tensors="pt")
        tokens =["[CLS]"] + self.tokenizer.tokenize(line) + ["[SEP]"]
        
        if len(tokens) > 128:
            print("input too long")
            return tokens, ["NONE" for t in tokens]

        labels = torch.tensor([1] * inputs["input_ids"].size(1)).unsqueeze(0)  # Batch size 1
        outputs = self.model(**inputs, labels=labels)
        logits = outputs.logits
        logits = outputs[1].detach().cpu().numpy()
        pred_labels = [self.tag_values[p] for p in np.argmax(logits, axis=2)[0]]
        return tokens, pred_labels
