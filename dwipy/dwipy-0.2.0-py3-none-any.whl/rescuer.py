try:
    from PIL import Image
except ImportError:
    import Image

import os
import re

from glob import glob
import shutil

import cv2
import numpy as np
import pydicom
import pytesseract
import SimpleITK as sitk

import dwipy.IO.gradient_table
import dwipy.IO.misc
import dwipy.constants
import dwipy.IO.converters
import dwipy.mrtrixpy
import dwipy.qa

# This requires the installation of tesseract 4.1.1 according to: https://medium.com/quantrium-tech/installing-tesseract-4-on-ubuntu-18-04-b6fcd0cbd78f

#############
## Functions to extract b-values if not directly found
###########
def extract_b_value_from_burned_in_annotation(DICOM_path):
    dicom_files = glob(os.path.join(DICOM_path, "*.dcm"))

    n_dcm_files_no_data = 0

    for i_dcm_file in dicom_files:
        fixed_b = False
        print(i_dcm_file)
        img_array = sitk.GetArrayFromImage(sitk.ReadImage(i_dcm_file))
        img_array = np.squeeze(img_array)
        # Assume high intensity for the text itself
        img_array[img_array != 2000] = 0
        img_array = cv2.resize(img_array, None, fx=6, fy=6, interpolation=cv2.INTER_CUBIC)

        try:
            ocr_text = pytesseract.image_to_string(
                img_array,
                config="--psm 13 -c load_system_dawg=false -c load_freq_dawg=false -c tessedit_char_whitelist==ADCadcbTSPR0123456789",
            )
        except:
            ocr_text = None

        if ocr_text is not None:
            ocr_text = ocr_text.strip()
            if "b=" in ocr_text or "5=" in ocr_text:
                if "b=" in ocr_text:
                    bval = ocr_text.split("b=")[-1]
                if "5=" in ocr_text:
                    bval = ocr_text.split("5=")[-1]
                # print(bval)
                last_zero = bval.rfind("0")
                # We cut off everything after 0 if there is any weird things left
                bval_only = bval[: last_zero + 1]
                bval_direction = bval[last_zero + 1 :]

                out_bval_direction = None

                if bval_direction == "T" or bval_direction == "7":
                    out_bval_direction = [0, 0, 0]
                elif bval_direction == "P":
                    out_bval_direction = [0, 1, 0]
                elif bval_direction == "S" or bval_direction == "5":
                    out_bval_direction = [0, 0, 1]
                elif bval_direction == "R" or bval_direction == "3":
                    out_bval_direction = [1, 0, 0]

                if bval_only == "S00":
                    bval_only = "500"
                elif bval_only == "S0":
                    bval_only = "50"
                # print(bval_only)
                i_dcm = pydicom.dcmread(i_dcm_file)
                i_dcm.add_new([0x0018, 0x9087], "DS", bval_only)
                if out_bval_direction is not None:
                    i_dcm.add_new([0x0018, 0x9089], "FD", out_bval_direction)
                pydicom.dcmwrite(i_dcm_file, i_dcm)
                fixed_b = True
            elif "abc" in ocr_text.lower() or "adc" in ocr_text.lower():
                # ADC slice, we don't want that.
                os.remove(i_dcm_file)
                fixed_b = True

        if not fixed_b:
            n_dcm_files_no_data += 1

        if n_dcm_files_no_data > 5:
            break
    return fixed_b


def extract_b_value_from_description(DICOM_path):
    dicom_files = glob(os.path.join(DICOM_path, "*.dcm"))

    fixed_b = False

    for i_dicom_file in dicom_files:
        i_dcm = pydicom.dcmread(i_dicom_file)
        diffusion_value = None
        if [0x18, 0x24] in i_dcm:
            sequence_name = i_dcm[0x18, 0x24].value
            diffusion_regex_expressions = ["ep_b(\d+)", "re_b(\d+)"]
            i_regex_expression = 0
            while diffusion_value is None and i_regex_expression < len(diffusion_regex_expressions):
                diffusion_value = re.search(
                    diffusion_regex_expressions[i_regex_expression], sequence_name
                )
                if diffusion_value is not None:
                    diffusion_value = diffusion_value.groups(0)[0].strip()
                i_regex_expression += 1
        if [0x0018, 0x1030] in i_dcm and diffusion_value is None:
            protocol_name = i_dcm[0x18, 0x1030].value
            diffusion_value = re.search("eB(\d+)", protocol_name)
            if diffusion_value is not None:
                diffusion_value = diffusion_value.groups(0)[0].strip()
            else:
                if protocol_name == "eBo":
                    diffusion_value = 0

        if [0x8, 0x8] in i_dcm and diffusion_value is None:
            image_type = i_dcm[0x8, 0x8].value

            if isinstance(image_type, pydicom.multival.MultiValue):
                image_type = "/".join(list(image_type))

            diffusion_value = re.search("DW_(\d+)", image_type)
            if diffusion_value is not None:
                diffusion_value = diffusion_value.groups(0)[0].strip()

        # if diffusion_value is not None:
        #     i_dcm.add_new([0x0018, 0x9087], "DS", diffusion_value)

        #     pydicom.dcmwrite(i_dicom_file, i_dcm)
        #     if not fixed_b:
        #         fixed_b = True
    return fixed_b


