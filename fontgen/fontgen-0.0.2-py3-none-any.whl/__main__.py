import fontmake.font_project
import fontmake.instantiator
import ufo2ft.preProcessor
import ufo2ft.featureWriters
from .setFilters import setFilters

from argparse import ArgumentParser
from unittest.mock import patch
from zipfile import ZipFile
from os.path import basename
# from extras import itf # import matraiFeatureWriter
import sys
import subprocess, os, shutil, stat, platform, json


### Change the input font family name accordingly ###

INPUT_FONT_NAME = "Amulya"
FINAL_OUTPUT_ZIP_DIR = '/Users/itf_01/IndianTypeFoundry/fontshare-fonts/Fonts-Produced'

### ============================================= ###

BASE_DIR = os.getcwd() # Directory of build.py
DEBUG_FEATURE_FILENAME = "debug.fea"
os.chdir(BASE_DIR)
TEMP_DIR = os.path.join(BASE_DIR,"temp")
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

class setfilters (object):

    def __init__(self, options):
        if options.output_formats == "var":
            self.variable_tag = True
        else:
            self.variable_tag = False
        with open( os.path.join(TEMP_DIR, "flags"), 'w') as f:
            f.write(json.dumps(self.variable_tag))



def call_glyphs2ufo(options):

    font_family_name = options.family_name

    input_filename = font_family_name + ".glyphs"
    input_dir = "masters"
    output_dir = "masters"

    # c = extras.config.glyphs2ufo
    args = ["glyphs2ufo"]

    args.extend([
        "--no-preserve-glyphsapp-metadata",
        "--no-store-editor-state",
        "--write-public-skip-export-glyphs",
        "--output-dir", output_dir,
        os.path.join(input_dir, input_filename),
    ])

    subprocess.call(args)


@patch.object(ufo2ft.preProcessor, 'loadFilters', setFilters.loadFilters_patched)
def call_fontmake(options):

    font_family_name = options.family_name

    input_filename = font_family_name + ".designspace"
    input_dir = os.path.join(BASE_DIR, "masters")
    print("input dir is " + input_dir)

    if not os.path.isdir(os.path.join(BASE_DIR, "output")):
        os.makedirs(os.path.join(BASE_DIR, "output"))

    output_dir = os.path.join(BASE_DIR, "output")
    output_path = None

    generate_features = True
    if generate_features:
        feature_writer_classes = [ufo2ft.featureWriters.MarkFeatureWriter, ufo2ft.featureWriters.KernFeatureWriter(mode="append")]

    # output_formats = [
    #     # "ufo",
    #     "otf",
    #     # "ttf",
    #     # "ttf-interpolatable",
    #     # "otf-interpolatable",
    #     # "variable",
    #     # "variable-cff2",
    # ]

    if options.output_formats == "otf":
        output_formats = ["otf"]
    elif options.output_formats == "ttf":
        output_formats = ["ttf"]
    elif options.output_formats == "otfttf":
        output_formats = ["ttf", "otf"]
    elif options.output_formats == "var":
        output_formats = ["variable"]

    if "variable" in output_formats:
        do_iup_optimization_on_gvar_table = False

    interpolate = True
    if interpolate:
        if "variable" in output_formats or "variable-cff2" in output_formats:
            name_pattern_for_interpolated_instances = ""
            # output_path = INPUT_FONT_NAME.replace(' ', '') + "-Variable"
        elif options.test_mode:
            name_pattern_for_interpolated_instances = "Regular"  # eg: ".+ Regular"
        else:
            name_pattern_for_interpolated_instances = ".+"
        round_point_coordinates_in_instances = True
        embed_external_feature_files_into_instances = True

    validate_ufo = True  # True
    remove_overlaps = True  # True
    use_production_names = False

    project = fontmake.font_project.FontProject()

    args = {}

    if options.timing:
        project.__init__(timing=True)

    if options.test_mode:
        file = open(DEBUG_FEATURE_FILENAME, "w")
        output_dir = os.path.join(os.path.join(BASE_DIR, "extras"), "products")
        args.update({"optimize_cff": 0})
        args.update({'debug_feature_file': file})

    else:
        args.update({"optimize_cff": 2})
        output_dir = output_dir

    args.update({"output_dir": output_dir})
    # args.update({"output_path": output_path})

    if generate_features:
        args.update({"feature_writers": feature_writer_classes})
    else:
        args.update({"feature_writer": None})

    args.update({"output": output_formats})

    if "variable" in output_formats and not do_iup_optimization_on_gvar_table:
        args.update({"optimize_gvar": False})

    if interpolate:
        args.update({"interpolate": name_pattern_for_interpolated_instances})

        if round_point_coordinates_in_instances:
            args.update({"round_instances": True})

        if embed_external_feature_files_into_instances:
            args.update({"expand_features_to_instances": True})
    else:
        args.update({"masters_as_instances": True})

    if validate_ufo:
        project.validate_ufo = True
    if not remove_overlaps:
        args.update({"remove_overlaps": False})
    if use_production_names:
        args.update({"use_production_names": True})
    else:
        args.update({"use_production_names": False})

    project.__init__(verbose=options.fontmake_verbose_level)

    designspacepath = os.path.join(input_dir, input_filename)

    project.run_from_designspace(designspacepath, **args)

    if options.test_mode:
        file.close()


