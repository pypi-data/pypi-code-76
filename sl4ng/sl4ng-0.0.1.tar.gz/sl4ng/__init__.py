from typing import Iterable, Any, Iterator, Sequence
import os

from .debug import *
from .files import *
from .functional import *
from .iteration import *
from .maths import *
from .persistance import *
from .stats import *
from .strings import *
from .system import *
from .types import *
from .web import *




HERE,THIS = os.path.split(__file__)


    
    
# def sgm(func:type(lambda:1),iterable:Iterable,arity:int=2) -> Any:
    # """Returns the sum of a iterable through a function, or the range(n) through a function for some integer n
    # Dependencies: itertools.chain
    # In: function, iterable
    # Out: value"""
    # from itertools import chain,combinations
    # if hasattr(iterable,'__iter__') or hasattr(iterable,'__next__'):
        # if isinstance(iterable,str):
            # if iterable.isnumeric():
                # return sum(func(int(i)) for i in iterable)
        # elif all(hasattr(i,'__len__') for i in iterable):
            # if all(len(x)==len(y) for x,y in combinations(iterable,2)):
                # return sum(
                    # func(
                        # *(
                            # v[i] for v in iterable
                        # )
                    # ) for i in range(len(iterable[0]))
                # )
        # else:
            # return sum(func(pair) for pair in combinations(iterable,arity))
    # elif isinstance(iterable,int):
        # return sum(func(i) for i in range(iterable))
    # elif isinstance(iterable,float):
        # return sum(sgm(func,str(iterable).split('.')[0]),sgm(func,str(iterable).split('.')[1]))



# def primes2(n):
#     """Generates a list of primes with n terms
#     Dependencies: factors (from meta)
#     In: int
#     Out: list"""
#     result = []
#     index = 2
#     while len(result) <= n:
#         if len(factors(index)) == 2:
#             result.append(index)
#             index += 1
#     return result
    













    

    
    


