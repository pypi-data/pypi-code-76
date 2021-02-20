# -*- coding: iso-8859-1 -*-
"""
Montrix MxDevTool Python Library
"""

from datetime import datetime
import sys
from .mxdevtool import *
from .mxdevtool import _mxdevtool
# from .utils import *
del sys

__author__ = 'Montrix Ltd.'
__email__ = 'master@montrix.co.kr'

if hasattr(_mxdevtool,'__version__'):
    __version__ = _mxdevtool.__version__
elif hasattr(_mxdevtool.cvar,'__version__'):
    __version__ = _mxdevtool.cvar.__version__
else:
    print('Could not find __version__ attribute')


__license__ = """
MxDevTool Non-Commercial Software License Agreement

This Non-Commercial Software License Agreement (Agreement) is between 
Montrix limited liability company(MTX) and you, the entity or individual 
entering into this Agreement (User). The MxDevTool software and documentation 
provided to User (Software) are licensed and are not sold. This Agreement is 
part of a package that includes MxDevTool Software and certain electronic 
and/or written materials. This Agreement covers your permitted download, 
installation and use of the MxDevTool licensed materials and the MxDevTool
Software. BY "INSTALLING" THE SOFTWARE YOU ACKNOWLEDGE AND AGREE THAT YOU 
HAVE READ ALL OF THE TERMS AND CONDITIONS OF THIS AGREEMENT, UNDERSTAND 
THEM, AND AGREE TO BE LEGALLY BOUND BY THEM. If you do not agree with the
terms of this Agreement, you may not, install or use the MxDevTool licensed 
materials or the MxDevTool Software.

General. A non-exclusive, nontransferable, perpetual license is
granted to the Licensee to install and use the Software for academic,
non-profit, or government-sponsored research purposes. Use of the
Software under this License is restricted to non-commercial purposes.
Commercial use of the Software requires a separately executed written
license agreement.

Permitted Use and Restrictions. Licensee agrees that it will
use the Software, and any modifications, improvements, or derivatives
to the Software that the Licensee may create (collectively,
"Improvements") solely for internal, non-commercial purposes and shall
not distribute or transfer the Software or Improvements to any person
or third parties without prior written permission from The Montrix. The
term "non-commercial," as used in this License, means academic or other
scholarly research which (a) is not undertaken for profit, or (b) is
not intended to produce works, services, or data for commercial use, or
(c) is neither conducted, nor funded, by a person or an entity engaged
in the commercial use, application or exploitation of works similar to
the Software.

Ownership and Assignment of Copyright. The Licensee acknowledges
that The Montrix hold copyright in the Software and associated
documentation, and the Software and associated documentation are the
property of The Montrix. The Licensee agrees that any Improvements made
by Licensee shall be subject to the same terms and conditions as the
Software. Licensee agrees not to assert a claim of infringement in
Licensee copyrights in Improvements in the event The Montrix prepares
substantially similar modifications or derivative works.  The Licensee
agrees to use his/her reasonable best efforts to protect the contents
of the Software and to prevent unauthorized disclosure by its agents,
officers, employees, and consultants. If the Licensee receives a request
to furnish all or any portion of the Software to a third party, Licensee
will not fulfill such a request but will refer the third party to the
http://www.montrix.co.kr/ Montrix web page</a>
so that the third party's use of this Software will be subject to the
terms and conditions of this License.  Notwithstanding the above,
Licensee may disclose any Improvements that do not involve disclosure
of the Software.

Copies. The Licensee may make a reasonable number of copies of
the Software for the purposes of backup, maintenance of the Software or
the development of derivative works based on the Software. These
additional copies shall carry the copyright notice and shall be
controlled by this License, and will be destroyed along with the
original by the Licensee upon termination of the License.

Acknowledgement. Licensee agrees that any publication of
results obtained with the Software will acknowledge its use by an
appropriate citation as specified in the documentation.

Disclaimer of Warranties and Limitation of Liability. THE
LICENSEE AGREES THAT ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT
NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
FOR A PARTICULAR PURPOSE ARE DISCLAIMED. THE MONTRIX MAKES NO
REPRESENTATION OR WARRANTY THAT THE SOFTWARE WILL NOT INFRINGE ANY
PATENT OR OTHER PROPRIETARY RIGHT.  IN NO EVENT SHALL THE MONTRIX BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Termination. This License is effective until terminated by
either party.  Licensee's rights under this License will terminate
automatically without notice from The Montrix if Licensee fails to comply
with any term(s) of this License. Licensee may terminate the License by
giving written notice of termination to The Montrix. Upon termination
of this License, Licensee shall immediately discontinue all use of the
Software and destroy the original and all copies, full or partial, of
the Software, including any modifications or derivative works, and
associated documentation.

Governing Law and General Provisions. This License shall be
governed by the laws of the South Korea, excluding the application of its 
conflicts of law rules. If any provisions of this License are held invalid or
unenforceable for any reason, the remaining provisions shall remain in
full force and effect. This License is binding upon any heirs and
assigns of the Licensee. The License granted to Licensee hereunder may
not be assigned or transferred to any other person or entity without
the express consent of The Montrix.  This License constitutes the
entire agreement between the parties with respect to the use of the
Software licensed hereunder and supersedes all other previous or
contemporaneous agreements or understandings between the parties,
whether verbal or written, concerning the subject matter. Any
translation of this License is done for local requirements and in the
event of a dispute between the English and any non-English versions,
the English version of this License shall govern.
"""

