import os
import shutil
import glob

import numpy as np

import dwipy.constants
import dwipy.IO.gradient_table
import dwipy.IO.misc
import dwipy.mrtrixpy
import dwipy.qa


def get_adc_from_image(image_file: str, grad_file: str, out_folder: str):

    dwi_type = dwipy.qa.get_dwi_type(grad_file)
    if dwi_type is dwipy.constants.DWITYPE.DWI_SINGLE_TRACE:
        _get_adc_from_trace_dwi(image_file, out_folder)
    elif dwi_type is dwipy.constants.DWITYPE.DWI_MULTI_B_VECS:
        _get_adc_from_dwi_with_bvecs(image_file, grad_file, out_folder)
    elif (
        dwi_type is dwipy.constants.DWITYPE.DWI_MULTI_TRACE
        or dwi_type is dwipy.constants.DWITYPE.DWI_TRACE_NONZERO_BVAL
    ):
        _get_adc_from_multi_trace_dwi(image_file, grad_file, out_folder)
    elif dwi_type is dwipy.constants.DWITYPE.DWI_MULTI_B_VECS_AND_TRACE:
        _get_adc_from_dwi_with_bvecs_and_trace(image_file, grad_file, out_folder)
    elif dwi_type is dwipy.constants.DWITYPE.DTI:
        _get_adc_from_dti(image_file, out_folder)

    return glob.glob(os.path.join(out_folder, "*_ADC.nii.gz"))


def _normalize_adc(adc_file: str):
    tmpdir = dwipy.IO.misc._get_tmp_dir()
    adc_multiplied_file = os.path.join(tmpdir, "ADC_multiplied.nii.gz")
    dwipy.mrtrixpy.mrcalc(adc_file, adc_multiplied_file, {"multiply": "1000"})

    adc_low_threshold_file = os.path.join(tmpdir, "ADC_low_threshold.nii.gz")
    dwipy.mrtrixpy.mrcalc(adc_multiplied_file, adc_low_threshold_file, {"max": "0"})

    adc_high_threshold_file = os.path.join(tmpdir, "ADC_high_threshold.nii.gz")
    dwipy.mrtrixpy.mrcalc(adc_low_threshold_file, adc_high_threshold_file, {"min": "100"})

    return adc_high_threshold_file


def _get_adc_from_trace_dwi(image_file, out_folder):
    tmpdir = dwipy.IO.misc._get_tmp_dir()

    file_name_basis = dwipy.IO.misc.get_file_base_name_without_extension(image_file)
    adc_and_b0_file = os.path.join(tmpdir, "ADC_B0.nii.gz")

    # Convert the image to a combined ADC and B0 file
    dwipy.mrtrixpy.dwi2adc(image_file, adc_and_b0_file, {})

    # First we extract the ADC file
    adc_extracted_file = os.path.join(tmpdir, "ADC_extracted.nii.gz")
    dwipy.mrtrixpy.mrconvert(
        adc_and_b0_file, adc_extracted_file, {"coord": ["3", "1"], "axes": "0,1,2"}
    )

    adc_final_file = _normalize_adc(adc_extracted_file)

    b0_extracted_file = os.path.join(tmpdir, "B0.nii.gz")
    dwipy.mrtrixpy.mrconvert(
        adc_and_b0_file, b0_extracted_file, {"coord": ["3", "0"], "axes": "0,1,2"}
    )

    shutil.copy(adc_final_file, os.path.join(out_folder, file_name_basis + "_ADC.nii.gz"))
    shutil.copy(b0_extracted_file, os.path.join(out_folder, file_name_basis + "_B0.nii.gz"))


