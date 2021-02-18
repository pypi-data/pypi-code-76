from typing import Tuple
import numpy
from dwipy import mrtrixpy
import os


def dcm2nii(
    dicom_dir: str,
    out_file: str,
    export_bvecs: bool = True,
):
    out_nifti_file = out_file + ".nii.gz"

    if export_bvecs:
        bval_file = out_file + ".bval"
        bvec_file = out_file + ".bvec"
        options = {"export_grad_fsl": [bvec_file, bval_file]}
    else:
        options = None
        bval_file = None
        bvec_file = None
    mrtrixpy.mrconvert(dicom_dir, out_nifti_file, options)

    return out_nifti_file, bval_file, bvec_file


def dcm2mif(dicom_dir: str, out_file: str, compress: bool = True) -> Tuple[str, str]:
    if compress:
        out_mif_file = out_file + ".mif.gz"
    else:
        out_mif_file = out_file + ".mif"
    grad_file = out_file + ".grads"
    if not os.path.exists(os.path.dirname(os.path.normpath(out_mif_file))):
        os.makedirs(os.path.dirname(os.path.normpath(out_mif_file)))
    print(out_mif_file)
    mrtrixpy.mrconvert(dicom_dir, out_mif_file, {"export_grad_mrtrix": grad_file})

    return out_mif_file, grad_file
