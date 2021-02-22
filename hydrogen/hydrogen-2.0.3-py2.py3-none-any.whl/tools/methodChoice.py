#!/usr/data/env python3
# -*- coding: utf-8 -*-
"""
Method repository for the sampling of number of events

author: Bruno Hadengue, bruno.hadengue@eawag.ch

Documentation Update: 4th Feb 2019.
"""

import numpy as np
from scipy.stats import truncnorm, lognorm

def method_nb_truncNorm(df, eventType, nbInhabitants):
    """
    Samples the number of events from a truncated normal distribution
    """
    try:
        return int(round(truncnorm.rvs(a=(eventType.nbEvents.lower-eventType.nbEvents.loc)/eventType.nbEvents.scale, #a and b bounds are defined over the standard normal distribution, hence
                            b=(eventType.nbEvents.upper-eventType.nbEvents.loc)/eventType.nbEvents.scale,  #the conversion using the mean and scale.
                            loc=eventType.nbEvents.loc, scale=eventType.nbEvents.scale)))  #truncated normal distribution
    except:
        raise ValueError("Problem occurred with '{}' method in 'nbEvents'. Please check initFile".format(eventType.nbEvents.method))

def method_nb_truncNormPerCap(df, eventType, nbInhabitants):
    """
    Samples the number of events from a truncated normal distribution for each inhabitant
    """
    try:
        nbEvents = 0
        try:
            for i in range(1, nbInhabitants+1, 1):
                nbEvents += int(round(truncnorm.rvs(a=(eventType.nbEvents.lower-eventType.nbEvents.loc)/eventType.nbEvents.scale, #a and b bounds are defined over the standard normal distribution, hence
                                        b=(eventType.nbEvents.upper-eventType.nbEvents.loc)/eventType.nbEvents.scale,  #the conversion using the mean and scale.
                                        loc=eventType.nbEvents.loc, scale=eventType.nbEvents.scale)))  #truncated normal distribution
        except TypeError:
            nbInhabitants = int(round(truncnorm.rvs(a=(nbInhabitants[2]-nbInhabitants[0])/nbInhabitants[1], #a and b bounds are defined over the standard normal distribution, hence
                                    b=(nbInhabitants[3]-nbInhabitants[0])/nbInhabitants[1],  #the conversion using the mean and scale.
                                    loc=nbInhabitants[0], scale=nbInhabitants[1])))  #truncated normal distribution))
            for i in range(1, nbInhabitants+1, 1):
                nbEvents += int(round(truncnorm.rvs(a=(eventType.nbEvents.lower-eventType.nbEvents.loc)/eventType.nbEvents.scale, #a and b bounds are defined over the standard normal distribution, hence
                                        b=(eventType.nbEvents.upper-eventType.nbEvents.loc)/eventType.nbEvents.scale,  #the conversion using the mean and scale.
                                        loc=eventType.nbEvents.loc, scale=eventType.nbEvents.scale)))  #truncated normal distribution
        return nbEvents
    except:
        raise ValueError("Problem occurred with '{}' method in 'nbEvents'. Please check initFile".format(eventType.nbEvents.method))

def method_nb_lognormal(df, eventType, nbInhabitants):
    """
    Samples the number of events from a lognormal distribution
    """
    try:
        return int(round(np.random.lognormal(mean=eventType.nbEvents.mean, sigma=eventType.nbEvents.sigma)))
    except:
        raise ValueError("Problem occurred with '{}' method in 'nbEvents'. Please check initFile".format(eventType.nbEvents.method))


def method_nb_truncLognormal(df, eventType, nbInhabitants):
    """
    Samples the number of events from a truncated lognormal distribution
    """
    try:
        cdfUp = lognorm.cdf(eventType.nbEvents.upper, eventType.nbEvents.sigma, scale=eventType.nbEvents.scale)
        cdfDown = lognorm.cdf(eventType.nbEvents.lower, eventType.nbEvents.sigma, scale=eventType.nbEvents.scale)
        return int(round(lognorm.ppf((cdfUp-cdfDown)*np.random.rand()+cdfDown, eventType.nbEvents.sigma, scale=eventType.nbEvents.scale)))
    except:
        raise ValueError("Problem occurred with '{}' method in 'nbEvents'. Please check initFile".format(eventType.nbEvents.method))

