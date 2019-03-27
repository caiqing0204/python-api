# -*- coding: utf-8 -*-
# @Time    : 17-12-14 下午1:23
# @Author  : Wang Chao
# warning：only tested for python2.7

from subprocess import Popen, PIPE, CalledProcessError


def check_call(*args, **kargs):
    cmd = kargs.get("args") or args[0]

    process = Popen(*args, stdout=PIPE, stderr=PIPE, **kargs)
    stdout, stderr = process.communicate()
    stdout = stdout.decode("utf-8")
    stderr = stderr.decode("utf-8")
    rc = process.poll()
    if rc:
        raise CalledProcessError(rc, cmd, stdout + "\n" + stderr)
    data = {
        'stdout': stdout,
        'stderr': stderr,
        'rc': rc
    }
    return data


class Git(object):
    def __init__(self, dest, url, version=None):
        self.dest = dest
        self.url = url
        self.version = version

    def local_branch(self):
        shell = "cd {0} && git branch".format(self.dest)
        stdout = check_call(shell, shell=True)
        stdout = stdout.strip().split("\n")
        stdout = [s.strip("* ") for s in stdout]
        return stdout

    def current_branch(self):
        shell = "cd {0} && git branch".format(self.dest)
        stdout = check_call(shell, shell=True)
        stdout = stdout.strip().split("\n")
        for i in stdout:
            if i.startswith('* '):
                res = i.strip('* ')
                return res

    def pull(self):

        shell = " cd {0} && git pull -q ".format(self.dest)
        check_call(shell, shell=True)
        return

    def reset(self):

        shell = "cd {0} && git reset --hard".format(self.dest)
        check_call(shell, shell=True)
        return

    def commit(self):
        shell = "cd {0} && git commit -am 'update version to {1}'".format(self.dest, self.version)
        check_call(shell, shell=True)
        return

    def push(self):
        shell = "cd {0} && git push origin develop:develop ".format(self.dest)
        check_call(shell, shell=True)
        return

    def remote_branch(self):
        shell = "cd {0} && git fetch -q -a && git branch -r".format(self.dest)
        stdout = check_call(shell, shell=True)
        stdout = stdout.strip().split("\n")
        stdout = [s.strip(" ").split("/", 1)[1] for s in stdout if "->" not in
                  s]
        return stdout

    def tag(self):
        shell = "cd {0} && git fetch -q -a && git tag".format(self.dest)
        stdout = check_call(shell, shell=True)
        if stdout:
            return stdout.strip().split("\n")
        else:
            return []

    def log(self):
        shell = ("cd {0} && git log -20 --pretty=\"%h  %an  %s\""
                 ).format(self.dest)
        stdout = check_call(shell, shell=True)
        stdout = stdout.strip().split("\n")
        stdout = [s.split("  ", 2) for s in stdout]
        return [{"abbreviated_commit": s[0],
                 "author_name": s[1],
                 "subject": s[2]}
                for s in stdout]

    def clone(self):
        shell = ("mkdir -p {0} && cd {0} && git clone -q {1} ."
                 ).format(self.dest, self.url)
        data = check_call(shell, shell=True)
        rc = data['rc']

        # destination path '.' already exists and is not an empty directory.
        if rc == 128:
            shell = ("cd {0} && git clean -xdfq && git reset -q --hard && git "
                     "remote update && git checkout -q master && git remote "
                     "prune origin && git pull -q --all --tags && git branch "
                     "| grep -v \\* | xargs git branch -D").format(self.dest)
            rc = check_call(shell, shell=True)
            # branch name required
            if rc == 123:
                return
        if rc != 0:
            raise Exception("克隆失败")

    def checkout_tag(self, tag):
        check_call(
            "cd {0} && git checkout -q {1}".format(self.dest, tag),
            shell=True)

    def checkout_branch(self, branch, version=""):

        if branch in self.local_branch():
            check_call("cd {0} && git checkout -q {1}  ".format(self.dest, branch, version), shell=True)
        else:
            check_call("cd {0} && git checkout -q -b {1} -t origin/{1} ".format(self.dest, branch, version),
                       shell=True)
