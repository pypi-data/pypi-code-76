from udpipe_parser import *
P = UDPipeParser()

text =  'какие факультеты каких институтов желательно закончить ( жителям Санкт-Петербурга ) ?'

q = P.run(text,logging=True)

for q_i in q:
    print(q_i)
    print()