def method_nb_truncLognormalPerCap(df, eventType, nbInhabitants):
    """
    Samples the number of events from a truncated lognormal distribution for each inhabitant
    """
    try:
        nbEvents = 0
        try:
            for i in range(1, nbInhabitants+1, 1):
                cdfUp = lognorm.cdf(eventType.nbEvents.upper, eventType.nbEvents.sigma, scale=eventType.nbEvents.scale)
                cdfDown = lognorm.cdf(eventType.nbEvents.lower, eventType.nbEvents.sigma, scale=eventType.nbEvents.scale)
                nbEvents += int(round(lognorm.ppf((cdfUp-cdfDown)*np.random.rand()+cdfDown, eventType.nbEvents.sigma, scale=eventType.nbEvents.scale)))
            return nbEvents
        except TypeError:
            nbInhabitants = int(round(truncnorm.rvs(a=(nbInhabitants[2]-nbInhabitants[0])/nbInhabitants[1], #a and b bounds are defined over the standard normal distribution, hence
            b=(nbInhabitants[3]-nbInhabitants[0])/nbInhabitants[1],  #the conversion using the mean and scale.
            loc=nbInhabitants[0], scale=nbInhabitants[1])))  #truncated normal distribution))
            for i in range(1, nbInhabitants+1, 1):
                cdfUp = lognorm.cdf(eventType.nbEvents.upper, eventType.nbEvents.sigma, scale=eventType.nbEvents.scale)
                cdfDown = lognorm.cdf(eventType.nbEvents.lower, eventType.nbEvents.sigma, scale=eventType.nbEvents.scale)
                nbEvents += int(round(lognorm.ppf((cdfUp-cdfDown)*np.random.rand()+cdfDown, eventType.nbEvents.sigma, scale=eventType.nbEvents.scale)))
            return nbEvents
    except:
        raise ValueError("Problem occurred with '{}' method in 'nbEvents'. Please check initFile".format(eventType.nbEvents.method))

def method_nb_poissonPerCap(df, eventType, nbInhabitants):
    """
    Determines number of events using a poisson process for each inhabitant
    """
    try:
        rate = df[eventType.type].sum()/eventType.nbEvents.avgEventVol
        if isinstance(nbInhabitants, list):
            nbInhabitants = int(round(truncnorm.rvs(a=(nbInhabitants[2]-nbInhabitants[0])/nbInhabitants[1], #a and b bounds are defined over the standard normal distribution, hence
                                    b=(nbInhabitants[3]-nbInhabitants[0])/nbInhabitants[1],  #the conversion using the mean and scale.
                                    loc=nbInhabitants[0], scale=nbInhabitants[1])))  #truncated normal distribution))
            return np.random.poisson(rate*nbInhabitants)
        else:
            return np.random.poisson(rate*nbInhabitants)
    except:
        raise ValueError("Problem occurred with '{}' method in 'nbEvents'. Please check initFile".format(eventType.nbEvents.method))

def method_nb_poisson(df, eventType, nbInhabitants):
    """
    Determines a number of events using a poisson process.
    """
    try:
        rate = df[eventType.type].sum()/eventType.nbEvents.avgEventVol
        return np.random.poisson(rate)
    except:
        raise ValueError("Problem occurred with '{}' method in 'nbEvents'. Please check initFile".format(eventType.nbEvents.method))

def method_nb_constant(df, eventType, nbInhabitants):
    """
    Sets a value for the number of events.
    """
    try:
        return eventType.nbEvents.value
    except:
        raise ValueError("Problem occurred with '{}' method in 'nbEvents'. Please check initFile".format(eventType.nbEvents.method))

def method_nb_list(df, eventType, nbInhabitants):
    """
    Samples number of events from a list
    """
    try:
        try:
            return np.random.choice(eventType.nbEvents.list, p=eventType.nbEvents.p)
        except:
            try:
                eventType.nbEvents.p
                print("Warning: uniform list sampling! Probability list dist.p has wrong format or sum is not equal 1")
                return np.random.choice(eventType.nbEvents.list)
            except AttributeError:
                return np.random.choice(eventType.nbEvents.list)
    except:
        raise ValueError("Problem occurred with '{}' method in 'nbEvents'. Please check initFile".format(eventType.nbEvents.method))

def method_nb_listPerCap(df, eventType, nbInhabitants):
    """
    Samples number of events from a list for each inhabitant
    """
    try:
        nbEvents = 0
        try:
            for i in range(1, nbInhabitants+1, 1):
                try:
                    nbEvents += np.random.choice(eventType.nbEvents.list, p=eventType.nbEvents.p)
                except:
                    try:
                        eventType.nbEvents.p
                        print("Warning: uniform list sampling! Probability list dist.p has wrong format or sum is not equal 1")
                        nbEvents += np.random.choice(eventType.nbEvents.list)
                    except AttributeError:
                        nbEvents += np.random.choice(eventType.nbEvents.list)
        except TypeError:
            nbInhabitants = int(round(truncnorm.rvs(a=(nbInhabitants[2]-nbInhabitants[0])/nbInhabitants[1], #a and b bounds are defined over the standard normal distribution, hence
                                    b=(nbInhabitants[3]-nbInhabitants[0])/nbInhabitants[1],  #the conversion using the mean and scale.
                                    loc=nbInhabitants[0], scale=nbInhabitants[1])))  #truncated normal distribution))
            #print(nbInhabitants)
            for i in range(1, nbInhabitants+1, 1):
                    try:
                        nbEvents += np.random.choice(eventType.nbEvents.list, p=eventType.nbEvents.p)
                        #print("nbEventstmp : {}".format(nbEvents))
                    except:
                        try:
                            eventType.nbEvents.p
                            print("Warning: uniform list sampling! Probability list dist.p has wrong format or sum is not equal 1")
                            nbEvents += np.random.choice(eventType.nbEvents.list)
                        except AttributeError:
                            nbEvents += np.random.choice(eventType.nbEvents.list)
        return nbEvents
    except:
        raise ValueError("Problem occurred with '{}' method in 'nbEvents'. Please check initFile".format(eventType.nbEvents.method))

