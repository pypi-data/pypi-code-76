from models.seat import *

def chr_to_int(char):
    '''Convert row char to row number
    Args:
        row (char): ('a', 'b')

    Returns:
        int:  row number (1 to max_row)
    '''
    return ord(char.lower()) - ord('a') + 1

def int_to_chr(num):
    '''Convert row number to row char
    Args:
        row (int): 0 to max_row-1

    Returns:
        int: row char ('a', 'b')
    '''
    return chr(ord('a') + num)

def seat_inds(seat):
    '''Get seat indices'''
    if not seat[0].isalpha():
        raise Exception("Seat {} not formatted correctly".format(seat))
    if not seat[1:].isnumeric():
        raise Exception("Seat {} not formatted correctly".format(seat))

    cur_row = chr_to_int(seat[0])
    cur_col = int(seat[1:])
    return (cur_row, cur_col)

def process_str(raw_str):
    '''Removes all whitespace and makes lowercase. Removes any trailing colons'''
    if raw_str == '':
        return ''
    if raw_str[-1] == ':':
        raw_str = raw_str[:-1]
    return "".join(raw_str.lower().split())

def get_col_inds(col_range):
    """Gets column indices in iterator form"""
    if '-' in col_range:
        beg_seat = col_range.split('-')[0]
        end_seat = col_range.split('-')[1]
        if beg_seat[0] != end_seat[0]:
            raise Exception("Non matching row char {} and {}".format(beg_seat[0], end_seat[0]))

        beg = int(beg_seat[1:])
        end = int(end_seat[1:])
        return range(beg, end+1)
    elif str.isdigit(col_range[1:]):
        return range(int(col_range[1:]), int(col_range[1:])+1)
    else:
        raise Exception("Unknown col range format: {}".format(cur_col_range))

