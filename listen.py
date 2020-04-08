import subprocess as sb
import os
from http.server import *
from urllib.parse import urlparse
from urllib.parse import parse_qs
import logging
import sys
import SimpleITK as sitk
import numpy as np
import json
import time

class CommandRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text")
        self.end_headers()

        self.__requested_method = {
            "/ct_segment_muscle": segment_muscle
        }


    def do_GET(self):
        self._set_headers()
        self.__handle_request()

    def __handle_request(self):
        parsed_url = urlparse(self.path)
        parsed_params = parse_qs(parsed_url.query)

        log_debug("Got request with url {} and params {}".format(parsed_url.path, parsed_params))

        if parsed_url.path not in self.__requested_method:
            log_debug("unkown request {} received".format(self.path))
            return


        print("running CT Muscle Segmenter")
        result_dict = self.__requested_method[parsed_url.path](parsed_params)
        print("result", result_dict)

        print("sending over", result_dict)
        self.wfile.write(json.dumps(result_dict).encode())



def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)

    mark_yourself_ready()
    httpd.serve_forever()


def mark_yourself_ready():
    hostname = os.environ['HOSTNAME']
    data_share_path = os.environ['DATA_SHARE_PATH']
    cmd = "touch {}/{}_ready.txt".format(data_share_path, hostname)

    logging.info("Marking as ready")
    sb.call([cmd], shell=True)


# PRE: file is .nii.gz
def segment_muscle(param_dict):
    print("### converter got parameters {}".format(param_dict))

    source_file = param_dict["source_file"][0]
    model_name = "MuscleNC"

    segment_command = "python3 /app/Inference.py --single_file {} --result_root {} --model {}"\
                         .format(source_file, "/tmp", model_name)
    sb.call([segment_command], shell=True)

    # remove from the end of source file ".nii.gz"
    volume_name = os.path.split(source_file)[1]
    source_file_name = volume_name[:len(volume_name) - 7]

    tmp_out_file = os.path.join("/tmp", source_file_name  + "_MuscleNC.nii.gz")
    data_share   = os.environ["DATA_SHARE_PATH"]
    output_name  = "ct-muscle-segment-" + str(time.time()) + ".nii.gz"

    move_command = "mv {} {}/{}".format(tmp_out_file, data_share, output_name)
    sb.call([move_command], shell=True)

    result_dict = {"segmentation": output_name}
    return result_dict

def setup_logging():
    file_handler = logging.FileHandler("log.log")
    stream_handler = logging.StreamHandler(sys.stdout)

    file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    stream_handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))

    logging.basicConfig(
        level=logging.DEBUG, # TODO level=get_logging_level(),
        # format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            file_handler,
            stream_handler
        ]
    )

def log_info(msg):
    logging.info(msg)

def log_debug(msg):
    logging.debug(msg)

def log_warning(msg):
    logging.warning(msg)

def log_critical(msg):
    logging.critical(msg)


if __name__ == '__main__':
    setup_logging()
    log_info("Started listening")
    run(handler_class=CommandRequestHandler)
