import json
import pyjq
from graphviz import Graph

jf = open('links.json', "r")
src = json.load(jf)
jf.close()
G = Graph(filename='links.dot')

for source in src:
    jf = open('/Users/ekimtco2/PycharmProjects/security-scripts/security_scripts/information/report_files/L0B/' +
              source + '.json', "r")
    print('finding nodes in ' + source)
    json_file = json.load(jf)
    jf.close()
    findings = pyjq.all(src[source]['query'], json_file)


    for finding in findings:

        # init graphviz stuff
        last_edge = None

        for node in src[source]['nodes']:
            print('Added node ' + finding[node])
            G.node(finding[node], label=node + '\n' + finding[node])
            if last_edge is not None:
                G.edge(last_edge, finding[node])
                last_edge = finding[node]
            else:
                # start formulating edge tuples on next loop
                last_edge = finding[node]



        print('____________')

# dump to file
G.render()
