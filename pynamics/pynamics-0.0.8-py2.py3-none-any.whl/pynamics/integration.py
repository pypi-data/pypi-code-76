import pynamics
import numpy
import logging
logger = logging.getLogger('pynamics.integration')

def integrate(*args,**kwargs):
    if pynamics.integrator==0:
        return integrate_odeint(*args,**kwargs)
    elif pynamics.integrator==1:
        newargs = args[0],args[2][0],args[1],args[2][-1]
        return integrate_rk(*newargs ,**kwargs)



def integrate_odeint(*arguments,**keyword_arguments):
    import scipy.integrate
    
    logger.info('beginning integration')
    result = scipy.integrate.odeint(*arguments,**keyword_arguments)
    logger.info('finished integration')
    return result

def integrate_rk(*arguments,**keyword_arguments):
    import scipy.integrate
    
    logger.info('beginning integration')
    try:
        result = scipy.integrate.RK45(*arguments,**keyword_arguments)
        y = [result.y]
        while True:
            result.step()
            y.append(result.y)
    except RuntimeError:
        pass
    logger.info('finished integration')
    return y
