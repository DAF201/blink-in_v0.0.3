import libs.static_files_loader as load_static_files
import libs.database as db
import libs.API as API
from tornado.web import Application
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop


def main():
    application = Application(API.PATH_DIR)
    http_server = HTTPServer(
        application,
        ssl_options={
            "certfile": load_static_files.load_config_file()["ssl"]["ssl_full_chain"],
            "keyfile": load_static_files.load_config_file()["ssl"]["ssl_private_key"],
        },
    )
    http_server.listen(load_static_files.load_config_file()["network"]["port"])
    IOLoop.instance().start()


# print(load_static_files.load_static_files())
if __name__ == "__main__":
    main()
