from sadedegel.summarize import TFIDFSummarizer, RandomSummarizer, PositionSummarizer, BandSummarizer, Rouge1Summarizer, \
    LengthSummarizer, TextRank, LexRankSummarizer, LexRankPureSummarizer

from sadedegel.dataset import load_annotated_corpus
from sklearn.model_selection import ParameterGrid, ParameterSampler

from sadedegel.config import config_context

from rich.progress import track
from rich.console import Console
from tqdm import tqdm
from rich import box
from rich.table import Table

from collections import defaultdict

from sklearn.metrics import ndcg_score  # type: ignore
from math import ceil
import numpy as np

from scipy.stats.distributions import uniform


def render_table(p_scores: dict, topK=5) -> Table:
    table = Table(
        "Method", "Score", box=box.SIMPLE
    )

    sorted_scores = sorted(p_scores.items(), key=lambda p: p[1], reverse=True)

    if topK is None:
        for m, s in sorted_scores:
            table.add_row(m, str(s))
    else:
        for m, s in sorted_scores[:topK]:
            table.add_row(m, str(s))

    return table


if __name__ == '__main__':
    anno = load_annotated_corpus(False)
    relevance = [[doc['relevance']] for doc in anno]

    with config_context(tokenizer="bert") as DocBuilder:
        docs = [DocBuilder.from_sentences(doc['sentences']) for doc in anno]

    pg = ParameterGrid(
        dict(tf_method=["binary", "raw", "freq", "log_norm", "double_norm"]
             , idf_method=["smooth", "probabilistic"],
             drop_stopwords=[True, False],
             drop_suffix=[True, False], drop_punct=[True, False],
             lowercase=[True, False]))

    models = [RandomSummarizer, (PositionSummarizer, [dict(mode="first"), dict(mode="last")]),
              (BandSummarizer, ParameterGrid(dict(k=[2, 3, 4, 5, 6]))),
              (Rouge1Summarizer, ParameterGrid(dict(metric=["precision", "recall", "f1"]))),
              (LengthSummarizer, ParameterGrid(dict(mode=["token", "char"]))),
              (TextRank, ParameterSampler(dict(alpha=uniform(0, 1)), 1)),
              (TFIDFSummarizer, pg),
              LexRankSummarizer,
              (LexRankPureSummarizer, ParameterGrid(
                  dict(tf_method=["binary", "raw", "freq", "log_norm", "double_norm"]
                       , idf_method=["smooth", "probabilistic"])))]


    def yield_model_instance(mm):
        for mod in tqdm(mm, desc="Models..."):
            if isinstance(mod, tuple):
                m, pg = mod

                for param in tqdm(pg, desc=f"{str(m).split(':')[0]}"):
                    yield m(**param)


            else:
                yield mod()


    scores = defaultdict(list)
    console = Console()

    percentage = 0.8

    # with Live(console=console, screen=True, auto_refresh=False) as live:

    for summarizer in yield_model_instance(models):

        ss = []

        for i, (y_true, d) in tqdm(enumerate(zip(relevance, docs))):
            y_pred = [summarizer.predict(d)]

            # score_10 = ndcg_score(y_true, y_pred, k=ceil(len(d) * 0.1))
            score = ndcg_score(y_true, y_pred, k=ceil(len(d) * percentage))
            # score_80 = ndcg_score(y_true, y_pred, k=ceil(len(d) * 0.8))

            ss.append(score)

        scores[str(summarizer)] = np.array(ss).mean()

    # live.update(render_table(scores, topK=10), refresh=True)

    # console.log(scores)

    console.log(render_table(scores, topK=None))
