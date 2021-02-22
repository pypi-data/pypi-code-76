from typing import List, Union, Tuple
import os
import tempfile
import subprocess
from math import isclose
import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation

import logging
logging.basicConfig(format='%(asctime)s %(message)s')

Lines = str


class CytosimReader:
    """
    Read data generated with cytosim. Initialize with the path 
    to the folder containing the output data. Reports can then
    be generated and read with the method ``read_report``.
    """

    def __init__(self, folder: str, report_executable: str='report'):
        """
        Create CytosimReader for an output folder containing data generated
        by cytosim simulations.

        :param folder: Path to folder containing cytosim output (cmo) files.
        :param report_executable: If you renamed your cytosim ``report`` executable,
                                  pass the name with this parameter.
        """
        self.folder = os.path.abspath(folder)
        self._folder_reports = os.path.join(folder, 'reports')
        if not os.path.exists(self._folder_reports):
            os.mkdir(self._folder_reports)
        if not os.path.isdir(self._folder_reports):
            msg = ('CytosimReader wants to put reports into '
                   f'folder "{self._folder_reports}".'
                   ' But there is a file with that name! Please move '
                   'that file if you want to use CytosimReader.')
            raise RuntimeError(msg)
        self.report_exe = report_executable

    def read_report(self, report_identifier: str,
                    aggregate=False, clear=False) -> Union[List['ReportBlock'], pd.DataFrame]:
        """
        Read data from one report. If the report does not exist yet, it will be generated
        in the subfolder ``reports``. The filename will be ``<report_identifier>.txt``,
        where ``:`` delimiter used by cytosim will be replaced by underscores ``_``.
        Data will be either a list of ReportBlock objects (one per recorded frame), or, 
        if aggregate=True, one pandas.DataFrame containing data of all frames.
        To access the actual data of a RecordBlock, use the member RecordBlock.data .

        :param report_identifier: One of the valid identifiers that can be passed as an argument
                                  to cytosim's ``report`` executable; for example ``fiber:points``,
                                  which will create a report file ``reports/fiber_points.txt`` 
                                  and read its content into a pandas.DataFrame .
        :param aggregate: If True, will return data from the report as one big aggregated
                          DataFrame. Otherwise will return a list of ReportBlock objects, one
                          for each recorded frame.
        :param clear: Remove an existing report and re-generate it.

        :return: Either a list of ReportBlock objects (one per recorded frame), or, if aggregate=True,
                 one pandas.DataFrame containing data of all frames.
        """
        split_report_identifier = report_identifier.split(':')
        split_report_identifier = [s.strip() for s in split_report_identifier]
        fname_report = '_'.join(split_report_identifier) + '.txt'
        fname_report = os.path.join(self._folder_reports, fname_report)

        if clear:
            if os.path.exists(fname_report):
                os.remove(fname_report)
        if not os.path.exists(fname_report):
            self._generate_report(report_identifier, fname_report)

        report_blocks = CytosimReader._parse_report_file(fname_report)

        if aggregate:
            return CytosimReader.aggregate(report_blocks)
            
        return report_blocks

    def export_xyz(
            self,
            periodic_box: Union[np.ndarray, List[float]] = None,
            fiber_radius: float=0.1,
            use_fibers: bool = True,
            use_beads: bool = True,
            use_couples: bool = True,
            use_singles: bool = False,
            color_by_id: bool = False,            
    ):
        n_frames = None
        if use_fibers:
            if periodic_box is not None:
                periodic_box = np.array(periodic_box)
            n_frames = self._export_xyz_fibers(color_by_id, periodic_box, fiber_radius)

        if use_beads:
            n = self._export_xyz_beads()
            if n_frames is None:
                n_frames = n
            else:
                if n is not None:
                    assert n_frames == n
        if use_couples:
            n = self._export_xyz_couples()
            if n_frames is None:
                n_frames = n
            else:
                if n is not None:
                    assert n_frames == n
        if use_singles:
            raise NotImplementedError

        if n_frames is None:
            msg = "No data selected for export"
            raise RuntimeError(msg)

    def read_bead_trajectories(self) -> np.ndarray:
        beads = self.read_report('bead', aggregate=True)
        trajs = np.full((beads['frame'].max()+1, beads['identity'].unique().shape[0], 3), np.nan)
        for i, bid in enumerate(beads['identity'].unique()):
            selected = beads[beads['identity'] == bid]
            frames = np.array(selected['frame'], dtype=int)
            positions = np.array(selected[['posX', 'posY', 'posZ']])
            trajs[frames, i] = positions
        return trajs

    def read_run_time(self) -> float:
        """
        Reads total run time in seconds from messages.cmo file.
        At each frame, the time since the previous frame is
        written to the 4th column of the messages file. There
        is also a sum of that time in the 5th column, but it
        has less precision. Since summing up the 4th column
        is not that expensive, that is what we use to
        determine the total time here.
        """
        fname = os.path.join(self.folder, 'messages.cmo')
        with open(fname, 'rt') as fh:
            summed_time = 0
            for line in fh:
                if not line.startswith('F'):
                    continue
                s = line.split()
                t = s[3]
                # strip last character 's' (seconds)
                t = float(t[:-1])
                summed_time += t
        return summed_time
        
    def _export_xyz_fibers(self, color_by_id: bool,
                           periodic_box: np.ndarray,
                           fiber_radius: float) -> Union[int, None]:
        fibers = self.read_report('fiber:point')
        if CytosimReader._is_empty(fibers):
            return
        n_frames = len(fibers)
        folder = os.path.join(self.folder, 'xyz')
        os.makedirs(folder, exist_ok=True)
        fname = os.path.join(folder, 'fibers.xyz')

        with open(fname, 'wt') as fh:
            for i in range(n_frames):
                n_particles = 0
                block_xyz = ""
                if fibers[i] is not None:
                    if periodic_box is None:
                        n, b = CytosimReader._fiber_point_to_xyz(fibers[i].data,
                                                                 color_by_id,
                                                                 fiber_radius)
                    else:
                        n, b = CytosimReader.\
                            _fiber_point_to_xyz_with_periodic_boundaries(
                                fibers[i].data,
                                periodic_box,
                                color_by_id,
                                fiber_radius
                            )
        
                    block_xyz += b
                    n_particles += n
                block_xyz = "{}\n\n".format(n_particles) + block_xyz
                fh.write(block_xyz)
        logging.info('exported fiber positions to {}'.format(fname))
        return n_frames

    def _export_xyz_beads(self) -> Union[int, None]:
        beads = self.read_report('bead')
        if CytosimReader._is_empty(beads):
            return
        n_frames = len(beads)
        folder = os.path.join(self.folder, 'xyz')
        os.makedirs(folder, exist_ok=True)
        fname = os.path.join(folder, 'beads.xyz')
        with open(fname, 'wt') as fh:
            for i in range(n_frames):
                n_particles = 0
                block_xyz = ""
                if beads[i] is not None:
                    n, b = CytosimReader._bead_to_xyz(beads[i].data)
                    block_xyz += b
                    n_particles += n
                block_xyz = "{}\n\n".format(n_particles) + block_xyz
                fh.write(block_xyz)
        logging.info('exported bead positions to {}'.format(fname))
        return n_frames

    def _export_xyz_couples(self) -> Union[int, None]:
        couples = self.read_report('couple:state')
        if CytosimReader._is_empty(couples):
            return
        n_frames = len(couples)
        folder = os.path.join(self.folder, 'xyz')
        os.makedirs(folder, exist_ok=True)
        fname = os.path.join(folder, 'couples_bridging.xyz')
        with open(fname, 'wt') as fh:
            for i in range(n_frames):
                n_particles = 0
                block_xyz = ""
                if couples[i] is not None:
                    n, b = CytosimReader._couple_to_xyz(couples[i].data)
                    block_xyz += b
                    n_particles += n
                block_xyz = "{}\n\n".format(n_particles) + block_xyz
                fh.write(block_xyz)
        logging.info('exported bridging couples\' positions to {}'.format(fname))
        return n_frames

    @staticmethod
    def _is_empty(report_blocks: List[Union['ReportBlock', None]]) -> bool:
        for b in report_blocks:
            if b is not None:
                return False
        return True

    @staticmethod
    def _fiber_point_to_xyz(fiber: pd.DataFrame, color_by_id: bool,
                            periodic_box: np.ndarray,
                            fiber_radius: float) -> Tuple[int, str]:
        id_fiber = np.array(fiber['identity'])
        fil_change = np.zeros_like(id_fiber, dtype=int)
        fil_change[0] = 1
        fil_change[1:] = id_fiber[1:] - id_fiber[:-1]
        w = np.where(fil_change == 1)[0]
        types = np.full_like(fil_change, 'core', dtype='<U4')
        types[w] = 'tail'
        types[w - 2] = 'head'
        mask = np.ones(fiber.shape[0], dtype=bool)
        mask[w-1] = False
        types = types[mask]
        id_fiber = id_fiber[mask]

        pos = np.array(fiber[['posX', 'posY', 'posZ']])
        segments = pos[1:] - pos[:-1]
        segments = segments[mask[:-1]]
        slengths = np.sqrt((segments**2).sum(1))

        centers = (pos[1:] + pos[:-1]) * 0.5
        positions = centers[mask[:-1]]
        orientations = np.zeros((fiber.shape[0] - len(w), 3))
        for i in range(3):
            orientations[:, i] = segments[:, i]/slengths        

        xyz = ""
        count = positions.shape[0]
        if color_by_id:
            line = "fiber_{} {:.2f} {:.2f} {:.2f} {:.6f} {:.6f} {:.6f} {:.6f} {:.2f} {:.2f}\n"
            specifier = id_fiber
        else:
            line = "{} {:.2f} {:.2f} {:.2f} {:.6f} {:.6f} {:.6f} {:.6f} {:.2f} {:.2f}\n"
            specifier = types

        for i in range(count):
            theta, phi = get_angles(orientations[i])
            r = Rotation.from_euler('yz', [theta, phi])
            quat = r.as_quat()

            xyz += line.format(
                specifier[i],
                positions[i, 0],
                positions[i, 1],
                positions[i, 2],
                quat[0],
                quat[1],
                quat[2],
                quat[3],
                fiber_radius,
                slengths,
            )
        return count, xyz

    @staticmethod
    def _fiber_point_to_xyz_with_periodic_boundaries(
            fiber: pd.DataFrame,
            box: np.ndarray,
            color_by_id: bool,
            fiber_radius: float
    ) -> Tuple[int, str]:
        count = 0
        xyz = ""
        for fid in fiber['identity'].unique():
            selected = fiber[fiber['identity'] == fid]
            pos = np.array(selected[['posX', 'posY', 'posZ']])
            shifted_pos = pos + box/2
            shifted_pos = minimum_image_projection(shifted_pos, box)
            shifted_coord_sets = split_filament_coords_at_borders(shifted_pos, box)
            for i in range(len(shifted_coord_sets)):
                c = shifted_coord_sets[i] - box/2                

                centers = (c[1:] + c[:-1]) * 0.5
                segments = c[1:] - c[:-1]
                slengths = np.sqrt((segments**2).sum(1))
                orientations = segments / slengths[:, np.newaxis]

                xyz_c = ""

                if color_by_id:
                    line = "fiber_{} {:.2f} {:.2f} {:.2f} {:.6f} {:.6f} {:.6f} {:.6f} {:.2f} {:.2f}\n"
                    specifier = np.full(centers.shape[0], fid, dtype=int)
                else:
                    line = "{} {:.2f} {:.2f} {:.2f} {:.6f} {:.6f} {:.6f} {:.6f} {:.2f} {:.2f}\n"
                    specifier = np.array(['core']*len(centers))
                    if i == 0:
                        specifier[0] = 'tail'
                    if i == len(shifted_coord_sets)-1:
                        specifier[-1] = 'head'

                for j in range(len(centers)):
                    theta, phi = get_angles(orientations[j])
                    r = Rotation.from_euler('yz', [theta, phi])
                    quat = r.as_quat()

                    xyz_c += line.format(
                        specifier[j],
                        centers[j, 0],
                        centers[j, 1],
                        centers[j, 2],
                        quat[0],
                        quat[1],
                        quat[2],
                        quat[3],
                        fiber_radius,
                        slengths[j]
                    )
                count += centers.shape[0]
                xyz += xyz_c
        return count, xyz
        
    @staticmethod
    def _bead_to_xyz(bead: pd.DataFrame) -> Tuple[int, str]:
        xyz = ""
        line = "bead_type_{} {:.2f} {:.2f} {:.2f}\n"
        for r in bead.iterrows():
            xyz += line.format(
                r[1]['class'],
                r[1]['posX'],
                r[1]['posY'],
                r[1]['posZ']
            )
        return bead.shape[0], xyz

    @staticmethod
    def _couple_to_xyz(couple: pd.DataFrame) -> Tuple[int, str]:
        xyz = ""
        line = "couple_{} {:.2f} {:.2f} {:.2f}\n"
        bridging = couple[(couple['fiber1'] != 0) & (couple['fiber2'] != 0)]
        for r in bridging.iterrows():
            xyz += line.format(
                r[1]['class'],
                r[1]['posX'],
                r[1]['posY'],
                r[1]['posZ']
            )
        return bridging.shape[0], xyz

    @staticmethod
    def _parse_report_file(fname) -> List['ReportBlock']:
        blocks = []
        current_block = []
        with open(fname, 'rt') as fh:
            for line in fh:
                if not line or line.isspace():
                    continue
                if line.startswith('% end'):
                    blocks.append(ReportBlock.parse(current_block))
                    current_block = []
                    continue
                current_block.append(line)
        return blocks

    def _generate_report(self, report_identifier, fname_report):
        command_args = [self.report_exe, report_identifier]
        with open(fname_report, 'wt') as fh:
            subprocess.call(command_args, cwd=self.folder, stdout=fh)

    @staticmethod
    def aggregate(
            report_blocks: List['ReportBlock']
    ) -> Union[pd.DataFrame, None]:
        cols = None
        df = None
        for block_i in report_blocks:
            if block_i is None:
                continue
            cols = block_i.data.columns
            cols = cols.insert(0, 'time').insert(0, 'frame')
            df = pd.DataFrame(columns=cols)
            break
        if cols is None:
            return None
        for block_i in report_blocks:
            if block_i is None:
                continue
            index = block_i.data.index + len(df)
            block_i.data.index = index
            df_i = pd.DataFrame(columns=cols, index=index)
            df_i['time'] = block_i.time
            df_i['frame'] = block_i.frame
            df_i[block_i.data.columns] = block_i.data[block_i.data.columns]
            df = df.append(df_i)
        return df


