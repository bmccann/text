# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import Counter
import unittest

import numpy as np
from torchtext import vocab


class TestVocab(unittest.TestCase):
    def test_vocab(self):
        c = Counter({'hello': 4, 'world': 3, 'ᑌᑎIᑕOᗪᕮ_Tᕮ᙭T': 5, 'freq_too_low': 2})
        v = vocab.Vocab(c, min_freq=3, specials=['<pad>', '<bos>'],
                        vectors='glove.test_twitter.27B.200d')

        self.assertEqual(v.itos, ['<unk>', '<pad>', '<bos>',
                                  'ᑌᑎIᑕOᗪᕮ_Tᕮ᙭T', 'hello', 'world'])
        vectors = v.vectors.numpy()

        # The first 5 entries in each vector.
        expected_glove_twitter = {
            'hello': [0.34683, -0.19612, -0.34923, -0.28158, -0.75627],
            'world': [0.035771, 0.62946, 0.27443, -0.36455, 0.39189],
        }

        for word in ['hello', 'world']:
            self.assertTrue(
                np.allclose(
                    vectors[v.stoi[word], :5], expected_glove_twitter[word]
                )
            )

        self.assertTrue(np.allclose(vectors[v.stoi['<unk>'], :], np.zeros(200)))