def remove_readonly(func, path, _):
    "Clear the readonly bit and reattempt the removal"
    os.chmod(path, stat.S_IWRITE)
    func(path)


def cleanup():
    srcpath = os.path.join(BASE_DIR, "output")
    destpath = os.path.join(BASE_DIR, "output")
    otf_path = os.path.join(srcpath, "OTF")
    variable_path = os.path.join(srcpath, "TTF")
    info_path = os.path.join(BASE_DIR, "info.txt")

    font_family_name = ""

    if os.path.exists(os.path.join(destpath, "fonts")):
        shutil.rmtree(os.path.join(destpath, "fonts"))
    if os.path.exists(os.path.join(destpath, "info")):
        shutil.rmtree(os.path.join(destpath, "info"))

    for root, subFolders, files in os.walk(srcpath):
        for file in files:
            if ("-Variable" in file) or ("-VF" in file):
                if ".ttf" in file:
                    if ("Italic" in file) or ("Italics" in file):
                        xxx = file.split(" ")
                        xxx.pop()
                        newFileName = ""
                        for x in xxx:
                            newFileName = newFileName + x
                        newFileName = newFileName + "-VariableItalic.ttf"
                    else:
                        xxx = file.split("-")
                        xxx.pop()
                        newFileName = ""
                        for x in xxx:
                            newFileName = newFileName + x
                        newFileName = newFileName + "-Variable.ttf"
                        newFileName = newFileName.replace(" ", "")

                    subFolder = os.path.join(destpath, "TTF")
                    if not os.path.isdir(subFolder):
                        os.makedirs(subFolder)
                    if os.path.exists(os.path.join(subFolder, file)):
                        os.remove(os.path.join(subFolder, file))
                    shutil.copy(os.path.join(root, file), subFolder)
                    os.rename(os.path.join(subFolder, file), os.path.join(subFolder, newFileName))
                # print("This is variable")
                continue
            elif ".otf" in file:
                subFolder = os.path.join(destpath, "OTF")
                if not os.path.isdir(subFolder):
                    os.makedirs(subFolder)
                if os.path.exists(os.path.join(subFolder, file)):
                    os.remove(os.path.join(subFolder, file))
                shutil.copy(os.path.join(root, file), subFolder)

                font_family_name = file.split("-")[0]
        break

    platform_name = platform.system()

    fonts_path = os.path.join(srcpath, "fonts")

    if not os.path.isdir(fonts_path):
        os.makedirs(fonts_path)

    if os.path.exists(os.path.join(srcpath, "info")):
        shutil.rmtree(os.path.join(srcpath, "info"))
    if os.path.exists(os.path.join(fonts_path, "OTF")):
        shutil.rmtree(os.path.join(fonts_path, "OTF"))
    if os.path.exists(os.path.join(fonts_path, "TTF")):
        shutil.rmtree(os.path.join(fonts_path, "TTF"))

    if not os.path.isdir(os.path.join(srcpath, "info")):
        os.makedirs(os.path.join(srcpath, "info"))

    shutil.move(otf_path, fonts_path)
    if os.path.isdir(variable_path):
        shutil.move(variable_path, fonts_path)
    shutil.copy(info_path, os.path.join(srcpath, "info"))

    test_range = []
    for i in range(1, len(font_family_name)):
        if font_family_name[i].isupper():
            test_range.append(i)

    abcd = 0
    zip_family_name = ""
    for t in test_range:
        zip_family_name = zip_family_name + font_family_name[abcd:t] + "-"
        abcd = t
    zip_family_name = zip_family_name + font_family_name[abcd:]
    zip_family_name = zip_family_name.lower()

    def zipdir(path, zipObj):
        for root, dirs, files in os.walk(path):
            for file in files:
                zipObj.write(os.path.join(root, file),
                             os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))

    if zip_family_name == "r-x100":
        zip_family_name = "rx-100"

    zip_dir_path = os.path.join(BASE_DIR, zip_family_name)
    if os.path.isfile(zip_family_name + ".zip"):
        os.remove(zip_family_name + ".zip")
    if os.path.exists(zip_dir_path):
        shutil.rmtree(zip_dir_path)
    os.makedirs(zip_dir_path)
    shutil.move(fonts_path, zip_dir_path)
    shutil.move(os.path.join(srcpath, "info"), zip_dir_path)

    with ZipFile(zip_family_name + ".zip", 'w') as zipObj:
        zipdir(zip_dir_path, zipObj)
        # zipdir(os.path.join(srcpath, "info"), zipObj)
    zipObj.close()
    shutil.rmtree(zip_dir_path)

    #### shutil.copy(zip_family_name + ".zip", FINAL_OUTPUT_ZIP_DIR)

    if platform_name == "Darwin":
        print("This is MAC")
        ADOBE_FONTS_DIR = "/Library/Application Support/Adobe/Fonts/"
        for folderName, subfolders, filenames in os.walk(otf_path):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                shutil.copy(filePath, ADOBE_FONTS_DIR)

    if platform_name == "Windows":
        print("This is Windows")
        # ADOBE_FONTS_DIR = "C:\Users\Rahul Gajjar\AppData\Roaming\Adobe\Fonts"
        for folderName, subfolders, filenames in os.walk(otf_path):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                shutil.copy(filePath, ADOBE_FONTS_DIR)

    print("Cleanup finished")

