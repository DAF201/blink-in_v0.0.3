from tornado.web import RequestHandler
from libs.static_files_loader import load_static_files, load_config_file, content_type


def request_wrapper(func):
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

    def post(self, path):
        try:
            args = self.request.arguments
            files = self.request.files
            self.write_error(200)
            print(args)
            print(files.keys())
        except:
            pass


PATH_DIR = [(r"/", root), (r"/API(.*)", API)]
