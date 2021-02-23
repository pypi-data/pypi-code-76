from pympler import muppy, summary


class Profiler(object):
    def __init__(self):
        self.all_objects = {}

    def printIncreased(self):
        all_objects = {}
        all_objects_instances = muppy.get_objects()
        all_objects_arr = summary.summarize(all_objects_instances)
        for name, number, size in all_objects_arr:
            all_objects[name] = (number, size)
        if (self.all_objects):
            increased_objs = []
            for name, values in all_objects.items():
                prev_values = self.all_objects.get(name)
                try:
                    if (values[1] > prev_values[1]):
                        increased_objs.append((name, values[0], values[1]))
                except:
                    print(name)
            self.all_objects = all_objects
            summary.print_(increased_objs)
            return increased_objs
        else:
            self.all_objects = all_objects
            summary.print_([])
            return []


if __name__ == '__main__':
    profiler = Profiler()


    # import gc
    class A(object):
        def __init__(self):
            self.bb = bytes(10)

        pass


    # ar = A()
    # gc.collect()
    # profiler.printIncreased()
    # print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
    # a = []
    #
    # g = 'd' + 's'
    # aee = A()
    # # aee = None
    # gc.collect()
    # profiler.printIncreased()
    #
    # print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
    #
    # aee.bb = A()
    # gc.collect()
    # profiler.printIncreased()
    # print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
    # df = {'m': bytes(10000000000)}
    # summary.print_(profiler.printIncreased())
    from pympler import classtracker

    tr = classtracker.ClassTracker()
    tr.track_class(str)
    a = A()
    tr.create_snapshot()
    print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
    profiler.printIncreased()
    a = A()
    b = {'b': bytes(1000000)}
    tr.create_snapshot()
    print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
    profiler.printIncreased()
    tr.stats.print_summary()