def loadconfig(options):

    module_dir = os.path.dirname(os.path.abspath(__file__))
    ini_dir = os.path.join(module_dir, "config")
    ini_file_name = options.load_config + ".ini"
    ini_file_path = os.path.join(ini_dir,ini_file_name)

    default_config_path = os.path.join(ini_dir, "config.ini")
    test_config_path = os.path.join(ini_dir, "test.ini")

    if options.load_config == "reset":
        shutil.copy(test_config_path, default_config_path)
        print("Config has been reset")
    elif os.path.isfile(os.path.join(ini_dir,ini_file_name)):
        # Copy selected ini file and make a copy with name config.ini
        shutil.copy(ini_file_path,default_config_path)
        print("Config file {} has been set".format(ini_file_name))
    else:
        print("File {} not found".format(ini_file_name))

def saveconfig(options):

    module_dir = os.path.dirname(os.path.abspath(__file__))
    ini_dir = os.path.join(module_dir, "config")

    load_ini_dir = BASE_DIR
    load_ini_file_name = options.save_config + ".ini"
    load_ini_file_path = os.path.join(load_ini_dir,load_ini_file_name)

    default_config_path = os.path.join(ini_dir, load_ini_file_name)

    if os.path.isfile(load_ini_file_path):
        # Copy selected ini file and make a copy with name config.ini
        shutil.copy(load_ini_file_path, default_config_path)
        print("Config file {} has been saved".format(load_ini_file_name))
    else:
        print("File {} not found".format(load_ini_file_name))