def _get_adc_from_dwi_with_bvecs(image_file: str, grad_file: str, out_folder):
    # in this case we have a DWI with bvecs
    # This means we have multiple vectors for a certain bvalue
    # But this vectors are (approximately) only in x/y/z direction
    # Also, we can have multiple b-values that have 3 b-vectors in the x/y/z direction
    tmpdir = dwipy.IO.misc._get_tmp_dir()

    file_name_basis = dwipy.IO.misc.get_file_base_name_without_extension(image_file)

    bvals = dwipy.IO.gradient_table.load_mrtrix_bvals(grad_file)
    unique_bval, idx, bval_counts = np.unique(bvals, return_index=True, return_counts=True)
    # By default unique sorts the bvals
    # But we want them in their original order
    original_order_bvals = bvals[np.sort(idx)]
    individual_b_images = {}
    grad_scheme = {}
    for idx, (i_unique_bval, i_count) in enumerate(zip(original_order_bvals, bval_counts)):
        # First we take the mean over the b-shells
        out_file_this_b = os.path.join(tmpdir, "TRACE_B" + str(i_unique_bval) + ".mif.gz")

        if i_count > 1:
            this_b_indexes = np.squeeze(np.argwhere(bvals == i_unique_bval))
            this_b_indexes = [str(int(i_this_b_indexes)) for i_this_b_indexes in this_b_indexes]
            this_b_indexes = ",".join(this_b_indexes)
            dwipy.mrtrixpy.mrconvert(image_file, out_file_this_b, {"coord": ["3", this_b_indexes]})
            out_file_this_b_product = os.path.join(
                tmpdir, "TRACE_B_PROD_" + str(i_unique_bval) + "_COR.mif.gz"
            )
            dwipy.mrtrixpy.mrmath(
                out_file_this_b, out_file_this_b_product, "product", {"axis": "3"}
            )
            out_file_this_b_corrected = os.path.join(
                tmpdir, "TRACE_B" + str(i_unique_bval) + "_COR.mif.gz"
            )
            dwipy.mrtrixpy.mrcalc(
                out_file_this_b_product,
                out_file_this_b_corrected,
                {"pow": str(np.around(1 / i_count, decimals=5))},
            )
            out_file_this_b = out_file_this_b_corrected
        else:
            dwipy.mrtrixpy.mrconvert(
                image_file, out_file_this_b, {"coord": ["3", str(int(idx))], "axes": "0,1,2"}
            )
        individual_b_images[i_unique_bval] = out_file_this_b
        grad_scheme[i_unique_bval] = "dw_scheme 0,0,0," + str(int(i_unique_bval))

    max_b = np.amax(list(individual_b_images.keys()))
    min_b = np.amin(list(individual_b_images.keys()))
    final_trace_file = os.path.join(tmpdir, "FINAL_TRACE.mif.gz")
    dwipy.mrtrixpy.mrcat([individual_b_images[min_b], individual_b_images[max_b]], final_trace_file)

    final_trace_file_with_grads = os.path.join(tmpdir, "FINAL_TRACE_GRADS.mif.gz")
    dwipy.mrtrixpy.mrconvert(
        final_trace_file,
        final_trace_file_with_grads,
        {
            "clear_property": "dw_scheme",
            "append_property": tuple([grad_scheme[min_b], grad_scheme[max_b]]),
        },
    )
    trace_file_in_output = os.path.join(out_folder, file_name_basis + "_TRACE.mif.gz")

    shutil.copy(final_trace_file_with_grads, trace_file_in_output)

    _get_adc_from_trace_dwi(trace_file_in_output, out_folder)


def _get_adc_from_dwi_with_bvecs_and_trace(image_file: str, grad_file: str, out_folder):
    tmpdir = dwipy.IO.misc._get_tmp_dir()

    file_name_basis = dwipy.IO.misc.get_file_base_name_without_extension(image_file)
    trace_file = os.path.join(tmpdir, "TRACE.mif.gz")

    grads = dwipy.IO.gradient_table.load_mrtrix_grads(grad_file)
    # non_zero_grads_index = np.squeeze(np.argwhere(grads[:, 3] > 0 ))
    # non_zero_grad_bvecs = grads[non_zero_grads_index, 0:3]
    total_bvec = np.sum(np.power(grads[:, 0:3], 2), axis=1)
    total_bvec_is_zero_index = np.squeeze(
        np.argwhere(np.bitwise_and(total_bvec == 0, grads[:, 3] > 0))
    )

    b0_volume = np.argwhere(grads[:, 3] == 0)

    dwi_b0_file = os.path.join(tmpdir, file_name_basis + "_B0.mif.gz")
    dwi_b1000_file = os.path.join(tmpdir, file_name_basis + "_B1000.mif.gz")

    dwipy.mrtrixpy.mrconvert(
        image_file,
        dwi_b0_file,
        {"coord": ["3", str(int(np.squeeze(b0_volume[0])))], "axes": "0,1,2"},
    )

    dwipy.mrtrixpy.mrconvert(
        image_file,
        dwi_b1000_file,
        {"coord": ["3", str(int(total_bvec_is_zero_index))], "axes": "0,1,2"},
    )

    dwi_single_trace_file = os.path.join(tmpdir, file_name_basis + "_TRACE.mif.gz")

    dwipy.mrtrixpy.mrcat([dwi_b0_file, dwi_b1000_file], dwi_single_trace_file)

    _get_adc_from_trace_dwi(dwi_single_trace_file, out_folder)
    shutil.copy(dwi_single_trace_file, os.path.join(out_folder, file_name_basis + "_TRACE.mif.gz"))


