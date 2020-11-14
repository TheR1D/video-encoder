from rest_framework.exceptions import ValidationError

from tqdm import tqdm
from tqdm.utils import disp_len, _unicode


ALLOWED_MEDIA_CONTAINERS = ("mov", "mp4", "m4a", "m4v", "mpg", "mxf", "avi", "mkv", "mov", "mp3", "aac")


def validate_file_name(value):
    file_name = value.name
    sliced_value = file_name.split(".")
    if len(sliced_value) != 2:
        raise ValidationError("Invalid file name. Extension required.", "INVALID_FILE_NAME")
    file_extension = sliced_value[1]
    if file_extension not in ALLOWED_MEDIA_CONTAINERS:
        raise ValidationError(f"Invalid media container, {file_extension} not supported", "INVALID_MEDIA_CONTAINER")
    return value


def validate_file_size(value):
    filesize = value.size
    if filesize > 10485760 * 200:
        raise ValidationError("The maximum file size that can be uploaded is 2GB.")
    return value


class CustomTqdm(tqdm):
    @staticmethod
    def status_printer(file):
        fp = file
        fp_flush = getattr(fp, "flush", lambda: None)  # pragma: no cover

        def fp_write(s):
            fp.write(_unicode(s))
            fp_flush()

        last_len = [0]

        def print_status(s):
            len_s = disp_len(s)
            # Adding new line after each iteration.
            fp_write("\n" + s + (" " * max(last_len[0] - len_s, 0)))
            last_len[0] = len_s

        return print_status