def main(args=None):
    parser = ArgumentParser()

    # outputGroup = parser.add_argument_group(title="Font Family Name")
    parser.add_argument(
        "-f",
        "--family-name",
        default=INPUT_FONT_NAME,
        metavar="FAMILYNAME",
        help="Type font family name. Make sure source files are in \'masters\' folder",
    )

    parser.add_argument(
        "-o",
        "--output-formats",
        default="all",
        metavar="OUTPUTFORMATS",
        help="Output font formats. Choose one: otf, ttf, var or otfttf Default: otf and variable",
    )

    parser.add_argument(
        "-lc",
        "--load-config",
        default="config",
        metavar="LOADCONFIG",
        help="Load a saved configuration file for automated font info generation. Choose the name of config you previously saved. To reset config type: -lc reset",
    )

    parser.add_argument(
        "-sc",
        "--save-config",
        default="config",
        metavar="SAVECONFIG",
        help="Save a configuration file for automated font info generation. Make sure you have yourconfig.ini file in current directory. Load a configuration after it has been set: -lc yourconfig",
    )


    parser.add_argument("-g", "--glyphs", action="store_true", dest="run_glyphs2ufo",
                        help='Use glyphs file to generate designspace and use that designspace for fontmake')

    parser.add_argument("-gd", "--glyphs2designspace", action="store_true", dest="only_run_glyphs2ufo",
                        help='Only generate designspace from glyphsapp file')

    parser.add_argument("-t", "--test", action="store_true", dest="test_mode",
                        help='Test mode for faster testing')

    parser.add_argument("--timing", action="store_true", help='Shows how much time it took to complete the process')

    parser.add_argument(
        "-v",
        "--fontmake-verbose-level",
        default="INFO",
        metavar="LEVEL",
        choices=("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"),
        help="Choose verbose level from DEBUG, INFO, WARNING, ERROR, and CRITICAL. Default value is INFO"
    )

    parser.add_argument("-c", "--cleanup", action="store_true", dest="cleanup_and_rename",
                        help='Move files from output dir and make zip file for fontstore')

    # parser.add_argument("-otf", "--otfonly", action="store_true", dest="otf_only",
    #                     help='Generate only OTF files')
    #
    # parser.add_argument("-var", "--variableonly", action="store_true", dest="variable_only",
    #                     help='Generate only TTF Variable files')
    #
    # parser.add_argument("-all", "--otfandvariable", action="store_true", dest="all_files_and_cleanup",
    #                     help='Generate OTF and Variable files and cleanup after production')

    options = parser.parse_args()

    setfilters(options)

    if options.run_glyphs2ufo:
        call_glyphs2ufo(options)
        call_fontmake(options)
    elif options.only_run_glyphs2ufo:
        call_glyphs2ufo(options)
    elif options.cleanup_and_rename:
        cleanup()
    elif options.test_mode:
        call_fontmake(options)
    elif options.output_formats == "otf":
        call_fontmake(options)
    elif options.output_formats == "ttf":
        call_fontmake(options)
    elif options.output_formats == "var":
        call_fontmake(options)
    elif options.output_formats == "otfttf":
        call_fontmake(options)
    elif not options.load_config == "config":
        loadconfig(options)
    elif not options.save_config == "config":
        saveconfig(options)
    elif options.output_formats == "all":

        print("Generating otf and ttf files for font family{}".format(options.family_name))

        options.output_formats = "otf"
        setfilters(options)
        call_fontmake(options)

        # options.otf_only = False  # Resetting the flag

        options.output_formats = "var"
        setfilters(options)
        call_fontmake(options)
        # options.variable_only = False  # Resetting the flag

        cleanup()
    else:
        print("Please provide correct options. For help type: fontgen -h")


if __name__ == "__main__":
    sys.exit(main())