if __name__ == "__main__":
    # t = range(10_000_000_000_000)
    # t = range(1_000_000_000)
    # arg = (i for i in t)
    # arg = (1 for i in t)
    # arg = t
    # print(eq(arg))
    # show((list(range(10000)) for i in range(10)),1,False,2,' ',False,True)
    
    # print(entropy(int(i) for i in y))
    
    # v = 15
    # l = []
    # for j in range(1,10):
        # print(sgm(lambda *args:pipe(args),[[1,2,3] for i in range(j)]))
        # l.append(sgm(lambda *args:pipe(args),[range(1,v) for i in range(j)]))
    
    # print(l)
    # print(gcd2(l))
    # [print(i,max(j for j in factors(i) if i>j)) for i in l]
    # print(guid())
    # help(guid)
    # ffplay(r"C:\Users\Kenneth\Downloads\byextension\wav")
    # ffplay(r'F:\Programs\Project Files\FL\2019 old\bisto\bonnuci\blackburn_2\submixes\blackburn_2_Master.wav',hide=False)
    # ffplay(r"C:\Users\Kenneth\Downloads\byextension\wav\alixperez-crooklyn.wav*C:\Users\Kenneth\Downloads\byextension\wav\alixperez-melanie.wav*C:\Users\Kenneth\Downloads\byextension\mkv\Knucks - Home-eKb0XPEnwOk.mkv*C:\Users\Kenneth\Downloads\byextension\mkv\UK Garage - M Dubs - 'Bump n Grind'-fFjWiAR1c-I.mkv*C:\Users\Kenneth\Downloads\byextension\mkv\Ghost - The Club-4_uggscguzs.mkv*C:\Users\Kenneth\Downloads\music\music\Alix Perez\Morning Sun _ Playing Tricks\02 Playing Tricks.mp3*C:\Users\Kenneth\Downloads\music\music\Alix Perez\Morning Sun _ Playing Tricks\01 Morning Sun.mp3*C:\Users\Kenneth\Downloads\music\music\Alix Perez\Dub Rock _ Love Bug\01 Dubrock.mp3*C:\Users\Kenneth\Downloads\music\music\Alix Perez\Dub Rock _ Love Bug\02 Lovebug (feat. Specific).mp3*C:\Users\Kenneth\Downloads\music\music\Unitz\The Drop _ Mornin Blues\01 The Drop.mp3*C:\Users\Kenneth\Music\Collection\Archy Marshall\A New Place 2 Drown\04 Ammi Ammi.mp3*C:\Users\Kenneth\Music\Collection\Archy Marshall\A New Place 2 Drown\09 Empty Vessels.mp3*C:\Users\Kenneth\Downloads\music\music\Belangeo\Unknown Album\belangeo_Tribal.ogg*C:\Users\Kenneth\Music\Collection\Alix Perez\1984\11 Suffer In Silence (feat. Zero T).mp3*C:\Users\Kenneth\Music\Collection\Alix Perez\1984\03 Fade Away.mp3*C:\Users\Kenneth\Music\Collection\Alix Perez\1984\08 I_m Free.mp3*C:\Users\Kenneth\Music\Collection\Alix Perez\1984\15 Hemlines (feat. Sabre).mp3*C:\Users\Kenneth\Downloads\music\music\Alix Perez\Magnolias _ Backlash\02 Backlash.mp3*C:\Users\Kenneth\Downloads\music\music\Las\Outlaw EP\03 Drumspeak.m4a*C:\Users\Kenneth\Downloads\music\music\Las\Backyard _ Tic\02 Tic.mp3*C:\Users\Kenneth\Downloads\music\music\Las\Backyard _ Tic\01 Backyard.mp3*C:\Users\Kenneth\Downloads\music\music\Las\Las x Mikael - Single\01 Dem Break.m4a*C:\Users\Kenneth\Music\Collection\LAS\Your Eyes EP\03 Aspect.mp3*C:\Users\Kenneth\Music\Collection\LAS\Your Eyes EP\04 Lesson.mp3*F:\Programs\Project Files\FL\2019 old\bisto\bonnuci\blackburn_2\submixes\blackburn_2_Master.wav",fullscreen=False,randomize=False,hide=False)
    # ffplay('*'.join(i for i in gather(r'c:\users\kenneth\downloads\music',ext='mp3',names=False)))
    # ffplay('*'.join(i for i in gather(r'c:\users\kenneth\music\collection\alix perez',names=False)),fullscreen=False,hide=False,randomize=False)
    # ffplay(r'C:\Users\Kenneth\Downloads\byextension\wav*c:\users\kenneth\music\collection\alix perez',randomize=False)
    # ffplay(
    # '*'.join((
        # r"C:\Users\Kenneth\Downloads\byextension\mp3\Ryan Patrick Maguire - $†@®.mp3",
        # r"C:\Users\Kenneth\Downloads\byextension\mp3\Ryan Patrick Maguire - free_language.mp3",
        # r"C:\Users\Kenneth\Downloads\byextension\mp3\Ryan Patrick Maguire - moDernisT.mp3"
    # )))
    # ffplay(r'C:\Users\Kenneth\Downloads\byextension\mp3\SAR01.mp3*C:\Users\Kenneth\Downloads\byextension\mp3\SAR262.mp3')
    # compare(succ,pred)
    # tst = {
        # 'a':1,
        # 'b':{},
        # 'c':{},
        # 'd':2,
        # 'e':[],
        # 'f':[],
        # 'g':1,
        # 'h':1,
    # }
    # print(deduplicate(tst))
    # for i in range(10): print(agora(),agora(True))
    # f = r'e:\projects\monties\2020\fileManagement\knownExtensions.pkl'
    # [print(i,f.index(i),i==j) for i,j in zip(set(f),shuffle(set(f))) if i==j]# else print(i,j)]# in set(f) for j in shuffle(set(f))] 
    # from math import log
    # help(log)
    # print((val:=factorial(len(f))),log(val,10),pyramid(log(val,10)),sep='\n',end='\n\n')
    # n = 1
    # while (k:=pyramid(n))>0:
        # k /= n
        # n += 1
        # print(n-1,k)
        
    # print(n,pyramid(n))
    # help(straw(__file__,False)[0])
    # print(straw(__file__,text=False,lines=False))
    # for i in straw(__file__,False): 
        # print(i.decode('utf-8'))
    # priter(f,1)
    # priter(shuffle(f))
    # print(empty(f))
    # print(os.curdir)
    # print(shutil.get_unpack_formats())
    # print(unpack(r"C:\Users\Kenneth\Downloads\music\music.rar"))
    # extractRar(r"C:\Users\Kenneth\Downloads\music\music.rar")
    # print(nameSpacer(__file__+'loll'))
    # unpack(r"C:\Users\Kenneth\Downloads\music\music.rar")
    pass