def method_nb_dummy(df, eventType, nbInhabitants):
    """
    Sets a dummy number of events
    """
    print("unrecognized method. Dummy number of events chosen: 4")
    return 4


def method_dist_loglogistic(dist):
    """
    Samples float value from a loglogistic distribution

    ATTENTION: this is a logistic and not a log-logistic. Log-logistic parameters must be transformed into logistic parameters first:
    loc_new = np.log(loc_before)
    scale_new = 1/scale.before
    """
    try:
        loc = np.log(dist.loc)
        scale = 1./dist.scale
        # print("parameters have been newly computed to %f, %f" %(loc, scale))
        return np.exp(np.random.logistic(loc=loc, scale=scale))
    except:
        raise ValueError("dist.loc or dist.scale is not available or format is wrong. Please check initFile")

def method_dist_truncNorm(dist):
    """
    Samples float value from a truncated normal distribution
    """
    try:
        return truncnorm.rvs(a=(dist.lower-dist.loc)/dist.scale, b=(dist.upper-dist.loc)/dist.scale,loc=dist.loc, scale=dist.scale)
    except:
        raise ValueError("dist.loc, dist.scale, dist.lower or dist.upper is not available or format is wrong for '{}' distribution. Please check initFile".format(dist.dist))

def method_dist_weibull(dist):
    """
    Samples float value from a Weibull distribution
    """
    try:
        return dist.scale*np.random.weibull(dist.shape)
    except:
        raise ValueError("dist.shape or dist.scale is not available or format is wrong for '{}' distribution. Please check initFile".format(dist.dist))

def method_dist_gamma(dist):
    """
    Samples float value from a Gamma distribution
    """
    try:
        return np.random.gamma(shape=dist.shape, scale=dist.scale)
    except:
        raise ValueError("dist.shape or dist.scale is not available or format is wrong for '{}' distribution. Please check initFile".format(dist.dist))

def method_dist_normal(dist):
    """
    Samples float value from a normal distribution
    """
    try:
        return np.random.normal(loc=dist.loc, scale=dist.scale)
    except:
        raise ValueError("dist.loc or dist.scale is not available or format is wrong for '{}' distribution. Please check initFile".format(dist.dist))

def method_dist_lognormal(dist):
    """
    Samples float value from a lognormal distribution
    """
    try:
        return np.random.lognormal(mean=dist.mean, sigma=dist.sigma)
    except:
        raise ValueError("dist.mean or dist.sigma is not available or format is wrong for '{}' distribution. Please check initFile".format(dist.dist))

def method_dist_constant(dist):
    """
    Sets a constant value
    """
    try:
        return dist.value
    except:
        raise ValueError("dist.value is not available or format is wrong for '{}' distribution. Please check initFile".format(dist.dist))

def method_dist_uniform(dist):
    """
    Samples float value from a uniform distribution
    """
    try:
        return np.random.uniform(low=dist.low, high=dist.high)
    except:
        raise ValueError("dist.low or dist.high is not available or format is wrong for '{}' distribution. Please check initFile".format(dist.dist))

def method_dist_rayleigh(dist):
    """
    Samples float value from a Rayleigh distribution
    """
    try:
        return np.random.rayleigh(scale=dist.scale)
    except:
        raise ValueError("dist.scale is not available or format is wrong for '{}' distribution. Please check initFile".format(dist.dist))

def method_dist_list(dist):
    """
    Samples float value from a list
    """
    try:
        try:
            return np.random.choice(dist.list, p=dist.p)
        except:
            try:
                dist.p
                print("Warning: uniform list sampling! Probability list dist.p has wrong format or sum is not equal 1")
                return np.random.choice(dist.list)
            except AttributeError:
                return np.random.choice(dist.list)
    except:
        raise ValueError("dist.list is not available or format is wrong for '{}' distribution. Please check initFile".format(dist.dist))

def method_dist_truncLognormal(dist):
    """
    Samples float value from a truncated lognormal distribution
    """
    try:
        cdfUp = lognorm.cdf(dist.upper, dist.sigma, scale=dist.scale)
        cdfDown = lognorm.cdf(dist.lower, dist.sigma, scale=dist.scale)
        return lognorm.ppf((cdfUp-cdfDown)*np.random.rand()+cdfDown, dist.sigma, scale=dist.scale)
    except:
        raise ValueError("dist.upper, dist.sigma, dist.scale or dist.lower is not available or format is wrong for '{}' distribution. Please check initFile".format(dist.dist))
