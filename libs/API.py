from tornado.web import RequestHandler
from libs.static_files_loader import load_static_files, load_config_file, content_type
from libs.file_tools import test_storage


def request_wrapper(func):
    # havent decide if I need this
    def wrapper(*args, **kwargs):
        # TODO: before request handle
        func(*args, **kwargs)
        # TODO: after request handle

    return wrapper


class root(RequestHandler):
    def get(self, *keys):
        self.write(load_static_files()["html"]["editor.html"])

    def post(self, *keys):
        return self.send_error(500)


class API(RequestHandler):

    @request_wrapper
    def get(self, path):
        if path in ("", "/"):
            # havent decided yet
            pass
        else:
            # requesting file
            file_name = path[1:]
            file_extension = file_name.split(".")[1]
            try:
                self.set_header("Content-Type", content_type[file_extension])
                self.set_header(
                    "Content-Disposition", f"attachment; filename={file_name}"
                )
                self.write(
                    load_static_files()[
                        load_config_file()["extension"][file_extension]
                    ][file_name]
                )
                self.flush()
            except:
                self.write_error(404)

    @request_wrapper
    def post(self, path):

        args = self.request.arguments
        files = self.request.files
        for key in files:
            temp_file = files[key][0]
            test_storage(temp_file["filename"], temp_file["body"])



        self.write_error(200)


PATH_DIR = [(r"/", root), (r"/API(.*)", API)]