class Room:
    """Contains grid representation of room containing seat instances"""
    def __init__(self):
        self.max_row = 1
        self.max_col = 1
        self.seats = []
        # Specifies where the row is discontinuous (can be considered new chunk)
        self.row_breaks = []

    def __str__(self):
        output = ''
        for rows in self.seats:
            for seat in rows:
                if seat == None:
                    output += "{0: <3}".format('n')
                else:
                    output += "{0: <3}".format(seat.sid)
                output += ' '
            output += '\n'
        return output

    def __repr__(self):
        return str(self)

    @classmethod
    def create_room(cls, filepath):
        """Instantiates room class with correct size and seats.
        Args:
            filepath (str): path to yaml file describing room layout.

        Returns:
            Room: Room instance with correct size, seats & seat qualities specified
        """
        with open(filepath, 'r') as f:
            f_raw = f.read()

        rm = cls()
        rm._update_size(f_raw)
        rm._add_seats(f_raw)
        rm._add_seat_specifiers(f_raw)
        return rm

    def _update_size(self, f_raw):
        """Gets dimensions of room (during instantiation)"""
        seat_flag = False
        for line in f_raw.splitlines():
            line = process_str(line)
            if line == "seats" or line == "seat":
                seat_flag = True
            elif line == "specifiers" or line == "specifier":
                seat_flag = False
            elif seat_flag:
                # Skip if empty line
                if line == "":
                    continue

                # Otherwise check if seat range is new max
                for seat_range in line.split(','):
                    # Skip if empty range
                    if seat_range == '':
                        continue

                    cur_row, cur_col = seat_inds(seat_range.split('-')[-1])

                    if cur_row > self.max_row:
                        self.max_row = cur_row
                    if cur_col > self.max_col:
                        self.max_col = cur_col

    def _add_seats(self, f_raw):
        """Adds seats to room (during instantiation)"""
        # Row major
        for row in range(self.max_row):
            self.row_breaks.append([])
            self.seats.append([None] * self.max_col)

        seat_flag = False
        infer_row_num = 0
        for line in f_raw.splitlines():
            line = process_str(line)
            if line == "seats" or line == "seat":
                seat_flag = True
            elif line == "specifiers" or line == "specifier":
                seat_flag = False
            elif seat_flag:
                # Skip if empty line
                if line == "":
                    continue

                # Update inference
                infer_row_num += 1

                # Add seats per each range
                for row_range in line.split(','):
                    # Skip if empty range
                    if row_range == '':
                        # Infer row from previous rows
                        self.row_breaks[infer_row_num-1].append(0)
                        continue

                    # Add seat
                    cur_row = chr_to_int(row_range[0])
                    cur_col = 1
                    for cur_col in get_col_inds(row_range):
                        self.seats[cur_row-1][cur_col-1] = Seat()

                    # Store row break
                    self.row_breaks[cur_row-1].append(cur_col-1)

    def _add_seat_specifiers(self, f_raw):
        """Adds seat features to each seat (during instantiation)"""
        spec_flag = False
        for line in f_raw.splitlines():
            line = process_str(line)
            if line == "specifiers" or line == "specifier":
                spec_flag = True
            elif line == "seats" or line == "seat":
                spec_flag = False
            elif spec_flag:
                # Skip if empty line
                if line == "":
                    continue

                # Check if line formatted correctly
                if len(line.split(':')) != 2:
                    raise Exception("Line not formatted correctly: {}".format(line))

                # Get seat indices
                cur_row, cur_col = seat_inds(line.split(':')[0])
                if self.seats[cur_row-1][cur_col-1] == None:
                    raise Exception("Adding quality to seat that doesn't exist {}".format(line))

                # Apply flag to seat
                flags = line.split(':')[1]
                for flag in flags:
                    if flag == 'b':
                        self.seats[cur_row-1][cur_col-1].broken = True
                        # If broken, need to split seats
                    if flag == 'l':
                        self.seats[cur_row-1][cur_col-1].left_handed = True
                    if flag == 's':
                        self.seats[cur_row-1][cur_col-1].special_needs = True

    def add_student(self, indices, sid):
        self.seats[indices[0]][indices[1]].sid = sid

    def set_enable(self, indices, val):
        self.seats[indices[0]][indices[1]].enable = val

    def get_spec_seats(self, left_hand=False, special_needs=False):
        """Gets specified seats or seats with more specificity
        e.g. If getting left_handed seats, will look for both special_needs and non_sp_needs seats

        Args:
            left_hand (bool): flag for whether to search for left or right handed students
            special_needs (bool): flag for whether to search for special needs students

        Returns:
            List of tuples: List of indices corresponding to seat locations
        """
        match_seats = []

        for row in range(self.max_row):
            for col in range(self.max_col):
                # Ignore if seat not there
                if self.seats[row][col] == None:
                    continue

                # Ignore broken seats
                if self.seats[row][col].broken:
                    continue

                # Ignore disabled seats
                if not self.seats[row][col].enable:
                    continue

                # Ignore if seat is taken
                if self.seats[row][col].sid != -1:
                    continue

                # Add seats based on condition
                if left_hand and special_needs:
                    if self.seats[row][col].left_handed and self.seats[row][col].special_needs:
                        match_seats.append((row, col))
                elif left_hand:
                    if self.seats[row][col].left_handed:
                        match_seats.append((row, col))
                elif special_needs:
                    if self.seats[row][col].special_needs:
                        match_seats.append((row, col))
                else:
                    match_seats.append((row, col))

        # Ensure that seats are sorted by row
        match_seats.sort()

        return match_seats

    def split_to_chunks(self):
        '''Splits seats into SeatGroup chunks if they are continuous and not broken.
        Returns:
            List[SeatGroups]: List of SeatGroups representing preliminary chunk.
        '''
        # Populate chunks assuming infinite max_chunk_size
        chunks = []

        is_chunk = False
        chunk_begin = None

        for row in range(self.max_row):
            for col in range(self.max_col):
                # Start new chunk
                if not is_chunk and self.seats[row][col] != None and not self.seats[row][col].broken:
                    is_chunk = True
                    chunk_begin = (row, col)
                # End current chunk
                elif is_chunk and (self.seats[row][col] == None or self.seats[row][col].broken):
                    is_chunk = False
                    chunk_end = (row, col-1)
                    chunks.append(SeatGroups(chunk_begin, chunk_end))

                # End current chunk due to row break
                if is_chunk and col in self.row_breaks[row]:
                    is_chunk = False
                    chunk_end = (row, col)
                    chunks.append(SeatGroups(chunk_begin, chunk_end))

            if is_chunk:
                is_chunk = False
                chunk_end = (row, col-1)
                chunks.append(SeatGroups(chunk_begin, chunk_end))

        return chunks

