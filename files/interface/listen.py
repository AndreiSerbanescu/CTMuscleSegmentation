import subprocess as sb
import os
import time
from common.utils import *
from common import listener_server
from common import utils
import shutil



# PRE: file is .nii.gz
def segment_muscle(param_dict):
    print("### muscle segmenter got parameters {}".format(param_dict))

    rel_source_file = param_dict["source_file"][0]
    # remove trailing / at the beggining of name
    # otherwise os.path.join has unwanted behaviour for base dirs
    # i.e. join(/app/data_share, /app/wrongpath) = /app/wrongpath
    rel_source_file = rel_source_file.lstrip('/')

    data_share = os.environ["DATA_SHARE_PATH"]
    source_file = os.path.join(data_share, rel_source_file)

    return segment_muscle_absolute(source_file)

def __create_tmp_out_dir():

    unique_id = utils.get_unique_id()
    tmp_out_file = os.path.join("/tmp", f"output-{unique_id}")

    if os.path.exists(tmp_out_file):
        log_debug(f"Temporary output file existed, deleting {tmp_out_file}")
        shutil.rmtree(tmp_out_file)

    os.makedirs(tmp_out_file)

    return tmp_out_file



def segment_muscle_absolute(source_file):
    model_name = "MuscleNC"

    tmp_out_dir = __create_tmp_out_dir()

    segment_command = "python3 /app/Inference.py --single_file {} --result_root {} --model {}" \
        .format(source_file, tmp_out_dir, model_name)
    exit_call_segment = sb.call([segment_command], shell=True)

    if exit_call_segment == 1:
        return {}, False

    # remove from the end of source file ".nii.gz"
    volume_name = os.path.split(source_file)[1]
    source_file_name = volume_name[:len(volume_name) - 7]

    tmp_out_file = os.path.join(tmp_out_dir, source_file_name + "_MuscleNC.nii.gz")
    data_share = os.environ["DATA_SHARE_PATH"]
    output_name = "ct-muscle-segment-" + str(time.time()) + ".nii.gz"

    move_command = "mv {} {}/{}".format(tmp_out_file, data_share, output_name)
    exit_call_move = sb.call([move_command], shell=True)

    if exit_call_move == 1:
        return {}, False

    result_dict = {"segmentation": output_name}
    return result_dict, True

if __name__ == "__main__":

    setup_logging()
    log_info("Started listening")

    served_requests = {
        "/ct_segment_muscle": segment_muscle
    }

    listener_server.start_listening(served_requests, multithreaded=True, mark_as_ready_callback=mark_yourself_ready)