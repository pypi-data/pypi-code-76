import csv
import json

class Student:
    @staticmethod
    def parse_stdt(filepath):
        """Parses student csv
        Args:
            filepath (str): path to student csv

        Returns:
            dict{Student}: dictionary of students, identified by SID
        """
        stdts = {}
        with open(filepath) as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                if len(row) < 5:
                    print("Error parsing student: {}. Skipping.".format(row))
                    continue
                try:
                    new_stdt = Student(row)
                except Exception as e:
                    print(e)
                    print("Error parsing student: {}. Skipping.".format(row))
                    continue
                stdts[new_stdt.sid] = new_stdt
        return stdts

    @staticmethod
    def parse_stdt_partners(filepath, stdts):
        """Parses student partners csv
        Args:
            filepath (str): path to student partners csv
            stdts (dict{Student}): dictionary of students, identified by SID

        Returns:
            dict{Student}: dictionary of students, identified by SID (modified with partners list)
        """
        # Do nothing if no filepath specified
        if filepath == None:
            return stdts

        with open(filepath) as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                for i, stdt_id in enumerate(row):
                    # Add all other sids (except for yourself)
                    stdts[stdt_id].past_partners = row[:i] + row[i+1:]
        return stdts

    def __init__(self, stdt):
        """ Initialize student by parsing line in csv. Does type checking"""
        self.first = stdt[0]
        self.last = stdt[1]

        if not str.isdigit(stdt[2]):
            raise Exception("SID must be an integer: {}".format(stdt[2]))
        elif int(stdt[2]) < 0:
            raise Exception("SID must be a postiive integer: {}".format(stdt[2]))
        else:
            self.sid = int(stdt[2])

        # Assume right hand
        self.left_hand = True if stdt[3] == "left" or "left" in stdt[3] else False

        # Assume no special needs
        self.special_needs = True if stdt[4] == "special" or "special" in stdt[4] else False

        self.past_partners = []

    def __str__(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return str(self)

    @staticmethod
    def get_spec_students(stdts, left_hand=False, special_needs=False):
        """Gets the specified students
        Args:
            stdts (dict{Student}): dictionary of students, identified by SID
            left_hand (bool): flag for whether to search for left or right handed students
            special_needs (bool): flag for whether to search for special needs students

        Returns:
            list[int]: list of specified student ids
        """
        spec_stdts = []
        for stdt in stdts.values():
            if stdt.left_hand == left_hand and stdt.special_needs == special_needs:
                spec_stdts.append(stdt.sid)

        return spec_stdts