def deep_search_b_values(dicom_path: str):
    # First we try to extract them from the description
    fixed_b = extract_b_value_from_description(dicom_path)
    if not fixed_b:
        # We now try to get it from burned in annotation
        fixed_b = extract_b_value_from_burned_in_annotation(dicom_path)

    return fixed_b


#########
## Fixes for b-values that are too high (i.e. 100001000)
########


def fix_high_b_value(DICOM_path):
    # GE specific fix
    dicom_files = glob(os.path.join(DICOM_path, "*.dcm"))

    fixed_b = False

    for i_dicom_file in dicom_files:
        i_dcm = pydicom.dcmread(i_dicom_file)
        diffusion_value = None
        if [0x0043, 0x1039] in i_dcm:
            dwi_values = i_dcm[0x43, 0x1039].value
            if dwi_values[0] > 5000:
                dwi_temp_val = dwi_values[0]
                dwi_temp_val = np.mod(dwi_temp_val, 1000000)
                if dwi_temp_val < 5000 and dwi_temp_val > 0:
                    dwi_values[0] = dwi_temp_val
                    diffusion_value = dwi_temp_val
                else:
                    diffusion_value = None
        if diffusion_value is not None:
            i_dcm[0x43, 0x1039].value = dwi_values

            pydicom.dcmwrite(i_dicom_file, i_dcm)
            if not fixed_b:
                fixed_b = True
    return fixed_b


###########
### Functions to fix cases where there is only 1 b value
##########


def fix_single_b_value(dicom_path):
    # First we convert to nifti to check if there are multiple images
    tmpdir = dwipy.IO.misc._get_tmp_dir()
    nifti_file = os.path.join(tmpdir, "DWI.nii.gz")
    dwipy.mrtrixpy.mrconvert(dicom_path, nifti_file)

    image_file = None
    grad_file = None
    fixed_b = False

    if has_visual_appearance_of_more_than_one_b(nifti_file):
        tmp_file = os.path.join(tmpdir, "DWI")
        image_file, grad_file = dwipy.IO.converters.dcm2mif(dicom_path, tmp_file)
        grads = dwipy.IO.gradient_table.load_mrtrix_grads(grad_file)

        fixed_b, fixed_grads = fix_high_intensity_single_b_value(nifti_file, grads)

        formatted_grad_vals = [
            "dw_scheme " + ",".join(i_grad.astype(int).astype(str)) for i_grad in fixed_grads
        ]
        # print(formatted_grad_vals)

        fixed_image_file = os.path.join(tmpdir, "DWI_FIXED_BVALS.mif.gz")
        dwipy.mrtrixpy.mrconvert(
            image_file,
            fixed_image_file,
            {"clear_property": "dw_scheme", "append_property": tuple(formatted_grad_vals)},
        )

        fixed_grads_file = os.path.join(tmpdir, "DWI_FIXED_BVALS.grads")
        dwipy.IO.gradient_table.write_mrtrix_grads(fixed_grads_file, fixed_grads)

        image_file = fixed_image_file
        grad_file = fixed_grads_file
        fixed_b = True

    return image_file, grad_file, fixed_b


def has_visual_appearance_of_more_than_one_b(nifti_file):
    more_than_one_b = False
    scan = sitk.ReadImage(nifti_file)
    if scan.GetDimension() == 4:
        scan = sitk.GetArrayFromImage(scan)
        means = []

        for i_shell in range(scan.shape[0]):
            means.append(np.mean(scan[i_shell, :]))

        more_than_one_b = np.amax(means) >= 1.1 * np.mean(means)

    return more_than_one_b


def fix_high_intensity_single_b_value(nifti_file, grads):
    # MAybe not possible in DICOM
    # Need to figure out some way to do it directly from MIF/NIFTI and then parse back the b-values
    image = sitk.ReadImage(nifti_file)
    fixed_b = False

    if image.GetDimension() == 4 and image.GetSize()[-1] == 2:
        scan = sitk.GetArrayFromImage(image)

        scan_0_mean = np.mean(scan[0, :])
        scan_1_mean = np.mean(scan[1, :])

        if scan_0_mean > 1.1 * scan_1_mean:
            grads[0, 3] = 0
            fixed_b = True
        elif scan_1_mean > 1.1 * scan_0_mean:
            grads[1, 3] = 0
            fixed_b = True

    return fixed_b, grads


####################3
## Functions for missing/too many slices
#############


def remove_superflous_slices(dicom_path):
    fixed_b = False
    dicom_files = glob(os.path.join(dicom_path, "*.dcm"))

    slice_locations = []
    for i_dcm_file in dicom_files:
        dcm = pydicom.dcmread(i_dcm_file)
        slice_locations.append(dcm[0x20, 0x1041].value)

    unique_members, counts = np.unique(slice_locations, return_counts=True, return_index=False)

    try:
        if len(np.argwhere(counts == 1)) == 1:
            to_remove_index = unique_members[int(np.squeeze(np.argwhere(counts == 1)))]
            to_remove_index = int(np.squeeze(np.argwhere(slice_locations == to_remove_index)))
            os.remove(dicom_files[to_remove_index])
            fixed_b = True
    except:
        pass

    return fixed_b


