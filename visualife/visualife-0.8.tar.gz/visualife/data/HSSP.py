import re


class HSSP:
    """Reads HSSP files and stores the data

    """
    def __init__(self, file_name_or_data):
        self.__ids = []
        self.__sequences = {}
        self.__headers = {}
        self.__n_aligned = 0
        self.__seq_length = 0

        self.__read_hssp(file_name_or_data)

    @property
    def ids(self):
        return self.__ids

    @property
    def headers(self):
        return self.__headers

    @property
    def sequences(self):
        return self.__sequences

    @property
    def seq_aligned(self):
        return self.__n_aligned

    @property
    def seq_length(self):
        return self.__seq_length

    def __read_hssp(self, file_name_or_data):
        if len(file_name_or_data) < 80:
            f = open(file_name_or_data)
            text = f.read()
            f.close()
        else:
            text = file_name_or_data
        lines = text.split("\n")
        for line in lines:
            if line.startswith("SEQLENGTH"):
                self.__seq_length = int(line.split()[1].strip())
            elif line.startswith("NALIGN"):
                self.__n_aligned = int(line.split()[1].strip())

        protein_starts = re.search(r'^## PROTEINS', text, flags=re.MULTILINE).start()
        alignments = re.finditer(r'^## ALIGNMENTS', text, flags=re.MULTILINE)
        alignment_starts = []
        for a in alignments:
            alignment_starts.append(a.start())
        stop = re.search(r'^## SEQUENCE', text, flags=re.MULTILINE).start()

        proteins = text[protein_starts:alignment_starts[0]]
        lines = proteins.split('\n')
        lines = lines[2:-1]
        for line in lines:
            self.__ids.append(line.split()[2])

        seq_tmp = ["" for _ in range(self.seq_length)]
        for x in range(len(alignment_starts) - 1):
            alignments = text[alignment_starts[x]:alignment_starts[x + 1]]
            lines = alignments.split('\n')
            lines = lines[2:-1]
            i = 0
            for line in lines:
                seq = line[51:121].replace(' ', '-')
                seq_tmp[i] += seq
                i += 1

        last = text[alignment_starts[-1]:stop]
        lines = last.split('\n')
        lines = lines[2:-1]
        i = 0
        for line in lines:
            seq = line[51:121].replace(' ', '-')
            seq_tmp[i] += seq
            i += 1
        for i in range(self.seq_length):
            seq_tmp[i] = seq_tmp[i][:self.seq_aligned]
        for i in range(self.seq_aligned):
            seq = ""
            for j in range(self.seq_length):
                seq += seq_tmp[j][i]
            self.__sequences[self.ids[i]] = seq



