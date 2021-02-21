import torch


def sents2t(sentences, seq_len, default=0):
    ret = torch.ones(len(sentences), seq_len, dtype=torch.int64) * default
    for _id, sentence in enumerate(sentences):
        ret[_id, 0:len(sentence)] = torch.tensor(sentence, dtype=torch.int64)
    return ret


def b_sents2t(batch, seq_len=0, default=0):
    if seq_len > 0:
        ret = torch.ones(len(batch), len(batch[0]), seq_len, dtype=torch.int64) * default
        for bid, sentences in enumerate(batch):
            for sid, sentence in enumerate(sentences):
                ret[bid, sid, 0:len(sentence)] = torch.tensor(sentence, dtype=torch.int64)
    else:
        size_1 = 0
        size_2 = 0
        for i in range(len(batch)):
            size_1 = max(size_1, len(batch[i]))
            for j in range(len(batch[i])):
                size_2 = max(size_2, len(batch[i][j]))
        ret = torch.ones(len(batch), size_1, size_2, dtype=torch.int64) * default
        for bid, sentences in enumerate(batch):
            for sid, sentence in enumerate(sentences):
                ret[bid, sid, 0:len(sentence)] = torch.tensor(sentence, dtype=torch.int64)
    return ret


def batch_lookup(x, i):
    index_dim = len(i.shape)
    if index_dim == 1:
        i = i.unsqueeze(1)
    ret = x[torch.arange(x.shape[0]).unsqueeze(1), i]
    if index_dim == 1:
        ret = ret.squeeze(1)
    return ret