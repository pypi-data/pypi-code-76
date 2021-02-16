#
#    (C) Quantum Computing Inc., 2020.
#
#    THIS IS UNPUBLISHED PROPRIETARY SOURCE CODE of the Copyright Holder. 
#    The contents of this file may not be disclosed to third parties, copied 
#    or duplicated in any form, in whole or in part, without the prior written
#    permission of the Copyright Holder.
#
import base64
from io import BytesIO

import numpy as np
import scipy.sparse as sp
import networkx as nx


def encode_data(data):
    if isinstance(data, sp.spmatrix):
        return encode_sparse_array(data)
    elif isinstance(data, dict):
        return encode_dict(data)
    else:
        return base64.b64encode(data).decode('utf-8')


def encode_dict(data):
    qubo_str = str(data).encode('utf-8')
    return encode_data(qubo_str)


def encode_ndarray(qubo: np.ndarray) -> bytes:
    fbytes = BytesIO()
    #######
    # To extract:
    # arrdata = np.load('fname.npz')['data']
    np.savez_compressed(fbytes, data=qubo)
    return fbytes.getvalue()


def encode_graph(graph: nx.Graph) -> bytes:
    fbytes = BytesIO()
    #######
    # To extract:
    # arrdata = np.load('fname.npz')['data']
    nx.write_gpickle(graph, fbytes)
    return fbytes.getvalue()


def encode_sparse_array(qubo: sp.spmatrix) -> bytes:
    fbytes = BytesIO()
    ########
    # To extract:
    #   arrdata = sp.load_npz('fname.npz')
    sp.save_npz(fbytes, qubo, compressed=True)
    return fbytes.getvalue()

