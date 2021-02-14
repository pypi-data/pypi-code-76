import itertools
import re
import csv
import sys

def argmax(x):
    return max(enumerate(x), key=lambda x:x[1])[0]

if __name__ == "__main__":
    FILE = "/tmp/field.txt"
    with open(FILE) as f_in:
        lines = [l.replace("\n","") for l in f_in]
        line_cnt = len(lines)
        proc_lines = ["".join(["|"*len(x) if len(x.strip()) == 0 else x for x in re.split("([ ]{3,})",l)]) for l in lines]
        proc_lines = [line.ljust(max([len(l) for l in proc_lines]),"|") for line in proc_lines]

        #find the best places to divide into fields
        slice_scores = [len([c for c in x if c != "|"]) for x in zip(*proc_lines)]
        slice_scores = slice_scores

        field_cuts = [0]
        for i,x in enumerate(slice_scores):
            if i==(len(slice_scores)-1): continue
            delta = slice_scores[i+1] - slice_scores[i]
            if ((delta+2) / (x+2)) > 2:
                field_cuts.append(i+1)
        field_cuts.append(len(slice_scores))
        # print(field_cuts)

        #now realign lines to better match these fields
        writer = csv.writer(sys.stdout)
        for l in lines:
            pieces = [x for x in re.split("([ ]{3,})",l) if x] #drop empty strings this picks up at the start sometimes
            line_cuts = [0]
            cnt = 0
            for p in pieces:
                cnt += len(p)
                if len(p.strip()) == 0:
                    line_cuts.append(cnt)
            line_cuts.append(len(l))
            fields = ['']*len(field_cuts)
            for i,c in enumerate(line_cuts[:-1]):
                #find the nearest field cut
                best_match_idx = argmax([-abs(c-x) for x in field_cuts[:-1]])
                # print(c,best_match_idx)
                fields[best_match_idx] += l[line_cuts[i]:line_cuts[i+1]]
            # print(fields)
            fields = [f.strip() for f in fields]
            writer.writerow(fields)
