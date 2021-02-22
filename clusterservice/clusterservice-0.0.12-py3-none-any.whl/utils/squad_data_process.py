from functools import partial
from tqdm import tqdm

import numpy as np
from transformers.data.processors.squad import SquadExample, SquadFeatures, SquadV2Processor
from transformers.data.processors.squad import _new_check_is_max_context
from transformers.file_utils import is_torch_available

if is_torch_available():
    import torch
    from torch.utils.data import TensorDataset


def squad_convert_example_to_features_init(tokenizer_for_convert):
    global tokenizer
    tokenizer = tokenizer_for_convert


def squad_convert_example_to_features(example, max_seq_length, doc_stride, max_query_length, is_training):
    features = []
    if is_training and not example.is_impossible:
        # Get start and end position
        start_position = example.start_position
        end_position = example.end_position

        # If the answer cannot be found in the text then skip this example
        actual_text = ' '.join(example.doc_tokens[start_position : (end_position + 1)])
        cleaned_answer_text = ' '.join(whitespace_tokenize(example.answer_text))
        if actual_text.find(cleaned_answer_text) == -1:
            logger.warning('Could not find answer: "%s" vs. "%s"', actual_text, cleaned_answer_text)
            return []

    tok_to_orig_index = []
    orig_to_tok_index = []
    all_doc_tokens = []
    for (i, token) in enumerate(example.doc_tokens):
        orig_to_tok_index.append(len(all_doc_tokens))
        sub_tokens = tokenizer.tokenize(token)
        for sub_token in sub_tokens:
            tok_to_orig_index.append(i)
            all_doc_tokens.append(sub_token)

    if is_training and not example.is_impossible:
        tok_start_position = orig_to_tok_index[example.start_position]
        if example.end_position < len(example.doc_tokens) - 1:
            tok_end_position = orig_to_tok_index[example.end_position + 1] - 1
        else:
            tok_end_position = len(all_doc_tokens) - 1

        tok_start_position, tok_end_position = _improve_answer_span(
            all_doc_tokens, tok_start_position, tok_end_position, tokenizer, example.answer_text
        )

    spans = []
    truncated_query = tokenizer.encode(example.question_text, add_special_tokens=False, max_length=max_query_length)
    sequence_added_tokens = (
        tokenizer.max_len - tokenizer.max_len_single_sentence + 1
        if 'roberta' in str(type(tokenizer)) or 'camembert' in str(type(tokenizer))
        else tokenizer.max_len - tokenizer.max_len_single_sentence
    )
    sequence_pair_added_tokens = tokenizer.max_len - tokenizer.max_len_sentences_pair

    span_doc_tokens = all_doc_tokens
    while len(spans) * doc_stride < len(all_doc_tokens):
        encoded_dict = tokenizer.encode_plus(
            truncated_query if tokenizer.padding_side == 'right' else span_doc_tokens,
            span_doc_tokens if tokenizer.padding_side == 'right' else truncated_query,
            max_length=max_seq_length,
            return_overflowing_tokens=True,
            pad_to_max_length=True,
            stride=max_seq_length - doc_stride - len(truncated_query) - sequence_pair_added_tokens,
            truncation_strategy='only_second' if tokenizer.padding_side == 'right' else 'only_first',
            return_token_type_ids=True,
        )

        paragraph_len = min(
            len(all_doc_tokens) - len(spans) * doc_stride,
            max_seq_length - len(truncated_query) - sequence_pair_added_tokens,
        )

        if tokenizer.pad_token_id in encoded_dict['input_ids']:
            if tokenizer.padding_side == 'right':
                non_padded_ids = encoded_dict['input_ids'][: encoded_dict['input_ids'].index(tokenizer.pad_token_id)]
            else:
                last_padding_id_position = (
                    len(encoded_dict['input_ids']) - 1 - encoded_dict['input_ids'][::-1].index(tokenizer.pad_token_id)
                )
                non_padded_ids = encoded_dict['input_ids'][last_padding_id_position + 1 :]
        else:
            non_padded_ids = encoded_dict['input_ids']

        tokens = tokenizer.convert_ids_to_tokens(non_padded_ids)

        token_to_orig_map = {}
        for i in range(paragraph_len):
            index = len(truncated_query) + sequence_added_tokens + i if tokenizer.padding_side == 'right' else i
            token_to_orig_map[index] = tok_to_orig_index[len(spans) * doc_stride + i]

        encoded_dict['paragraph_len'] = paragraph_len
        encoded_dict['tokens'] = tokens
        encoded_dict['token_to_orig_map'] = token_to_orig_map
        encoded_dict['truncated_query_with_special_tokens_length'] = len(truncated_query) + sequence_added_tokens
        encoded_dict['token_is_max_context'] = {}
        encoded_dict['start'] = len(spans) * doc_stride
        encoded_dict['length'] = paragraph_len

        spans.append(encoded_dict)

        if 'overflowing_tokens' not in encoded_dict:
            break

        span_doc_tokens = encoded_dict['overflowing_tokens']

    for doc_span_index in range(len(spans)):
        for j in range(spans[doc_span_index]['paragraph_len']):
            is_max_context = _new_check_is_max_context(spans, doc_span_index, doc_span_index * doc_stride + j)
            index = (
                j
                if tokenizer.padding_side == 'left'
                else spans[doc_span_index]['truncated_query_with_special_tokens_length'] + j
            )
            spans[doc_span_index]['token_is_max_context'][index] = is_max_context

    for span in spans:
        # Identify the position of the CLS token
        cls_index = span['input_ids'].index(tokenizer.cls_token_id)

        # p_mask: mask with 1 for token that cannot be in the answer (0 for token which can be in an answer)
        # original TF implementation also keeps the classification token (set to 0)
        p_mask = np.ones_like(span['token_type_ids'])
        if tokenizer.padding_side == 'right':
            p_mask[len(truncated_query) + sequence_added_tokens :] = 0
        else:
            p_mask[-len(span['tokens']) : -(len(truncated_query) + sequence_added_tokens)] = 0

        pad_token_indices = np.where(span['input_ids'] == tokenizer.pad_token_id)
        special_token_indices = np.asarray(
            tokenizer.get_special_tokens_mask(span['input_ids'], already_has_special_tokens=True)
        ).nonzero()

        p_mask[pad_token_indices] = 1
        p_mask[special_token_indices] = 1

        # Set the cls index to 0: the CLS index can be used for impossible answers
        p_mask[cls_index] = 0

        span_is_impossible = example.is_impossible
        start_position = 0
        end_position = 0
        if is_training and not span_is_impossible:
            # For training, if our document chunk does not contain an annotation,
            # we throw it out since there is nothing to predict
            doc_start = span['start']
            doc_end = span['start'] + span['length'] - 1
            out_of_span = False

            if not (tok_start_position >= doc_start and tok_end_position <= doc_end):
                out_of_span = True

            if out_of_span:
                start_position = cls_index
                end_position = cls_index
                span_is_impossible = True
            else:
                if tokenizer.padding_side == 'left':
                    doc_offset = 0
                else:
                    doc_offset = len(truncated_query) + sequence_added_tokens

                start_position = tok_start_position - doc_start + doc_offset
                end_position = tok_end_position - doc_start + doc_offset

        features.append(
            SquadFeatures(
                span['input_ids'],
                span['attention_mask'],
                span['token_type_ids'],
                cls_index,
                p_mask.tolist(),
                example_index=0,  # cannot set unique_id and example_index here; they will be set after multiple processing
                unique_id=0,
                paragraph_len=span['paragraph_len'],
                token_is_max_context=span['token_is_max_context'],
                tokens=span['tokens'],
                token_to_orig_map=span['token_to_orig_map'],
                start_position=start_position,
                end_position=end_position,
                is_impossible=span_is_impossible,
                qas_id=example.qas_id,
            )
        )

    return features

