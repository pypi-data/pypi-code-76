import os
import tempfile
import shutil
from typing import Tuple
import glob

import dwipy.constants
import dwipy.IO.converters
import dwipy.IO.misc
import dwipy.mrtrixpy
import dwipy.qa
import dwipy.rescuer
import dwipy.IO.gradient_table
import dwipy.metrics.adc


class Pipeline:
    def __init__(self) -> None:
        self.make_adc = True

    def process(self, dwi_folder: str, out_folder: str) -> bool:
        """
        Process a DWI dicom folder.

        Convert DICOM to nifti, extracts the b-values, pre-process and calculates the ADC

        Args:
            dwi_folder (str): Folder with the DICOM files of the DWI
            out_folder (str): Folder in which to put outputs

        Returns:
            bool: Whether folder was successfully processed.
        """

        tmp_folder = tempfile.mkdtemp()
        dicom_files = glob.glob(os.path.join(dwi_folder, "*.dcm"))
        for i_file in dicom_files:
            shutil.copy(
                i_file, os.path.join(tmp_folder, os.path.basename(os.path.normpath(i_file)))
            )
        dwi_folder = tmp_folder
        out_file = os.path.join(out_folder, os.path.normpath(os.path.basename("DWI.mif.gz")))

        image_file, grad_file, conversion_successful = self.convert_dicom_to_image(
            dwi_folder,
            out_file,
        )

        if not conversion_successful:
            bval_status = dwipy.qa.check_grad_file_status(grad_file)
            fixed_image_file, fixed_grad_file, conversion_successful = dwipy.rescuer.rescue_dwi(
                dwi_folder, bval_status
            )

            if (
                fixed_image_file is not None
                and os.path.exists(fixed_image_file)
                and fixed_grad_file is not None
                and os.path.exists(fixed_grad_file)
            ):
                if os.path.exists(image_file):
                    os.remove(image_file)
                if os.path.exists(grad_file):
                    os.remove(grad_file)

                shutil.copy(fixed_image_file, image_file)
                shutil.copy(fixed_grad_file, grad_file)

                image_file = fixed_image_file
                grad_file = fixed_grad_file

        print(conversion_successful)
        bval_status = dwipy.qa.check_grad_file_status(grad_file)
        if conversion_successful:
            adc_success = dwipy.metrics.adc.get_adc_from_image(image_file, grad_file, out_folder)

        return conversion_successful and adc_success, image_file

    def convert_dicom_to_image(self, dicom_folder: str, out_file: str) -> Tuple[str, str, bool]:
        # First a naieve approach where the folder is converted using mrtrix
        # Perhaps this will already work
        image_file, grad_file = dwipy.IO.converters.dcm2mif(dicom_folder, out_file)

        grad_status = dwipy.qa.check_grad_file_status(grad_file)

        return image_file, grad_file, grad_status is dwipy.constants.GRADSTATUS.VALID_GRADS

    def process_patient_folder(self, patient_folder: str):
        output_folder = os.path.join(patient_folder, "OUTPUT")
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)

        scan_folders = os.listdir(patient_folder)
        scan_folders = [
            os.path.join(patient_folder, i_scan_folder) for i_scan_folder in scan_folders
        ]

        folder_status = []
        calculated_adc = False
        for i_folder in scan_folders:
            if os.path.exists(output_folder):
                shutil.rmtree(output_folder)
            os.makedirs(output_folder)
            calculated_adc, bval_status = self.process(i_folder, output_folder)
            folder_status.append(bval_status)
            if calculated_adc:
                break

        if not calculated_adc:
            # Perhaps we have folders that are separate b-values
            # So we need to combine them
            individual_folders = []
            if os.path.exists(output_folder):
                shutil.rmtree(output_folder)
            os.makedirs(output_folder)
            for i_folder, i_status in zip(scan_folders, folder_status):
                if (
                    i_status is dwipy.constants.GRADSTATUS.ONE_BVAL_SINGLE_IMAGE
                    or i_status is dwipy.constants.GRADSTATUS.ONE_BVAL
                ):
                    individual_folders.append(i_folder)

            individual_image_files = {}
            for i_i_individual_folder, i_individual_folder in enumerate(individual_folders):
                n_slices = len(glob.glob(os.path.join(i_individual_folder, "*")))
                img_file, _, _ = self.convert_dicom_to_image(
                    i_individual_folder,
                    os.path.join(output_folder, "DWI_B_INDIVIDUAL_" + str(i_i_individual_folder)),
                )
                if n_slices in individual_image_files:
                    individual_image_files[n_slices].append(img_file)
                else:
                    individual_image_files[n_slices] = [img_file]
            for i_individiual_image_files in individual_image_files.values():
                if len(i_individiual_image_files) >= 2:
                    full_image_file = os.path.join(output_folder, "DWI.mif.gz")
                    full_grad_file = os.path.join(output_folder, "DWI.grads")
                    dwipy.mrtrixpy.mrcat(i_individiual_image_files, full_image_file)
                    dwipy.mrtrixpy.mrinfo(full_image_file, {"export_grad_mrtrix": full_grad_file})

                    if os.path.exists(full_image_file) and os.path.exists(full_grad_file):
                        calculated_adc = dwipy.metrics.adc.get_adc_from_image(
                            full_image_file, full_grad_file, output_folder
                        )
                    if calculated_adc:
                        break
        return calculated_adc
