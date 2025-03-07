from github import Github, NamedUser, Repository, GithubException
from libs.file_tools import data_slice, data_hash, virtual_file
from json import dumps, loads
from requests import get
from PIL import Image


class github_tool:
    g: Github
    u: NamedUser
    r: Repository

    def __init__(self, path, repo):
        with open(path, "r") as f:
            github_tool.g = Github(f.read())
        github_tool.u = self.g.get_user()
        github_tool.r = github_tool.u.get_repo(repo)

    # upload file by slice large file to small files, and create a json contains file info
    # maybe need to make files can cross repos in the future, but for now everything is still in one repo
    @staticmethod
    def upload(file_data, file_name=""):
        # 25 MB each
        file_data = data_slice(file_data, 1024 * 1024 * 25)
        file_hash = data_hash(file_data)
        inf = {"file_name": file_name, "file_content": file_hash}

        # check if file already exist
        try:
            inf = github_tool.r.get_contents(file_name).decoded_content.decode("utf-8")
            return loads(inf)
        except GithubException as e:
            if e.status == 404:
                github_tool.r.create_file(file_name, "", dumps(inf))
                for x in range(len(file_data)):
                    try:
                        github_tool.r.create_file(file_hash[x], "", file_data[x])
                    except:
                        continue
        return inf

    @staticmethod
    def download(file_name):
        # download file from github, might be multiple files cause the original file might be larger then 25mb

        # check if descriptor file exist on github
        inf: str
        try:
            inf = loads(
                github_tool.r.get_contents(file_name).decoded_content.decode("utf-8")
            )
        except GithubException as e:
            if e.status == 404:
                raise EOFError
            else:
                print(e)

        file_contents = inf["file_content"]
        file_contents = [file_contents[str(x)] for x in range(len(file_contents))]
        for file in file_contents:
            # get the download urls
            try:
                file_contents.append(github_tool.r.get_contents(file).download_url)

            # pass stupid assertion error: none, it doesnt even tells me what is wrong
            except:
                continue
        file_contents = file_contents[int(len(file_contents) / 2) :]
        # seems like python does now like random bytes and serialized bytes in one list still
        file_data = []
        # get content of files, still encoded images likely
        for url in file_contents:
            file_data.append(get(url).content)
        return file_data

    @staticmethod
    def clean_up(file_name):

        inf = github_tool.r.get_contents(file_name).decoded_content.decode("utf-8")
        inf = loads(inf)
        return github_tool.__clean_up__(inf, len(inf["file_content"]))

    # clear up failed file
    @staticmethod
    def __clean_up__(file_info, chunk_index):
        success_count = 0
        for x in range(chunk_index):
            try:
                # dumps will convert int key to str
                if github_tool.__del__(file_info["file_content"][x]):
                    success_count += 1
                else:
                    continue
            except:
                if github_tool.__del__(file_info["file_content"][str(x)]):
                    success_count += 1
                else:
                    continue
        github_tool.__del__(file_info["file_name"])
        return success_count == chunk_index

    @staticmethod
    def __del__(file_name):
        try:
            targert_file = github_tool.r.get_contents(file_name)
            github_tool.r.delete_file(targert_file.path, "", targert_file.sha)
        except Exception as e:
            return False
        return True

    @staticmethod
    def close():
        github_tool.g.close()
