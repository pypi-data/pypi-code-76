from PyLFMF._cppkernel import LFMF, vector_LFMF 
import numpy as np
from numpy.lib import recfunctions as rfn
import pandas as pd

arguments = ['h_tx', 'h_rx', 'freq',
             'power_tx', 'N', 'dist',
             'epsilon', 'sigma', 'polar']
# repr, str
err_msg = 'Incorrect input format. Run help(PyLFMF) for help.'

dt_in = np.dtype([
            ('h_tx', np.double), ('h_rx', np.double), ('freq', np.double),
            ('power_tx', np.double), ('N', np.double), ('dist', np.double),
            ('epsilon', np.double), ('sigma', np.double), ('polar', np.double)
            ])

dt_out = np.dtype([('A', np.double), ('E', np.double), ('P', np.double),
                   ('method', np.double), ('status', np.double)])

def fromarray(data):
    if isinstance(data, list):
        data = np.array(data)
    try:
        data = data.reshape(-1, 9)
        data = rfn.unstructured_to_structured(data, dt_in)
    except:
        raise ValueError(err_msg)
    return data


def frompandas(df, mapper=None):
    if not isinstance(df, pd.DataFrame):
        raise ValueError(err_msg) 
    try:
        if mapper is not None:
            buf = []
            for arg in arguments:
                buf.append(mapper[arg])
            df = df[buf]
        else:
            df = df[arguments]
    except:
        raise ValueError("Mapping column names has failed.")
    df = fromarray(df.to_numpy())
    return df
            
  
def fit(data):
    results = vector_LFMF(data)
    return np.array(results, dtype=dt_out)
	
        
        
def helpin():
    print(
'''
              Low Frequency / Medium Frequency (LF/MF) Propagation Model

|===============================================================================================|
|					INPUTS:							|
|-------------------------------------------------------------|---------------------------------|
|   Variable  |  Type	|  Units  |         Limits	      |	         Description	        |
|-------------|---------|---------|---------------------------|---------------------------------|
| h_tx__meter |	double	|  meter  |   0 <= h_tx__meter <= UB  |	   Height of the transmitter	|
|-------------|---------|---------|---------------------------|---------------------------------|
| h_rx__meter |	double	|  meter  |   0 <= h_rx__meter <= UB  |    Height of the receiver	|
|-------------|---------|---------|---------------------------|---------------------------------|
| f__mhz      |	double	|   MHz	  |   0.01 <= f__mhz <= 30    |    Frequency            	|		
|-------------|---------|---------|---------------------------|---------------------------------|
| P_tx__watt  |	double	|  Watt	  |       0 < P_tx__watt      |	   Transmitter power		|
|-------------|---------|---------|---------------------------|---------------------------------|
| N_s	      |	double	| N-Units |     250 <= N_s <= 400     |    Surface refractivity		|
|-------------|---------|---------|---------------------------|---------------------------------|
| d__km	      |	double	|   km	  |        0 < d__km	      |	   Path distance		|
|-------------|---------|---------|---------------------------|---------------------------------|
| epsilon     |	double	|         |       1 <= epsilon	      |	   Relative permittivity	|
|-------------|---------|---------|---------------------------|---------------------------------|
| sigma       |	double	|   S/m	  |        0 < sigma	      |	   Conductivity			|
|-------------|---------|---------|---------------------------|---------------------------------|
| pol	      |	 int	|	  | 	 0 = Horizontal       |    Polarization			|
|	      |		|	  |	 1 = Vertical	      |		   			|
|-------------|---------|---------|---------------------------|---------------------------------|
|  UB - upper bound is calculated according to the Handbook on Ground Wave Propagation	        |
|       published by The International Telecommunication Union (ITU):			        |
|       For epsilon << 60 * sigma * lambda: UB = 1.2 * sigma^{1/2} * lambda^{3/2}         	|
|-----------------------------------------------------------------------------------------------|	
''')
    return

def helpout():
    print(
'''
|=======================================================================================|
|				   OUTPUTS						|
|==========|========|============|======================================================|
| Variable |  Type  |   Unit     | 	               Description			|
|----------|------- |------------|------------------------------------------------------|
|    A	   | double |	dB	 | 	Basic transmission loss				|
|----------|--------|------------|------------------------------------------------------|
|    E	   | double |	dB(uV/m) |	Electrice field strength			|
|----------|--------|------------|------------------------------------------------------|
|    P	   | double |	 dBm	 |	Received power					|
|----------|--------|------------|------------------------------------------------------|
|  method  |  int   |		 |	Solution method					|
|	   | 	    |		 |	0 = Flat earth with curve correction		|
|	   |	    |		 |	1 = Residue series				|
|----------|--------|------------|------------------------------------------------------|
|  status  |  int   |		 |	0 = SUCCESS					|
|	   |	    |		 |	2000 = Upper bound for h_tx__meter is used	|
|	   |  	    |		 |	2001 = Upper bound for h_rx__meter is used	|
|	   |	    |		 |	2002 = Upper bound for h_tx__meter is used	| 				
|	   |        |            |	1000 = TX terminal height is out of range	|
|          |        |            |      1001 = RX terminal height is out of range	|
|	   |	    |	   	 |	1002 = Frequency is out of range		|
|	   |	    |		 |	1003 = Transmit power is out of range		|
|	   |	    |		 |	1004 = Surface refractivity is out of range	|
| 	   |	    |		 |	1005 = Path distance is out of range		|		
|	   |	    | 		 |	1006 = Epsilon is out of range			|
|	   |	    |		 |	1007 = Sigma is out of range			|
|	   |	    |		 |	1008 = Invalid value for polarization		|
|----------|--------|------------|------------------------------------------------------|
''')
    return