_reports_with_fiber_blocks = [
    'fiber:points',
    'fiber:point'
]


class ReportBlock:
    """
    Stores data of a single frame of data generated with cytosim's ``report`` executable.
    Access meta data with members ``frame``, ``time``, ``label``, ``info``, or 
    access the actual data (as a pandas.DataFrame) with member ``data``. E.g., if your
    ReportBlock object is ``block``, access data as ``block.data``.
    """

    def __init__(self, frame: int, time: float, label: str,
                 info: List[str], data: pd.DataFrame):
        self.frame = frame
        self.time = time
        self.label = label
        self.info = info
        self.data = data

    @staticmethod
    def read_data(column_names: str, data_block: str) -> pd.DataFrame:
        tf = tempfile.TemporaryFile('w+t')
        tf.write(column_names)
        tf.write(data_block)
        tf.seek(0)

        data = pd.read_csv(tf, delim_whitespace=True, comment='%')
        return data

    @staticmethod
    def parse(block: List[Lines]) -> Union['ReportBlock', None]:
        frame = ReportBlock._parse_frame(block[0])
        time = ReportBlock._parse_time(block[1])
        label = ReportBlock._parse_label(block[2])
        first_data_line = None
        for i in range(3, len(block)):
            if block[i].startswith('%'):
                continue
            first_data_line = i
            break
        if first_data_line is None:
            return None
        if label in _reports_with_fiber_blocks:
            info = block[3: first_data_line-2]
            column_names = block[first_data_line-2][2:]
            data_block = ''.join(block[first_data_line:])
            df = ReportBlock.read_data(column_names, data_block)
            return ReportBlock(frame, time, label, info, df)

        info = block[3: first_data_line - 1]
        column_names = block[first_data_line - 1][2:]
        data_block = ''.join(block[first_data_line:])
        df = ReportBlock.read_data(column_names, data_block)
        return ReportBlock(frame, time, label, info, df)

    @staticmethod
    def _parse_frame(line) -> int:
        s = line.split()
        assert s[1] == 'frame', "This line does not contain the current frame number."
        return int(s[2])

    @staticmethod
    def _parse_time(line) -> float:
        s = line.split()
        assert s[1] == 'time', "This line does not contain the time of the current frame."
        return float(s[2])

    @staticmethod
    def _parse_label(line):
        s = line.split()
        assert s[1] == 'report', "This line does not contain the report label."
        return ' '.join(s[2:])

    def __str__(self):
        return "ReportBlock \"{}\", frame {}".format(self.label, self.frame)

    def __repr__(self):
        return self.__str__()


