import os
from mimetypes import MimeTypes

def get_file_content_type(filename):
    mime = MimeTypes()
    content_type = mime.guess_type(filename)[0]
    if content_type:
        if content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            return 'binary/octet-stream'
        return content_type
    return 'binary/octet-stream'
