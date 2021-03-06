import json

import sacrebleu
from nltk.translate.bleu_score import SmoothingFunction, corpus_bleu

from lib.data.util import reverse_index, trim_sentences

# Global variables
DATASET = None
TARGET_VOCAB = None


def bleu_score(reference, candidate, log_outputs=True):
    # TODO: Find a workaround for Keras metric API limitation
    # reference = reverse_indexing(reference, TARGET_VOCAB, ravel=True)
    candidate = trim_sentences(reverse_index(candidate, TARGET_VOCAB))
    if log_outputs:
        with open('%s_output.json' % DATASET, 'w') as json_file:
            json.dump(list(zip(reference, candidate)), json_file)
    reference = [[x] for x in reference]

    bleu_m4 = 0
    try:
        bleu_m4 = corpus_bleu(reference, candidate, smoothing_function=SmoothingFunction().method4)
    except Exception as e:
        print(e)

    bleu_m5 = 0
    try:
        bleu_m5 = corpus_bleu(reference, candidate, smoothing_function=SmoothingFunction().method5)
    except Exception as e:
        print(e)

    return bleu_m4, bleu_m5


def multi_bleu_score(candidate, target_vocab):
    lang_pair = '-'.join(DATASET.split('_'))
    candidate = reverse_index(candidate, target_vocab)
    _, *refs = sacrebleu.download_test_set('wmt14', lang_pair)
    bleu = sacrebleu.corpus_bleu(candidate, refs)
    return bleu.score