def get_angles(v: np.ndarray) -> Tuple[float, float]:
    """
    Get angles theta, phi in spherical coordinates of vector v.
    """
    theta = np.arccos(v[2])
    # phi = np.arccos(v[0]/np.sin(theta))
    phi = np.arctan2(v[1], v[0])
    return theta, phi


def minimum_image_projection(
        coords: np.ndarray,
        box: Union[np.ndarray, List[float]]) -> np.ndarray:
    proj = np.empty_like(coords)
    for i in range(len(box)):
        proj[:, i] = coords[:, i] -\
            np.floor_divide(coords[:, i], box[i]) * box[i]
    return proj

def split_filament_coords_at_borders(ordered_bead_coords: np.ndarray,
                                     box) -> List[np.ndarray]:
    """
    @param ordered_bead_coords Coordinates of beads, have to be corrected via minimum image!
    """
    coordinate_sets = []
    diff = ordered_bead_coords[1:] - ordered_bead_coords[:-1]
    shifts = _compute_shifts_array(diff, box)
    shifts_at = np.where(shifts != 0)
    if len(shifts_at[0]) == 0:
        return [ordered_bead_coords]
    shifts_at_n, shifts_at_i, r_cuts = _sort_conflicting_shifts(shifts_at[0], shifts_at[1],
                                                                ordered_bead_coords, diff,
                                                                shifts, box)
    shifted_diffs = diff + shifts
    n_prev = shifts_at_n[0]
    prev_virtual_bead = None

    coord_set, prev_virtual_bead = _generate_coord_set_before_first_split(
        ordered_bead_coords[:shifts_at_n[0] + 1], n_prev, r_cuts[0], shifted_diffs)
    coordinate_sets.append(coord_set)
    for j, n in enumerate(shifts_at_n[1:]):
        j = j+1
        set_shape = list(ordered_bead_coords.shape)
        if n == n_prev:
            num_points = 2
        else:
            num_points = n - n_prev + 2
        set_shape[0] = num_points
        coord_set = np.empty(tuple(set_shape))
        if prev_virtual_bead is not None:
            prev_i = shifts_at_i[j-1]
            if isclose(prev_virtual_bead[prev_i], box[prev_i], abs_tol=box[prev_i] * 0.01):
                prev_virtual_bead[prev_i] -= box[prev_i]
            else:
                prev_virtual_bead[prev_i] += box[prev_i]
            coord_set[0] = prev_virtual_bead
        if n == n_prev:
            virtual_bead = coord_set[0] + (r_cuts[j] - r_cuts[j-1]) * shifted_diffs[n]
        else:
            coord_set[1: -1] = ordered_bead_coords[n_prev+1: n+1]
            virtual_bead = ordered_bead_coords[n] + r_cuts[j] * shifted_diffs[n]
        prev_virtual_bead = virtual_bead
        coord_set[-1] = virtual_bead

        coordinate_sets.append(coord_set)
        n_prev = n
        
    coord_set = _generate_coord_set_after_last_split(
        ordered_bead_coords, n_prev, shifts_at_i, prev_virtual_bead, box)
    
    coordinate_sets.append(coord_set)
    
    return coordinate_sets

