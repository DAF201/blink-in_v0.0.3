from json import load
from os.path import basename, isfile, join
from os import listdir

content_type = {
    "txt": "text/plain",
    "html": "text/html",
    "css": "text/css",
    "js": "text/javascript",
    "json": "application/json",
    "xml": "application/xml",
    "svg": "image/svg+xml",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "gif": "image/gif",
    "webp": "image/webp",
    "bmp": "image/bmp",
    "mp3": "audio/mpeg",
    "ogg": "audio/ogg",
    "wav": "audio/wav",
    "mp4": "video/mp4",
    "ogg": "video/ogg",
    "webm": "video/webm",
    "woff": "font/woff",
    "woff2": "font/woff2",
    "otf": "font/otf",
    "ttf": "font/ttf",
    "pdf": "application/pdf",
    "zip": "application/zip",
    "rar": "application/x-rar-compressed",
    "tar": "application/x-tar",
    "doc": "application/msword",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "xls": "application/vnd.ms-excel",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "ppt": "application/vnd.ms-powerpoint",
    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "swf": "application/x-shockwave-flash",
    "octet": "application/octet-stream",
    "json": "application/json",
    "form": "multipart/form-data",
    "alternative": "multipart/alternative",
    "mixed": "multipart/mixed",
    "ico": "image/x-icon",
}


def load_config_file():
    if not hasattr(load_config_file, "data_loaded"):
        load_config_file.data_loaded = False
        load_config_file.config = {}

    def load_data():
        with open("config.json") as js:
            load_config_file.config = load(js)
            load_config_file.data_loaded = False
        with open(load_config_file.config["database"]["path"]) as database_config:
            while True:
                line = database_config.readline()
                if not line:
                    break
                split_index = line.find("=")
                load_config_file.config["database"][line[:split_index]] = line[
                    split_index + 1 : -1
                ]
        with open(load_config_file.config["database"]["token_path"]) as github_token_path:
                load_config_file.config["database"]["github_token"] = github_token_path.read()
        return load_config_file.config

    return load_config_file.config if load_config_file.data_loaded else load_data()


def load_static_files():
    if not hasattr(load_static_files, "data_loaded"):
        load_static_files.data_loaded = False
        load_static_files.container = {}

    def load_data():
        for dir in load_config_file()["static_files"].keys():
            load_static_files.container[dir] = {}
            for file_basename in [
                basename(file)
                for file in listdir(load_config_file()["static_files"][dir])
                if isfile(join(load_config_file()["static_files"][dir], file))
            ]:
                with open(
                    "".join((load_config_file()["static_files"][dir], file_basename)),
                    "rb",
                ) as file_stream:
                    load_static_files.container[dir][file_basename] = file_stream.read()
        load_static_files.data_loaded = True
        return load_static_files.container

    return load_static_files.container if load_static_files.data_loaded else load_data()
