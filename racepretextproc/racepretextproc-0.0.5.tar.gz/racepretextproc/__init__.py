from racepretextproc.visualization import visualize
from racepretextproc.normalization import normalization
from racepretextproc.noise_remove import noise_remove
from racepretextproc.lemetstemtoken import lemetstemtoken

def process(text, noise=True, norm=True, lemma=True, visual=True):
    """
    Process Text
    :param text:
    :param remove_noise:
    :param normalization:
    :param lemma:
    :param visualize:
    :return:
    """
    original_text = text;
    if noise:
        text_proc = noise_remove.textpreprocessor(text)
        text = text_proc.remove_noise(remove_stop_words=True, remove_non_eng=False)

    if norm:
        text = normalization.normalization(text).normalizmain()

    if lemma:
        lemstemObj = lemetstemtoken.lemetization_stemming_tokenization(text);
        text = lemstemObj.lemet_stem_token(do_stem=True)

    if visual:
        visualize.WordCloud(max_words=50).show(text);
        visualize.FrequencyDist.show(text, min_length=3, nof_large_words=20)

    return text
