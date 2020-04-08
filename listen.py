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


def convert(param_dict):
    # TODO implement
    print("### converter got parameters".format(param_dict))

    result_dict = {}
    return result_dict

def segment_muscle(param_dict):
    print("### converter got parameters".format(param_dict))

    # TODO check file is .nii.gz not .dcm
    # TODO implement
    result_dict = {}
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
