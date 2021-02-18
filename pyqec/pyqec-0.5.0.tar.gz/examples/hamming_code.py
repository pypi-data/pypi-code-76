from pyqec.sparse import BinaryMatrix, BinaryVector
from pyqec.classical import LinearCode, BinarySymmetricChannel
from pyqec.experiments import ClassicalDecodingExperiment, Laboratory

import matplotlib.pyplot as plt

parity_check_matrix = BinaryMatrix(
    7,
    [
        [3, 4, 5, 6],
        [1, 2, 5, 6],
        [0, 2, 4, 6]
    ]
)
hamming_code = LinearCode(
    parity_check_matrix, 
    tag="Hamming code"
)

class HammingDecoder:
    def __init__(self, code):
        self.code = code

    def decode(self, message):
        syndrome = self.code.syndrome_of(message)
        bit = self.bit_to_flip(syndrome)
        if bit:
            # To flip the bit, we addition a vector with a single 1 at the corresponding position.
            return message + BinaryVector(7, [bit])
        else:
            # It is already a codeword.
            return message

    def bit_to_flip(self, syndrome):
        bit_to_flip = 0
        for unsatisfied_position in syndrome:
            # The smallest position correspond 
            # to the highest power of 2.
            bit_to_flip += 2**(len(syndrome) - 1 - unsatisfied_position)
        if bit_to_flip > 0:
            # We offset because binary vector are 0-indexed.
            return bit_to_flip - 1 
        else:
            # There is no bit to flip
            return None

decoder = HammingDecoder(hamming_code)

def build_experiment(probability):
    noise = BinarySymmetricChannel(probability)
    return ClassicalDecodingExperiment(hamming_code, decoder, noise)

labo = Laboratory(4)

probabilities = [0.05 * i for i in range(1, 21)]

for probability in probabilities:
    labo.add_experiment(build_experiment(probability))

results = labo.run_all_experiments_n_times(500)

results.plot("nice_figure.pdf")

