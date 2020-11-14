import os
import re
import shlex
import subprocess

import ffpb

from django.conf import settings

from app.utils.misc import CustomTqdm
from app.models import MediaFile


def convert_video(guid, output_format):
    output_path = os.path.join(settings.MEDIA_ROOT, "converted", guid)
    input_path = os.path.join(settings.MEDIA_ROOT, "uploads", guid)
    output_file_path = f"{output_path}.{output_format}"
    command_string = f"-i {input_path} {output_file_path}"
    command = shlex.split(command_string)
    output_log = output_path + ".log"
    log_file = open(output_log, "w+", encoding="utf-8")  # File will be closed in tqdm module.
    exit_code = ffpb.main(command, log_file, "utf-8", CustomTqdm)
    media_file = MediaFile.objects.get(guid=guid)
    # TODO: Investigate all exit codes from shell.
    if exit_code is None or exit_code == 0:
        media_file.output_file = f"converted/{guid}.{output_format}"
        media_file.status = "DONE"
    else:
        media_file.status = "FAILED"
    media_file.save(update_fields=("output_file", "status"))


def get_processing_progress(guid):
    file_path = os.path.join(settings.MEDIA_ROOT, "converted", guid + ".log")
    command_string = f"tail -1 {file_path}"
    if os.path.exists(file_path):
        last_log_line = subprocess.check_output(shlex.split(command_string), encoding="utf-8")
        print(last_log_line)
        regex_pattern = r"\d{1,3}%"
        matching_string = re.findall(regex_pattern, last_log_line)[0]
        return matching_string
    return 0
