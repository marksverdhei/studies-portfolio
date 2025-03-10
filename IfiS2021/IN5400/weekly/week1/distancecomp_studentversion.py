import os, sys
import numpy as np
import torch
import time


def forloopdists(feats, protos):
    N = feats.shape[0]
    P = protos.shape[0]
    # d with shape N * P
    d = [[0] * N for _ in range(P)]
    for j in range(P):
        for i in range(N):
            diff = feats[i] - protos[j]
            # Since norm involves square root we can skip a computation
            d[j][i] = sum(i**2 for i in diff)

    return d


def numpydists(feats, protos):
    diffs = feats - protos[:, None]
    return (diffs**2).sum(axis=2)


def pytorchdists(feats0, protos0, device):
    feats = torch.from_numpy(feats0)
    protos = torch.from_numpy(protos0)

    diffs = feats - protos[:, None]
    return (diffs**2).sum(axis=2)


def run():
    feats = np.random.normal(size=(50,300)) #5000 instead of 250k for forloopdists
    protos = np.random.normal(size=(20,300))

    since = time.time()
    dists0 = forloopdists(feats, protos)
    dists0 = np.array(dists0)
    time_elapsed = float(time.time()) - float(since)
    print('Comp complete in {:.3f}s'.format( time_elapsed ))


    since = time.time()
    dists2 = numpydists(feats,protos)
    time_elapsed = float(time.time()) - float(since)
    print('Comp complete in {:.3f}s'.format( time_elapsed ))

    np.testing.assert_almost_equal(dists0, dists2)

    device = torch.device('cpu')
    since = time.time()
    dists1 = pytorchdists(feats, protos, device)
    dists1 = dists1.numpy()
    time_elapsed = float(time.time()) - float(since)
    print('Comp complete in {:.3f}s'.format( time_elapsed ))

    print(dists0.shape, dists1.shape, dists2.shape)


if __name__=='__main__':
    run()
