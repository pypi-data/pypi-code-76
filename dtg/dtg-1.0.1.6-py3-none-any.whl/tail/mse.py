import numpy as np
from scipy.special import erfinv


def estimate_t_p(val):
    return erfinv(2*val-1)*np.sqrt(2)


def estimate_ro_p(val):
    return erfinv(1-val)*np.sqrt(2)


def boot(entity, x, alp, beta, num, k, real=None):
    if hasattr(k, "__iter__"):
        if len(k) == 0:
            return [(np.infty, -1, [])]

        return np.array([boot(entity, x, alp, beta, num, i, entity.estimate(x, i)) for i in k if entity.estimate(x, i) != -1])

    if real is None:
        real = entity.estimate(x, k)
    if real == -1:
        return (np.infty, -1, [])

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
        bias = (np.mean(np.where(ga == -1, real-10, ga)) - real) ** 2
        vr = np.var(np.where(ga == -1, np.mean(ga[ga != -1]), ga))
        return vr + bias, real, ga[ga != -1]
    except Exception as error:
        print(error)
        return np.infty, -1, []
    except OverflowError as error:
        print(error)
        return np.infty, -1, []


def boot_estimate(entity, x, alp, beta, num, speed=True, pers=(0.95, 0.1)):
    k = entity.get_k(x)
    x_ = entity.prepare(x)

    if len(k) < 2:
        return None, 0, (0, 0)

    if speed:
        count = 0
        mse, alpr, dls = boot(entity, x_, alp, beta, num, k[0])

        for k_ in k:
            mse_, alp_, dls_ = boot(entity, x_, alp, beta, num, k_)

            if mse_ < mse:
                mse = mse_
                alpr = alp_
                count = 0
                dls = dls_
            else:
                count += 1

            if count == int(0.1 * k.size) or count == 100:
                break
        alps, mses, dls = [alpr], [mse], [dls]
    else:
        mses, alps, dls = zip(*boot(entity, x_, alp, beta, num, k))

    try:
        ar = np.nanargmin(mses)
        dls = dls[ar]
    except:
        ar = 0
        dls = [alps[ar]]

    t_p = estimate_t_p(pers[0])
    ro_p = estimate_ro_p(pers[1])
    ro = ro_p*(1 + (t_p/np.sqrt(2*num) + ((5*(t_p**2) + 10)/(12 * num))))
    return (
        alps[ar],
        (
            np.mean(dls) - ro * np.std(dls),
            np.mean(dls) + ro * np.std(dls),
        )
    )
