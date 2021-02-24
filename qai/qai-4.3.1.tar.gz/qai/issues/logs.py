from qai.issues.add_issues import parse


def get_payload_stats(json_data, nlp):
    try:
        _ = json_data.items()
        els = [json_data]
    except AttributeError:
        els = json_data

    n_seg = len(els) if els else 0
    n_sent = 0
    n_word = 0

    try:
        for el in els:
            segment, _, _ = parse(el)
            n_sent += len(list(nlp(segment).sents))
            n_word += len(segment.split())
    except:
        # this will cause escaped exception in sanic logger
        # do nothing
        pass

    return n_seg, n_sent, n_word
