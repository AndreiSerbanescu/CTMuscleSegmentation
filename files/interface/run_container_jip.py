import os
from common.utils import *
import shutil
from common_jip.batch_job import *
from listen import segment_muscle_absolute

def handle_output(param_dict, element_output_dir):

    fat_report_path = param_dict["segmentation"]
    data_share = os.environ["DATA_SHARE_PATH"]
    full_fat_report_path = os.path.join(data_share, fat_report_path)

    element_output_name = os.path.join(element_output_dir, "muscle_segmentation.nii.gz")
    shutil.copyfile(full_fat_report_path, element_output_name)

if __name__ == "__main__":
    start_batch_job(handle_output_callback=handle_output, task_method=segment_muscle_absolute)
