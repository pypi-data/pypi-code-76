import sys
import os
import cv2
import pandas as pd
from shutil import copyfile
from configparser import ConfigParser
sys.path.append('../')

try:
    import visualization as visu      # noqa: E402
except ImportError:
    import tools.visualization as visu      # noqa: E402
try:
    import optimization as opt      # noqa: E402
except ImportError:
    import tools.optimization as opt      # noqa: E402
try:
    import grids                  # noqa: E402
except ImportError:
    pass

# Imports for loading config files

# ------------------------ Import config parameters --------------#
conf_cv2 = ConfigParser()
conf_cv2.read('./config/config_cv2.cfg')

# --- FUNCTIONS RELATED TO EXPORTING AND IMPORTING GRIDS FROM EXTERNAL FILE --#


def make_folder(folder):
    """
    If no folder of the given name already exists, create new one.

    Parameters
    ----------
    folder: str
        Name of the folder to be created.
    """

    if not os.path.exists(folder):
        parent_folders = folder.split('/')
        for i in range(1, len(parent_folders) + 1):
            path = ''
            for x in parent_folders[0:i]:
                path += x + '/'
            if not os.path.exists(path[0:-1]):
                os.mkdir(path[0:-1])


def export_grid(grid,
                backup_name=None,
                folder=None,
                allow_saving_in_existing_backup_folder=False,
                empty_background=False,
                save_image=True):
    """
    Export grid in folder as separated files:
        - nodes.csv
            contains the _nodes attribute data
        - links.csv
            contains the _links attribute data
        - initial_image(.jpeg or .png)
            contains initial image
        - about.json
            contains info about the grid (creation date and _id)
        - grid_config.py
            backup of the config.py file used for the grid

    Parameters
    ----------
    grid: :class:`~.grids.Grid`
            Grid object.
    folder: str
        Path of the folder the grid should be saved in
    backup_name: str
        Name of the grid backup.

    allow_saving_in_existing_backup_folder: bool
        When True and a folder with the same name as the parameter
        backup_name, no new folder is created and the grid is exported in
        the folder of the backup_name.
        When False and a folder with the same name as the parameter
        backup_name exists, a new folder is created with a extension _i
        (where i is an integer).

     empty_background: bool
        When True, an image of the grid network is saved on a transparent
        background.

    save_image: bool
        Determines whether or not the images (grid image and initial image)
        are saved in the backup folder.

    Notes
    -----
        If no folder is given, the default path to folder is
        f'data/backup/{grid._id}/'.

        If no folder name is given, the grid will be saved in a folder called
        f'backup_{grid._id}_{counter}', where counter is a index added
        to distiguish backups of the same grid.
    ----------
    """

    if folder is None:
        folder = 'data/backup/' + grid.get_id()
        make_folder('data')
        make_folder('data/backup')
        make_folder(folder)
    else:
        if not os.path.exists(folder):
            parent_folders = folder.split('/')
            for i in range(1, len(parent_folders) + 1):
                path = ''
                for x in parent_folders[0:i]:
                    path += x + '/'
                make_folder(path[0:-1])

    if backup_name is None:
        backup_name = f'backup_{grid.get_id()}'

    if not allow_saving_in_existing_backup_folder:
        if os.path.exists(f'{folder}/{backup_name}'):
            counter = 1
            while os.path.exists(
                   f'{folder}/{backup_name}_{counter}'):
                counter += 1
            backup_name = f'{backup_name}_{counter}'
    full_path = f'{folder}/{backup_name}'

    make_folder(full_path)

    # Export nodes dataframe into csv file
    grid.get_nodes().to_csv(full_path + '/nodes.csv')

    # Export links dataframe into csv file
    grid.get_links().to_csv(full_path + '/links.csv')

    # Copy config files

    copyfile('./config/config_grid.cfg', full_path + '/config_grid.cfg')
    copyfile('./config/config_cv2.cfg', full_path + '/config_cv2.cfg')

    # Update config files
    config_grid = ConfigParser()
    config_grid.read(full_path + '/config_grid.cfg')
    config_grid.set('files', 'meter_per_pixel_ratio',
                    str(grid.get_meter_per_pixel_ratio()))
    config_grid.set('files', 'village_name',
                    str(grid.get_id()))

    with open(full_path + '/config_grid.cfg', "w+") as configfile:
        config_grid.write(configfile)

    # Save initial and grid images
    if save_image:
        visu.draw_grid(grid)
        cv2.imwrite(full_path + '/initial_image.png', grid.get_initial_image())
        cv2.imwrite(full_path + '/Grid_' + str(grid.get_id())
                    + '.png', grid.get_image())
        if empty_background is True:
            cv2.imwrite(full_path + '/Grid_empty_background.png',
                        visu.transparent_grid_image(grid))

    print(f'Grid saved in \n{full_path}\n\n')


def import_grid(folder):
    """
    Import a grid that was previously exported using the export_grid
    function.

    Parameters
    ----------
    folder: str
        Path to the folder where the backup files (nodes.csv, links.csv
        initial_image(.jpeg or .png), about.json and grid_config.py)
        of the given grid have been saved in.
    Returns
    -------
        Copy of the exported Grid located in the folder defined by the path.
    """

    # Save path to image
    if os.path.exists(folder + '/initial_image.png'):
        path_to_image = folder + '/initial_image.png'
    elif os.path.exists(folder + '/initial_image.jpeg'):
        path_to_image = folder + '/initial_image.jpeg'
    elif os.path.exists(folder + '/initial_image.JPG'):
        path_to_image = folder + '/initial_image.JPG'
    else:
        path_to_image = None

    # Import grid id from config_grid.cfg file
    config_grid = ConfigParser()
    config_grid.read(folder + '/config_grid.cfg')
    grid_id = config_grid.get('files', 'village_name')
    meter_per_pixel_ratio = config_grid.getfloat('files',
                                                 'meter_per_pixel_ratio')

    # Import data from csv files to nodes and links DataFrames
    nodes = pd.read_csv(folder + '/nodes.csv',
                        converters={
                            'label': str,
                            'pixel_x_axis': int,
                            'pixel_y_axis': int,
                            'node_type': str,
                            'type_fixed':
                                lambda x: True if x == 'True' else False,
                            'segment': str,
                            'allocation_capacity': int})
    nodes = nodes.set_index('label')

    links = pd.read_csv(folder + '/links.csv',
                        converters={'from': str,
                                    'to': str,
                                    'type': str,
                                    'distance': float,
                                    },
                        index_col=[0])
    # Create new Grid
    grid = grids.Grid(_id=grid_id,
                      _nodes=nodes,
                      _links=links,
                      _image_path=path_to_image,
                      _meter_per_pixel_ratio=meter_per_pixel_ratio,
                      _path_config_files=folder + 'config_grid.cfg')
    opt.link_nodes(grid)

    return grid
