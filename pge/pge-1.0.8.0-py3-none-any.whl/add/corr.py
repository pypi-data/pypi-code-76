import numpy as np

from dtg.dependence.acf import acf


def autocorrelation(graph, attr, h=None):
    nodes = graph.get_ids(stable=True)
    mxes = []

    comms = set([(node,) for node in nodes])
    count = 0
    while count < graph.size():
        print(len(mxes))
        new_comms = set()

        mx = np.max([np.max(graph.get_attributes(attr, comm)) for comm in comms])
        for comm in comms:
            if len(mxes) < count + 1:
                mxes.append(mx)
                new_comms.add(comm)
            else:
                if mxes[count] == mx:
                    new_comms.add(comm)
                if mxes[count] > mx:
                    new_comms = set(comm)
                    mxes[count] = mx

        comms = set()
        for new_comm in new_comms:
            for node_out in graph.get_out_degrees(new_comm, un=True):
                if node_out not in new_comm:
                    comms.add(tuple(np.sort(list(new_comm) + [node_out])))
        count += 1

    return acf(np.array(mxes), h)
