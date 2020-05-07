import os
import glob
from listen import segment_muscle_absolute
from common.utils import *
import shutil
from common.exceptions import TaskFailedException


def __validate_input_files_and_get_fullpath(files, element_input_dir):
    if len(files) == 0:
        log_error(f"No files found in {element_input_dir} - skipping")
        return "", False

    if files[0].endswith(".nii.gz"):
        abs_source_file = os.path.join(element_input_dir, files[0])
        return abs_source_file, True

    elif files[0].endswith(".dcm"):
        log_error(f"Not able to compute visceral fat measurements for dicom files (only nifti .nii.gz) - skipping")
        return "", False
    else:
        log_error(f"Unrecognised input file type inside {element_input_dir} - skipping")
        return "", False


def  __compute_task(task_method, source_file):
    try:
        param_dict, success = task_method(source_file)
    except Exception as e:
        raise TaskFailedException(str(e))

    if not success:
        raise TaskFailedException()

    return param_dict


def start_batch_job():
    setup_logging()

    batch_folders = [f for f in glob.glob(os.path.join('/', os.environ['WORKFLOW_DIR'], os.environ['BATCH_NAME'], '*'))]

    for batch_element_dir in batch_folders:

        element_input_dir = os.path.join(batch_element_dir, os.environ['OPERATOR_IN_DIR'])
        element_output_dir = os.path.join(batch_element_dir, os.environ['OPERATOR_OUT_DIR'])
        os.makedirs(element_output_dir, exist_ok=True)

        files = os.listdir(element_input_dir)

        abs_source_file, valid = __validate_input_files_and_get_fullpath(files, element_input_dir)

        if not valid:
            continue

        try:
            param_dict = __compute_task(segment_muscle_absolute, source_file=abs_source_file)
        except TaskFailedException as e:
            log_error(f"Task failed with exception {e}")
            log_error("Skipping")
            continue

        fat_report_path = param_dict["segmentation"]
        data_share = os.environ["DATA_SHARE_PATH"]
        full_fat_report_path = os.path.join(data_share, fat_report_path)

        element_output_name = os.path.join(element_output_dir, "muscle_segmentation.nii.gz")
        shutil.copyfile(full_fat_report_path, element_output_name)


if __name__ == "__main__":
    start_batch_job()
