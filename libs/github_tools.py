from github import Github, NamedUser, Repository, GithubException

try:
    from libs.file_tools import data_slice, data_hash
except:
    from file_tools import data_slice, data_hash

from json import dumps, loads


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
                # dumps will convert int key to str key
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
    def access(file_name=""):
        return github_tool.r.get_contents(file_name)

    @staticmethod
    def close():
        github_tool.g.close()