def _get_adc_from_dti(image_file: str, out_folder):
    tmpdir = dwipy.IO.misc._get_tmp_dir()

    file_name_basis = dwipy.IO.misc.get_file_base_name_without_extension(image_file)
    tensor_file = os.path.join(tmpdir, "DT.mif.gz")
    adc_file = os.path.join(tmpdir, "ADC.nii.gz")

    dwipy.mrtrixpy.dwi2tensor(image_file, tensor_file, {})
    dwipy.mrtrixpy.tensor2metric(tensor_file, {"adc": adc_file})

    adc_final_file = _normalize_adc(adc_file)

    shutil.copy(adc_final_file, os.path.join(out_folder, file_name_basis + "_ADC.nii.gz"))

    b0_extracted_file = os.path.join(tmpdir, "B0.nii.gz")

    dwipy.mrtrixpy.dwiextract(image_file, b0_extracted_file, {"bzero": None})

    shutil.copy(b0_extracted_file, os.path.join(out_folder, file_name_basis + "_B0.nii.gz"))


def _get_adc_from_multi_trace_dwi(image_file: str, grad_file: str, out_folder: str):
    tmpdir = dwipy.IO.misc._get_tmp_dir()

    bvals = dwipy.IO.gradient_table.load_mrtrix_bvals(grad_file)
    # Need to find the 0 bval and hopefully the 1000 bval

    # Before we checked for b=0 and b=1000, but cannot guarantee that those are actually
    # The values there are, sometime b=50 is low and b=800 is high
    # Perhaps add a check for this.
    if 0 in bvals:
        b0_volume = np.argwhere(bvals == 0)[0]
    else:
        b0_volume = np.argmin(bvals)
    if 1000 in bvals:
        b1000_volume = np.argwhere(bvals == 1000)[0]
    else:
        b1000_volume = np.argmax(bvals)

    # If they're the same we have a problem
    if b0_volume == b1000_volume:
        return

    else:
        file_name_basis = dwipy.IO.misc.get_file_base_name_without_extension(image_file)

        dwi_b0_file = os.path.join(tmpdir, file_name_basis + "_B0.mif.gz")
        dwi_b1000_file = os.path.join(tmpdir, file_name_basis + "_B1000.mif.gz")

        dwipy.mrtrixpy.mrconvert(
            image_file,
            dwi_b0_file,
            {"coord": ["3", str(int(np.squeeze(b0_volume)))], "axes": "0,1,2"},
        )

        dwipy.mrtrixpy.mrconvert(
            image_file,
            dwi_b1000_file,
            {"coord": ["3", str(int(np.squeeze(b1000_volume)))], "axes": "0,1,2"},
        )

        dwi_single_trace_file = os.path.join(tmpdir, file_name_basis + "_TRACE.mif.gz")

        dwipy.mrtrixpy.mrcat([dwi_b0_file, dwi_b1000_file], dwi_single_trace_file)

        _get_adc_from_trace_dwi(dwi_single_trace_file, out_folder)
        shutil.copy(
            dwi_single_trace_file, os.path.join(out_folder, file_name_basis + "_TRACE.mif.gz")
        )
