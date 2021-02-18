import numpy as np

from scipy.stats import norm


def boot(entity, x, alp, beta, num, k):
    if hasattr(k, "__iter__"):
        if len(k) == 0:
            return [(np.infty, 0, 0)]

        return np.array([boot(entity, x, alp, beta, num, i) for i in k])

    try:
        k1 = int(k * (x.size ** ((1 - beta) * alp)))
        n1 = int(x.size ** beta)
        if k1 + 1 > n1:
            k1 = n1 - 1

        ga = []
        for _ in np.arange(num):
            sub_x = np.array(
                [x[i] for i in np.random.choice(np.arange(0, x.size), n1, replace=True)]
            )
            sub_x.sort()
            ga.append(entity.estimate(sub_x, k1))

        ga = np.array(ga)
        real = entity.estimate(x, k)
        bias = (np.mean(np.where(np.isnan(ga), real-10, ga)) - real) ** 2
        vr = np.var(np.where(np.isnan(ga), np.nanmean(ga), ga))
        return vr + bias, real, np.sqrt(vr)
    except Exception as error:
        print(error)
        return np.infty, 0, 0
    except OverflowError as error:
        print(error)
        return np.infty, 0, 0


def boot_estimate(entity, x, alp, beta, num, speed=True, pers=0.05):
    k = entity.get_k(x, boot=True)
    x_ = entity.prepare(x)

    if len(k) < 2:
        return None, 0, (0, 0)

    if speed:
        count = 0
        mse, alpr, dls = boot(entity, x_, alp, beta, num, k[0])
        k_opt = k[0]

        for k_ in k:
            mse_, alp_, dls_ = boot(entity, x_, alp, beta, num, k_)

            if mse_ < mse:
                mse = mse_
                alpr = alp_
                k_opt = k_
                count = 0
                dls = dls_
            else:
                count += 1

            if count == int(0.1 * k.size) or count == 100:
                break
        return (
            alpr,
            k_opt,
            (alpr - dls * norm.ppf(1 - pers), alpr - dls * norm.ppf(pers)),
        )

    mses, alps, dls = zip(*boot(entity, x_, alp, beta, num, k))
    if len(mses) == 1:
        return mses[0], alps[0], (alps[0], alps[0])
    ar = np.argmin(mses)
    return (
        alps[ar],
        k[ar],
        (
            alps[ar] - dls[ar] * norm.ppf(1 - (pers / 2)),
            alps[ar] - dls[ar] * norm.ppf(pers / 2),
        ),
    )