def _generate_coord_set_before_first_split(bead_coords_before_split, n, r_cut, shifted_diffs):
    coord_set_shape = list(bead_coords_before_split.shape)
    coord_set_shape[0] = coord_set_shape[0] + 1
    coord_set = np.empty(tuple(coord_set_shape))
    coord_set[:-1] = bead_coords_before_split[:]
    virtual_bead = bead_coords_before_split[-1] + r_cut * shifted_diffs[n]
    coord_set[-1] = virtual_bead
    return coord_set, virtual_bead
    

def _generate_coord_set_after_last_split(ordered_bead_coords, n_prev,
                                         shifts_at_i, prev_virtual_bead, box):
    num_points = len(ordered_bead_coords) - n_prev
    set_shape = list(ordered_bead_coords.shape)
    set_shape[0] = num_points
    coord_set = np.empty(tuple(set_shape))
    last_i = shifts_at_i[-1]
    if isclose(prev_virtual_bead[last_i], box[last_i], abs_tol=box[last_i] * 0.01):
        prev_virtual_bead[last_i] -= box[last_i]
    else:
        prev_virtual_bead[last_i] += box[last_i]
    coord_set[0] = prev_virtual_bead
    coord_set[1:] = ordered_bead_coords[n_prev+1:]
    return coord_set