######################
# Fix nan values
######################


def fix_nan_b_vals(dicom_path):
    fixed_b = False
    dicom_files = glob(os.path.join(dicom_path, "*.dcm"))

    bvals = []
    missing_bvals = []
    for i_dcm_file in dicom_files:
        dcm = pydicom.dcmread(i_dcm_file)
        if [0x18, 0x9087] in dcm:
            bvals.append(dcm[0x18, 0x9087].value)
        else:
            missing_bvals.append(i_dcm_file)

    if len(missing_bvals) < len(dicom_files) and np.count_nonzero(bvals) > 0:
        for i_dcm_file in missing_bvals:
            dcm = pydicom.dcmread(i_dcm_file)
            dcm.add_new([0x0018, 0x9087], "DS", 0)
            pydicom.dcmwrite(i_dcm_file, dcm)
            fixed_b = True
    return fixed_b


###############3
# Fix DTI with only one directoin
#####


def fix_dti_one_direction(dicom_path):
    # First we convert to nifti to check if there are multiple images
    tmpdir = dwipy.IO.misc._get_tmp_dir()
    tmp_file = os.path.join(tmpdir, "DWI")
    image_file, grad_file = dwipy.IO.converters.dcm2mif(dicom_path, tmp_file)
    grads = dwipy.IO.gradient_table.load_mrtrix_grads(grad_file)

    # Fix the grads
    grads[:, 0:3] = 0
    formatted_grad_vals = [
        "dw_scheme " + ",".join(i_grad.astype(int).astype(str)) for i_grad in grads
    ]

    fixed_image_file = os.path.join(tmpdir, "DWI_FIXED_BVALS.mif.gz")
    dwipy.mrtrixpy.mrconvert(
        image_file,
        fixed_image_file,
        {"clear_property": "dw_scheme", "append_property": tuple(formatted_grad_vals)},
    )

    fixed_grads_file = os.path.join(tmpdir, "DWI_FIXED_BVALS.grads")
    dwipy.IO.gradient_table.write_mrtrix_grads(fixed_grads_file, grads)

    image_file = fixed_image_file
    grad_file = fixed_grads_file
    fixed_b = True

    return image_file, grad_file, fixed_b


########
## General functions
######


def rescue_dwi(dicom_path: str, bval_status: dwipy.constants.GRADSTATUS):
    image_file = None
    grad_file = None
    conversion_successful = False
    tmp_dir = dwipy.IO.misc._get_tmp_dir()
    image_file = os.path.join(tmp_dir, "DWI")
    if bval_status is dwipy.constants.GRADSTATUS.BVALS_TOO_HIGH:
        fixed_b = fix_high_b_value(dicom_path)
        if fixed_b:
            (image_file, grad_file,) = dwipy.IO.converters.dcm2mif(
                dicom_path,
                image_file,
            )
            conversion_successful = (
                dwipy.qa.check_grad_file_status(grad_file) is dwipy.constants.GRADSTATUS.VALID_GRADS
            )
    elif bval_status is dwipy.constants.GRADSTATUS.BVALS_HAS_NAN:
        fixed_b = fix_nan_b_vals(dicom_path)
        if fixed_b:
            (image_file, grad_file,) = dwipy.IO.converters.dcm2mif(
                dicom_path,
                image_file,
            )
            conversion_successful = (
                dwipy.qa.check_grad_file_status(grad_file) is dwipy.constants.GRADSTATUS.VALID_GRADS
            )

    elif bval_status is dwipy.constants.GRADSTATUS.GRADS_NOT_FOUND:
        removed_slices = False
        if dwipy.IO.misc.get_number_of_dcm_files(dicom_path) % 2 != 0:
            # Unequal number of files, need to fix this
            removed_slices = remove_superflous_slices(dicom_path)

        fixed_b = deep_search_b_values(dicom_path)
        print(fixed_b)
        if fixed_b or removed_slices:
            image_file, grad_file = dwipy.IO.converters.dcm2mif(dicom_path, image_file)
            print(dwipy.qa.check_grad_file_status(grad_file))
            conversion_successful = (
                dwipy.qa.check_grad_file_status(grad_file) is dwipy.constants.GRADSTATUS.VALID_GRADS
            )
            print("final")
            print(conversion_successful)
            print("final")
    elif bval_status is dwipy.constants.GRADSTATUS.ONE_BVAL:
        image_file, grad_file, conversion_successful = fix_single_b_value(dicom_path)
    elif bval_status is dwipy.constants.GRADSTATUS.DTI_ONE_DIRECTION:
        image_file, grad_file, conversion_successful = fix_dti_one_direction(dicom_path)
    return image_file, grad_file, conversion_successful
