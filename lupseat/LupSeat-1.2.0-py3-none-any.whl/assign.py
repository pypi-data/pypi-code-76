import random
import math
from models.student import *
from models.room import *

class Algorithm:
    @staticmethod
    def choose_algorithm(alg):
        alg = alg.lower().replace(' ','')
        if alg == "chunkincrease":
            return ChunkIncrease()
        elif alg == "consecdivide":
            return ConsecDivide()
        elif alg == "randomassign":
            return RandomAssign()
        else:
            raise Exception("Algorithm {} Unknown".format(alg))

    @staticmethod
    def choose_seat(seat_inds):
        '''Randomly choose seat from list and remove it.'''
        ele = random.choice(seat_inds)
        seat_inds.remove(ele)
        return ele

    @staticmethod
    def assign_seats_rand(rm, stdts):
        '''Assign seats based on specificity, from most specific to least. 
        Room class controls which seats are available for students.
        Room class is mutated to include SID of student sitting there.
        Not all students are guaranteed a desired seat, esp if there aren't enough specified seats available.

        Args:
            rm (Room): Room instance
            stdts (Dict{Student}): Dictionary of students, specified by SID
        '''
        # In decreasing order of specificity
        params = [{'left_hand':True, 'special_needs':True},
                  {'left_hand':False, 'special_needs':True},
                  {'left_hand':True, 'special_needs':False},
                  {'left_hand':False, 'special_needs':False}]

        carry_over_stdts = []
        for param in params:
            # Get list of students and available seats
            spec_stdts = Student.get_spec_students(stdts, left_hand=param['left_hand'], special_needs=param['special_needs'])
            seat_inds = rm.get_spec_seats(left_hand=param['left_hand'], special_needs=param['special_needs'])

            # Add list of students with previously unseated students
            spec_and_carry_stdts = carry_over_stdts + spec_stdts
            carry_over_stdts = []

            # Add student to room
            for index, stdt_id in enumerate(spec_and_carry_stdts):
                if len(seat_inds) == 0:
                    carry_over_stdts = spec_and_carry_stdts[index:]
                    break

                rm.add_student(Algorithm.choose_seat(seat_inds), stdt_id)

        # Not enough seats for all students
        if len(carry_over_stdts) > 0:
            raise Exception("Not enough seats in room for students")

class RandomAssign(Algorithm):
    @staticmethod
    def assign_empty_seats(rm, stdts):
        pass


class ChunkIncrease(Algorithm):
    @staticmethod
    def distribute_empty_2pass(seat_group, max_chunk_size, chk_size_l):
        '''Second pass to distribute empty seat inds within seat group.
        Args:
            seat_group (SeatGroup): Single SeatGroup to distribute students
            max_chunk_size (int): Max size of students sitting together
            empty_inds (List[Tuple(int, int)]): List of empty seat indices from initial pass

        Returns:
            (List[Tuple(int, int)]): List of empty seat indices
        '''
        size = seat_group.size()
        if size <= max_chunk_size:
            return []

        # Check whether seats within chunks can be redistributed
        chk_size_l.sort()
        while chk_size_l[0] <= chk_size_l[-1] - 2:
            chk_size_l[0] += 1
            chk_size_l[-1] -= 1
            chk_size_l.sort()

        # Edge seats should be prioritized
        swapIndex = 1
        while chk_size_l[0] == 0:
            if swapIndex >= len(chk_size_l):
                break
            chk_size_l[0], chk_size_l[swapIndex] = chk_size_l[swapIndex], chk_size_l[0]
            swapIndex += 1

        # Get new empty inds
        empty_inds = []
        seat = 0
        for chk_size in chk_size_l:
            seat += chk_size
            cur_seat = (seat_group.chunk_begin[0], seat_group.chunk_begin[1] + seat)
            empty_inds.append(cur_seat)
            seat += 1

        # Remove last seat from empty inds
        return empty_inds[:-1]

    @staticmethod
    def distribute_empty(seat_group, max_chunk_size):
        '''Gets list of indices where empty seats should go. Prioritizes edge seats.
        Args:
            seat_group (SeatGroup): Single SeatGroup to distribute students
            max_chunk_size (int): Max size of students sitting together

        Returns:
            (List[Tuple(int, int)]): List of empty seat indices (if 2 pass not needed)
            (List[int]): List of chunk sizes separated by empty seat (used for 2 pass)
        '''
        size = seat_group.size()
        if max_chunk_size >= size:
            return [], [size]

        empty_inds = []
        chunk_list = []

        # Continue assignment linearly
        current_chunk_size = 0
        for seat in range(size):
            cur_seat = (seat_group.chunk_begin[0], seat_group.chunk_begin[1] + seat)

            # Special case: If we are at second to last seat
            # (Due to last seat already being taken)
            # If adding (this seat + last seat) to current chunk exceeds max size
            edges_assgn = size > 2
            second_last = seat == (size - 2) and edges_assgn and current_chunk_size + 2 > max_chunk_size

            if current_chunk_size == max_chunk_size or second_last:
                # Break off chunk (got too big) or second to last must be empty
                empty_inds.append(cur_seat)
                chunk_list.append(current_chunk_size)
                current_chunk_size = 0
            else:
                current_chunk_size += 1

        # Add last seat
        if current_chunk_size != 0:
            chunk_list.append(current_chunk_size)
            current_chunk_size = 0

        return empty_inds, chunk_list

    @staticmethod
    def get_possible_seats(seat_group, max_chunk_size):
        '''Determines the number of seats possible in this chunk given with some maximum chunk size.
        Args:
            seat_group (SeatGroup): SeatGroup object to specify current chunk
            max_chunk_size (int): Max size of students sitting together

        Returns:
            (int): Number of students who can be seated within this chunk
        '''
        size = seat_group.size()
        if max_chunk_size >= size:
            return size

        taken = 0
        while True:
            size -= max_chunk_size
            taken += max_chunk_size

            if size <= 0:
                # Fix overflow
                taken -= (-size)

                return taken

            # Leave space to separate chunk
            size -= 1

    @staticmethod
    def get_max_chunk_size(chunks, num_students):
        '''Find the minumum "max chunk size" needed to fit everybody.
        Args:
            chunks (List[SeatGroups]): list of prelimiinary chunks before applying empty seats
            num_students (int): Number of students who need seats

        Returns:
            int: Minimum "max size of chunk" necessary to create chunks to fit everybody in the room
        '''
        for chunk_size in range(1, num_students+1):
            num_seats_filled = 0
            for chunk in chunks:
                num_seats_filled += ChunkIncrease.get_possible_seats(chunk, chunk_size)

                # All students filled
                if num_seats_filled >= num_students:
                    return chunk_size

        # Students don't fit in seats
        raise Exception("Students don't fit in seat")

    @staticmethod
    def assign_empty_seats(rm, stdts):
        '''Disables empty seats by distributing it evenly amongst room.
        Args:
            rm (Room): Room instance
            stdts (dict{Student}): dictionary of students, identified by SID
        '''
        chunks = rm.split_to_chunks()
        max_chunk_size = ChunkIncrease.get_max_chunk_size(chunks, len(stdts))

        for chunk in chunks:
            _, chk_size_l = ChunkIncrease.distribute_empty(chunk, max_chunk_size)
            empty_inds = ChunkIncrease.distribute_empty_2pass(chunk, max_chunk_size, chk_size_l)

            for empty_ind in empty_inds:
                rm.set_enable(empty_ind, False)