def _compute_shifts_array(diff, box):
    shifts = np.zeros_like(diff)
    for i, b in enumerate(box):
        if b is None:            
            continue
        shifts_i = -b * np.rint(diff[:, i] / b)
        shifts[:, i] = shifts_i
    return shifts
        
def _sort_conflicting_shifts(shifts_at_n, shifts_at_i,
                             ordered_bead_coords, diff, shifts, box):

    r_cuts = np.zeros(shifts_at_n.shape)
    for j in range(len(shifts_at_n)):
        conflicting_indices = []
        nj = shifts_at_n[j]
        k = j + 1
        while k < len(shifts_at_n):
            nk = shifts_at_n[k]
            if nj != nk:
                break
            conflicting_indices.append(k)
            k += 1
        if len(conflicting_indices) == 0:
            ij = shifts_at_i[j]
            dx = diff[nj, ij] + shifts[nj, ij]
            x_nj_ij = ordered_bead_coords[nj, ij]
            if x_nj_ij + dx > box[ij]:
                r_cut = abs((box[ij] - x_nj_ij) / dx)
            else:                
                r_cut = abs(x_nj_ij / dx)
            r_cuts[j] = r_cut
            continue
        conflicting_indices.insert(0, j)
        boundary_cuts = {}
        for l in conflicting_indices:
            nl = shifts_at_n[l]
            il = shifts_at_i[l]
            dx = diff[nl, il] + shifts[nl, il]
            x_nl_il = ordered_bead_coords[nl, il]
            if x_nl_il + dx > box[il]:
                r_cut = abs((box[il] - x_nl_il) / dx)
            else:                
                r_cut = abs(x_nl_il / dx)
            boundary_cuts[l] = r_cut
        sorted_boundary_cut_pairs = sorted(boundary_cuts.items(), key=lambda x: x[1])

        conflicting_shifts_in_correct_order_n = []
        conflicting_shifts_in_correct_order_i = []
        r_cuts_in_correct_order = []
        # a cut pair is a Tuple of the index in the shifts_at array and the r_cut value
        for cut_pair in sorted_boundary_cut_pairs:
            conflicting_shifts_in_correct_order_n.append(shifts_at_n[cut_pair[0]])
            conflicting_shifts_in_correct_order_i.append(shifts_at_i[cut_pair[0]])
            r_cuts_in_correct_order.append(cut_pair[1])
        shifts_at_n[j:j+len(conflicting_indices)] = conflicting_shifts_in_correct_order_n
        shifts_at_i[j:j+len(conflicting_indices)] = conflicting_shifts_in_correct_order_i
        r_cuts[j:j+len(conflicting_indices)] = r_cuts_in_correct_order
    return shifts_at_n, shifts_at_i, r_cuts
