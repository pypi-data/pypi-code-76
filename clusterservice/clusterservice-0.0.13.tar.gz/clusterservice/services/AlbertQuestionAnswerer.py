import logging

import torch
from transformers import squad_convert_examples_to_features
from transformers.data.processors.squad import SquadExample, SquadResult, SquadV2Processor
from transformers.data.metrics.squad_metrics import compute_predictions_logits
from torch.utils.data import DataLoader, SequentialSampler

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


class AlbertQuestionAnswerer:

    def __init__(self, model, tokenizer):
        self.output_dir = ''

        # Config
        self.n_best_size = 1
        self.max_answer_length = 30
        self.do_lower_case = True
        self.null_score_diff_threshold = 0.0
        
        self.tokenizer = tokenizer
        self.model =  model
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        #logger.debug('Using device*********************************', self.device)
        self.model.to(self.device)
        self.processor = SquadV2Processor()

    def to_list(self, tensor):
        return tensor.detach().cpu().tolist()

    def predict(self, question_texts, context_texts):
        """Setup function to compute predictions"""
        examples = []
        for i, context_text in enumerate(context_texts):
            for j, question_text in enumerate(question_texts):
                example = SquadExample(
                    qas_id='%d-%d' % (i, j),
                    question_text=question_text,
                    context_text=context_text,
                    answer_text=None,
                    start_position_character=None,
                    title='Predict',
                    is_impossible=False,
                    answers=None,
                )
                examples.append(example)

        features, dataset = squad_convert_examples_to_features(
            examples=examples,
            tokenizer=self.tokenizer,
            max_seq_length=384,
            doc_stride=128,
            max_query_length=64,
            is_training=False,
            return_dataset='pt',
            threads=1,
        )
        eval_sampler = SequentialSampler(dataset)
        eval_dataloader = DataLoader(dataset, sampler=eval_sampler, batch_size=10)

        all_results = []

        for batch in eval_dataloader:
            self.model.eval()
            batch = tuple(t.to(self.device) for t in batch)
            with torch.no_grad():
                inputs = {
                    'input_ids': batch[0],
                    'attention_mask': batch[1],
                    'token_type_ids': batch[2],
                }
                example_indices = batch[3]
                outputs = self.model(**inputs)
                for i, example_index in enumerate(example_indices):
                    eval_feature = features[example_index.item()]
                    unique_id = int(eval_feature.unique_id)
                    output = [self.to_list(output[i]) for output in outputs]
                    start_logits, end_logits = output
                    result = SquadResult(unique_id, start_logits, end_logits)
                    all_results.append(result)

        predictions = compute_predictions_logits(
            examples,
            features,
            all_results,
            self.n_best_size,
            self.max_answer_length,
            self.do_lower_case,
            None,
            None,
            None,
            False,  # verbose_logging
            True,  # version_2_with_negative
            self.null_score_diff_threshold,
            self.tokenizer,
        )

        return predictions
