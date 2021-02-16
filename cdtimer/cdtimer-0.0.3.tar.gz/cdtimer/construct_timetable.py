'''
Daniel Vogler
read in time timetable file
'''

def read_timetable_file(timetable_file):

    import csv
    import operator

    timetable = [[] for _ in range(5)]

    with open(timetable_file, newline='') as csvfile:
        timetable_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(timetable_reader)
        for row in timetable_reader:
            ### read in exercises
            timetable[0].append(row[0])
            ### read in weights and reps (optional)
            timetable[1].append(row[1])
            ### read in total sets
            timetable[2].append(int(float(row[2])))
            ### read in set times
            timetable[3].append(row[3])
            ### read in order
            timetable[4].append(row[4])

    ### total number of sets
    timetable_sets = sum( timetable[2] )
    print("Total sets: ", timetable_sets, "\n")

    ### construct list of all timetable sets
    timetable_list = [[] for x in range(7)]

    ### different exercises
    for i in range(len(timetable[0])):
        ### exercise sets
        for j in range(timetable[2][i]):

            ### timetable set decomposition
            timetable_rw = timetable[1][i].split('/')
            timetable_rw_split = timetable_rw[j].split('-')
            if len(timetable_rw_split) > 1:    
                timetable_rw_split = str(timetable_rw_split[0] + "x" + timetable_rw_split[1]+"kg")
            else:
                timetable_rw_split = timetable_rw_split[0]

            ### timetable order decomposition
            timetable_order = timetable[4][i].split('/')

            ### list of all individual sets
            ### exercise
            timetable_list[0].append(timetable[0][i])
            ### reps (and weight)
            timetable_list[1].append(timetable_rw_split)
            ### set no out of total sets
            timetable_list[2].append(str(str(j+1)+"/"+str(timetable[2][i])))
            ### time per set
            timetable_list[3].append(int(float(timetable[3][i])))
            ### order of set
            timetable_list[4].append(int(float(timetable_order[j])))
            ### total time
            timetable_list[5].append(sum(timetable_list[3]))
            ### set index
            timetable_list[6].append(0)

    ### transpose list
    timetable_list = list(map(list, zip(*timetable_list)))
    ### sort by set order
    timetable_list = sorted(timetable_list, key=operator.itemgetter(4))

    ### print out timetable
    set_time = 0
    timetable_set_time = []
    for i in range(len(timetable_list)):
        timetable_list[i][5] = set_time
        timetable_list[i][6] = i
        timetable_set_time.append(set_time)

        set_time += timetable_list[i][3]
        
        print("Set", "{:02d}".format(timetable_list[i][6]+1),"-", timetable_list[i][0], timetable_list[i][1], "#", timetable_list[i][2], "for", timetable_list[i][3], "s at", timetable_list[i][5], "s")

    ### final time required for whole timetable
    set_time = timetable_list[-1][5] + timetable_list[-1][3]

    return timetable_list, timetable_set_time, set_time