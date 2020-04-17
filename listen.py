import subprocess as sb
import os
import time
from common.utils import *
from common import listener_server



# PRE: file is .nii.gz
def segment_muscle(param_dict):
    print("### muscle segmenter got parameters {}".format(param_dict))

    rel_source_file = param_dict["source_file"][0]

    data_share = os.environ["DATA_SHARE_PATH"]
    source_file = os.path.join(data_share, rel_source_file)

    model_name = "MuscleNC"

    segment_command = "python3 /app/Inference.py --single_file {} --result_root {} --model {}"\
                         .format(source_file, "/tmp", model_name)
    exit_call_segment = sb.call([segment_command], shell=True)

    if exit_call_segment == 1:
        return {}, False

    # remove from the end of source file ".nii.gz"
    volume_name = os.path.split(source_file)[1]
    source_file_name = volume_name[:len(volume_name) - 7]

    tmp_out_file = os.path.join("/tmp", source_file_name  + "_MuscleNC.nii.gz")
    data_share   = os.environ["DATA_SHARE_PATH"]
    output_name  = "ct-muscle-segment-" + str(time.time()) + ".nii.gz"

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