class ConsecDivide(Algorithm):
    @staticmethod
    def total_chunk_size(chunks):
        '''Gets total num of seats in all SeatGroups
        Args:
            chunks (List[SeatGroup]): List of SeatGroups in room

        Returns:
            int: Number of available seats
        '''
        total = 0
        for chunk in chunks:
            total += chunk.size()
        return total

    @staticmethod
    def get_subchunk_empty(new_subchunks, subchunk_size, remainder, offset):
        '''Gets empty seat indiices based on params.
        Args:
            new_subchunks (int): Number of subchunks to split seats into.
            subchunk_size (int): Number of seats per subchunk.
            remainder (int): Left over seats to be distributed into subchunks.
            offset (int): Number of col offset where the seat begins.

        Returns:
            (List[int]): List of empty seat indices by column.
        '''
        counter = 0
        empty_list = []
        for subchunk in range(new_subchunks):
            # Compute size of current chunk
            cur_subchunk_size = subchunk_size
            if remainder > 0:
                cur_subchunk_size += 1
                remainder -= 1

            empty_list.append(cur_subchunk_size + counter + offset)
            counter += cur_subchunk_size + 1

        # Remove last element
        return empty_list[:-1]

    @staticmethod
    def assign_empty_seats(rm, stdts):
        '''Disables empty seats by continuous splitting
        Args:
            rm (Room): Room instance
            stdts (dict{Student}): dictionary of students, identified by SID
        '''
        # Split until all empty seats accounted for
        chunks = rm.split_to_chunks()
        num_stdts = len(stdts)
        num_seats = ConsecDivide.total_chunk_size(chunks)
        num_empty = num_seats - num_stdts

        if num_stdts == num_seats:
            return
        elif num_stdts > num_seats:
            raise Exception("Not enough seats for all students")

        chunks.sort(key=SeatGroups.max_chunk_size, reverse=True)

        for i in range(num_empty):
            if chunks[0].max_chunk_size() <= 1:
                break

            # Compute how many times this chunk needs to be split
            num_subchunks = len(chunks[0].empty) + 1
            new_subchunks = num_subchunks + 1

            # Compute size of new subchunks
            occupied_seats = chunks[0].size() - (len(chunks[0].empty) + 1)
            subchunk_size = math.floor(occupied_seats / new_subchunks)
            remainder = occupied_seats % new_subchunks

            # Beginning of col
            offset = chunks[0].chunk_begin[1]

            # Get empty seat indices to split into subchunks
            chunks[0].empty = ConsecDivide.get_subchunk_empty(new_subchunks, subchunk_size, remainder, offset)

            chunks.sort(key=SeatGroups.max_chunk_size, reverse=True)

        # Finalize empty seats
        ConsecDivide.apply_empty_seats(rm, chunks)

    @staticmethod
    def apply_empty_seats(rm, chunks):
        '''Finished splitting chunk, disable empty seats
        Args:
            rm (Room): Room object.
            chunks (List[SeatGroup]): List of SeatGroups in room
        '''
        for chunk in chunks:
            row = chunk.chunk_begin[0]
            for col in chunk.empty:
                rm.set_enable((row, col), False)