def squad_convert_examples_to_features(
    examples,
    tokenizer,
    max_seq_length,
    doc_stride,
    max_query_length,
    is_training,
    return_dataset=False,
    threads=1,
    tqdm_enabled=True,
):
    """
    Converts a list of examples into a list of features that can be directly given as input to a model.

    It is model-dependent and takes advantage of many of the tokenizer's features to create the model's
    inputs.

    Args:
        examples: list of :class:`~transformers.data.processors.squad.SquadExample`
        tokenizer: an instance of a child of :class:`~transformers.PreTrainedTokenizer`
        max_seq_length: The maximum sequence length of the inputs.
        doc_stride: The stride used when the context is too large and is split across several features.
        max_query_length: The maximum length of the query.
        is_training: whether to create features for model evaluation or model training.
        return_dataset: Default False. Either 'pt' or 'tf'.
            if 'pt': returns a torch.data.TensorDataset,
            if 'tf': returns a tf.data.Dataset
        threads: multiple processing threadsa-smi

    Returns:
        list of :class:`~transformers.data.processors.squad.SquadFeatures`

    Example::
        processor = SquadV2Processor()
        examples = processor.get_dev_examples(data_dir)
        features = squad_convert_examples_to_features(
            examples=examples,
            tokenizer=tokenizer,
            max_seq_length=args.max_seq_length,
            doc_stride=args.doc_stride,
            max_query_length=args.max_query_length,
            is_training=not evaluate,
        )
    """
    # Defining helper methods
    features = []
    threads = 1
    squad_convert_example_to_features_init(tokenizer)

    annotate_ = partial(
        squad_convert_example_to_features,
        max_seq_length=max_seq_length,
        doc_stride=doc_stride,
        max_query_length=max_query_length,
        is_training=is_training,
    )

    for example in tqdm(examples,
            total=len(examples),
            desc='convert squad examples to features',
            disable=not tqdm_enabled):
        features.append(squad_convert_example_to_features(
            example=example,
            max_seq_length=max_seq_length,
            doc_stride=doc_stride,
            max_query_length=max_query_length,
            is_training=is_training
            ))

    new_features = []
    unique_id = 1000000000
    example_index = 0
    for example_features in tqdm(
        features, total=len(features), desc='add example index and unique id', disable=(not tqdm_enabled)
    ):
        if not example_features:
            continue

        for example_feature in example_features:
            example_feature.example_index = example_index
            example_feature.unique_id = unique_id
            new_features.append(example_feature)
            unique_id += 1

        example_index += 1

    features = new_features
    del new_features
    if return_dataset == 'pt':
        if not is_torch_available():
            raise RuntimeError('Torch must be installed to return a PyTorch dataset.')

        # Convert to Tensors and build dataset
        all_input_ids = torch.tensor([f.input_ids for f in features], dtype=torch.long)
        all_attention_masks = torch.tensor([f.attention_mask for f in features], dtype=torch.long)
        all_token_type_ids = torch.tensor([f.token_type_ids for f in features], dtype=torch.long)
        all_cls_index = torch.tensor([f.cls_index for f in features], dtype=torch.long)
        all_p_mask = torch.tensor([f.p_mask for f in features], dtype=torch.float)
        all_is_impossible = torch.tensor([f.is_impossible for f in features], dtype=torch.float)

        if not is_training:
            all_feature_index = torch.arange(all_input_ids.size(0), dtype=torch.long)
            dataset = TensorDataset(
                all_input_ids,
                all_attention_masks,
                all_token_type_ids,
                all_feature_index,
                all_cls_index,
                all_p_mask
            )
        else:
            all_start_positions = torch.tensor([f.start_position for f in features], dtype=torch.long)
            all_end_positions = torch.tensor([f.end_position for f in features], dtype=torch.long)
            dataset = TensorDataset(
                all_input_ids,
                all_attention_masks,
                all_token_type_ids,
                all_start_positions,
                all_end_positions,
                all_cls_index,
                all_p_mask,
                all_is_impossible
            )

        return features, dataset

    elif return_dataset == 'tf':
        if not is_tf_available():
            raise RuntimeError('TensorFlow must be installed to return a TensorFlow dataset.')

        def gen():
            for i, ex in enumerate(features):
                yield (
                    {
                        'input_ids': ex.input_ids,
                        'attention_mask': ex.attention_mask,
                        'token_type_ids': ex.token_type_ids,
                        'feature_index': i,
                        'qas_id': ex.qas_id,
                    },
                    {
                        'start_position': ex.start_position,
                        'end_position': ex.end_position,
                        'cls_index': ex.cls_index,
                        'p_mask': ex.p_mask,
                        'is_impossible': ex.is_impossible,
                    },
                )

        # Why have we split the batch into a tuple? PyTorch just has a list of tensors.
        train_types = (
            {
                'input_ids': tf.int32,
                'attention_mask': tf.int32,
                'token_type_ids': tf.int32,
                'feature_index': tf.int64,
                'qas_id': tf.string,
            },
            {
                'start_position': tf.int64,
                'end_position': tf.int64,
                'cls_index': tf.int64,
                'p_mask': tf.int32,
                'is_impossible': tf.int32,
            },
        )

        train_shapes = (
            {
                'input_ids': tf.TensorShape([None]),
                'attention_mask': tf.TensorShape([None]),
                'token_type_ids': tf.TensorShape([None]),
                'feature_index': tf.TensorShape([]),
                'qas_id': tf.TensorShape([]),
            },
            {
                'start_position': tf.TensorShape([]),
                'end_position': tf.TensorShape([]),
                'cls_index': tf.TensorShape([]),
                'p_mask': tf.TensorShape([None]),
                'is_impossible': tf.TensorShape([]),
            },
        )

        return tf.data.Dataset.from_generator(gen, train_types, train_shapes)

    else:
        return features
