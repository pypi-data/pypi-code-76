import re


def sorted_nicely( l ): 
    """ Sort the given iterable in the way that humans expect.""" 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)
    
def l_test( l ): 
    """ Sort the given iterable in the way that humans expect."""
    print(l)
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    print(convert)
    for i, x in enumerate(l) : 
        try:
            print(alphanum_key(l[i]))
        except:
            print(alphanum_key(l[x]))
    return sorted(l, key = alphanum_key)
	
if __name__ == '__main__':
    list = ['max', 'is', 'a', 'good', 'guy']
    print(sorted_nicely(list))
    print(l_test(list))
    #list = [('max', 'is'), ('a', ''), ('good', 'guy')] type error
    tup = ('max', 'is', 'a', '', 'good', 'guy')
    print(sorted_nicely(tup))
    print(l_test(tup))
    dict = {'what' : 'a good guy', 'max': 'is'}
    print(sorted_nicely(dict))
    dict2 = {}
    for x in l_test(dict): print('dict['+x+']: '+dict[x])
    [ print('dict['+x+']: '+dict[x]) for x in l_test(dict) ]
    [ print(x+' '+dict[x]) for x in l_test(dict) ]
    for x in l_test(dict): dict2[x] = dict[x]
    print(dict2)