def default_calendar() -> Calendar:
    import locale

    locale = locale.getdefaultlocale()
    lang = locale[0]

    if lang == '':
        return UnitedStates()
    else:
        return SouthKorea()


# def get_argType_fromName(name):
#     if 'Curve' == arg[-len('Curve'):]:
#         return 'Curve'
#     elif 'Ts' == arg[-len('Ts'):]:
#         return 'Ts'
#     elif 'Para' == arg[-len('Para'):]:
#         return 'Para'
#     elif 'Date' == arg[-len('Date'):]:
#         return 'Date'
#     elif 'compounding' == arg or 'Compounding' == arg[-len('Compounding'):]:
#         return 'Compounding'
#     elif 'Tenor' == arg[-len('Tenor'):]:
#         return 'Tenor'
#     else:
#         return 'Double'


def check_fromDict(d: dict, key, v):

    if not isinstance(d, dict):
        raise Exception('dictionary type is required - {0}'.format(d))

    if not key in d:
        raise KeyError(key, d)
    
    if d[key] != v:
        raise Exception('class type is invalid - {0}, {1} -> input_d - {2}'.format(d[key], v, d))


# market_data
class MarketData:

    CTG_QUOTE_NAME = 'quote'
    CTG_YIELDCURVE_NAME = 'yieldCurve'
    CTG_VOLTS_NAME = 'volTs'

    def __init__(self, data=None):
        if data is None:
            self.initialize()
        else:
            self.__dict__ = data

    def initialize(self):
        self.quote = dict()
        self.yieldCurve = dict()
        self.volTs = dict()
        self.timestamp = None

    @staticmethod
    def fromDict(d: dict):
        return MarketData(d)

    def toDict(self):
        import copy
        return copy.deepcopy(self.__dict__)

    def clone(self):
        return MarketData(self.toDict())
    
    def hashCode(self) -> str:
        from .utils import get_hashCode
        return get_hashCode(self)

    def get_quote_d(self, arg):
        if not isinstance(arg, str):
            return arg

        if not arg in self.quote:
            raise Exception('no exist marketdata(quote) - {0} -> all quote data: {1}'.format(arg, self.quote))
        
        return self.quote[arg]

    def get_quote_v(self, arg):
        if not isinstance(arg, str):
            return arg

        if not arg in self.quote:
            raise Exception('no exist marketdata(quote) - {0} -> all quote data: {1}'.format(arg, self.quote))
        
        return self.quote[arg]['v']

    # def get_quote(self, arg):
    #     from mxdevtool.quotes import parseClassFromDict
    #     return parseClassFromDict(self.get_quote_d(arg))

    def get_yieldCurve_d(self, arg):
        if not isinstance(arg, str):
            return arg
            
        if not arg in self.yieldCurve:
            raise Exception('no exist marketdata(yieldCurve) - {0} -> all yieldCurve data: {1}'.format(arg, self.yieldCurve))
        
        return self.yieldCurve[arg]

    def get_yieldCurve(self, arg) -> YieldTermStructure:
        from mxdevtool.xenarix import parseClassFromDict
        return parseClassFromDict(self.get_yieldCurve_d(arg))

    def get_volTs_d(self, arg):
        if not isinstance(arg, str):
            return arg

        if not arg in self.volTs:
            raise Exception('no exist marketdata(volTs) - {0} -> all volTs data: {1}'.format(arg, self.volTs))
        
        return self.volTs[arg]

    def get_volTs(self, arg):
        from mxdevtool.xenarix import parseClassFromDict
        return parseClassFromDict(self.get_volTs_d(arg))
    
    # for intellisense
    def get_volTs_black(self, arg) -> BlackVolTermStructure: 
        volts = self.get_volTs(arg)
       
        if not isinstance(volts, BlackVolTermStructure):
            raise Exception('BlackVolTermStructure type is required - {0}'.format(type(volts)))

        return volts

    def get_volTs_ir(self, arg):
        pass

    def get_all_d(self, pattern=None):
        d = { 
            **self.quote,
            **self.yieldCurve,
            **self.volTs,
        }

        if pattern is None:
            return d

        # pattern 
        from fnmatch import fnmatch
        
        res = dict()

        for k, v in d.items():
            if fnmatch(pattern):
                res[k] = v

        return res


