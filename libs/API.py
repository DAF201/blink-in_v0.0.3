from libs.static_files_loader import load_static_files, load_config_file, content_type
from libs.file_tools import virtual_file
from libs.github_tools import github_tool
from libs.coding import Data
from libs.image_encoding import data_decoding, data_encoding
from json import dumps, loads
from tornado.web import RequestHandler
from PIL import Image
from zipfile import ZipFile, ZIP_DEFLATED

GITHUB = github_tool(r"C:\Users\daf201\Desktop\token.txt", "blink_in_inventory")


def request_wrapper(func):
    # havent decide if I need this
    def wrapper(*args, **kwargs):
        # TODO: before request handle
        func(*args, **kwargs)
        # TODO: after request handle

    return wrapper


class root(RequestHandler):
    def get(self, *keys):
        if "mobile" in self.request.headers.get("User-Agent").lower():
            self.write(load_static_files()["html"]["mobile_editor.html"])
        else:
            self.write(load_static_files()["html"]["desktop_editor.html"])

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

    # only handle upload/download one at a time
    # if some files are uploaded, download request will be ignored
    @request_wrapper
    def post(self, path):
        self.set_header("Content-Type", content_type["json"])
        # editor contents
        editor_contents = self.request.arguments["editor_data"][0].decode("utf-8")
        if editor_contents == "{}":
            # uploaded file data
            files = self.request.files
            # returning response
            response = {}
            for key in files:
                file_name = files[key][0]["filename"]
                file_content = files[key][0]["body"]
                # encode data to str
                file_content = Data.encode(file_content)
                # encode data to image
                file_content = data_encoding(file_content.encode("utf-8"))
                # save image data to memory
                vf = virtual_file()
                file_content.save(vf, "WEBP", lossless=True)
                # read image, try to upload to github
                file_content = vf.getvalue()
                response[key] = GITHUB.upload(file_content, file_name)
            self.write(dumps(response))
        else:
            try:
                editor_contents = loads(editor_contents)
            except:
                self.write({"error": "syntax error"})
                return
            target_files = list(editor_contents.values())
            vz = virtual_file()
            with ZipFile(vz, "w", ZIP_DEFLATED) as zip:
                for file_name in target_files:
                    response = b"".join(GITHUB.download(file_name))
                    vf = virtual_file()
                    vf.write(response)
                    data = data_decoding(Image.open(vf)).decode("utf-8")
                    zip.writestr(file_name, Data.decode(data), ZIP_DEFLATED)
            vz.seek(0)
            self.set_header("Content-Type", content_type["zip"])
            self.set_header(
                "Content-Disposition", 'attachment; filename="blink-in.zip"'
            )
            self.write(vz.read())


PATH_DIR = [(r"/", root), (r"/API(.*)", API)]
