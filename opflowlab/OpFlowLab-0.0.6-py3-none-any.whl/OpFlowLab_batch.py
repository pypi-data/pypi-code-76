import glob
import os

import OpFlowLab

main_folder = r"K:\Jupyter\synthetic_data\piv5"
folder_list = glob.glob(os.path.join(main_folder, "*movement*"))

for folder in folder_list:
    print(folder)
    if os.path.isdir(folder):
        image_filepath = os.path.join(folder, "stack.tif")

        opFlow = OpFlowLab.OpFlowLab(folder, image_filepath,
                               os.path.join(folder, "NvidiaOF_Slow"), os.path.join(folder, "Reverse", "NvidiaOF_Slow"),
                               os.path.join(folder, "labels"),
                               velocity_type="dense", velocity_ext_type="*.bin", image_ext_type="*.tif",
                               velocity_dtype="float16", kernel_size=5)

        opFlow.flowMatch_function(output_folder="matched",
                                  pairwise_threshold_distance=10,
                                  min_object_size=100, max_object_size=1500,
                                  )