# default market data
# inheritance is needed for using
class MarketDataProvider:
    def __init__(self):
        pass

    def initialize(self):
        pass



    def get_data(self, **kwargs):
        pass

    def add_request_qt(self, name, **kwargs):
        pass

    def add_request_yc(self, name, **kwargs):
        pass

    def add_request_vts(self, name, **kwargs):
        pass

    def remove_request(self, **kwargs):
        pass    


# wrapping
class TimeEqualGrid(core_TimeEqualGrid):
    def __init__(self, refDate=Date.todaysDate(), maxYear=10, nPerYear=12):
        self._refDate = refDate
        self._maxYear = maxYear
        self._nPerYear = nPerYear
        
        core_TimeEqualGrid.__init__(self, refDate, maxYear, nPerYear)

    @staticmethod
    def fromDict(d: dict):
        check_fromDict(d, CLASS_TYPE_NAME, TimeEqualGrid.__name__)

        refDate = Date(d['refDate'])
        maxYear = d['maxYear']
        nPerYear = d['nPerYear']

        return TimeEqualGrid(refDate, maxYear, nPerYear)

    def toDict(self):
        res = dict()

        res[CLASS_TYPE_NAME] = self.__class__.__name__
        res['refDate'] = str(self._refDate)
        res['maxYear'] = self._maxYear
        res['nPerYear'] = self._nPerYear

        return res


class TimeArrayGrid(core_TimeArrayGrid):
    def __init__(self, refDate=Date.todaysDate(), times=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]):

        self._refDate = refDate
        self._times = times

        core_TimeArrayGrid.__init__(self, refDate, times)

    @staticmethod
    def fromDict(d: dict):
        check_fromDict(d, CLASS_TYPE_NAME, TimeArrayGrid.__name__)

        refDate = Date(d['refDate'])
        times = d['times']
        
        return TimeArrayGrid(refDate, times)

    def toDict(self):
        res = dict()

        res[CLASS_TYPE_NAME] = self.__class__.__name__
        res['refDate'] = str(self._refDate)
        res['times'] = self._times

        return res


class TimeGrid(core_TimeGrid):
    def __init__(self, refDate=Date.todaysDate(), maxYear=10, frequency_type='annual', frequency_month=1, frequency_day=1):

        self._refDate = refDate
        self._maxYear = maxYear
        self._frequency_type = frequency_type
        self._frequency_month = frequency_month
        self._frequency_day = frequency_day

        core_TimeGrid.__init__(self, refDate, maxYear, frequency_type, frequency_month, frequency_day)

    @staticmethod
    def fromDict(d: dict):
        check_fromDict(d, CLASS_TYPE_NAME, TimeGrid.__name__)

        refDate = Date(d['refDate'])
        maxYear = d['maxYear']
        frequency_type = d['frequency_type']
        frequency_month = d['frequency_month']
        frequency_day = d['frequency_day']

        return TimeGrid(refDate, maxYear, frequency_type, frequency_month, frequency_day)

    def toDict(self):
        res = dict()

        res[CLASS_TYPE_NAME] = self.__class__.__name__
        res['refDate'] = str(self._refDate)
        res['maxYear'] = self._maxYear
        res['frequency_type'] = self._frequency_type
        res['frequency_month'] = self._frequency_month
        res['frequency_day'] = self._frequency_day

        return res


class ManagerBase:
    def __init__(self, config):
        self.config = config

