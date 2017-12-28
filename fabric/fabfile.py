# -*- coding: utf-8 -*-
# @Time    : 17-8-17 下午2:33
# @Author  : Wang Chao
from fabric.api import env, sudo, put, run, local, get, settings
from fabric.contrib import project, console
from django.conf import settings


class Fabapi(object):
    def __init__(self, hostip):
        env.hosts = hostip
        env.user = settings.DEPLOYUSER
        env.abort_on_prompts = True
        env.key_filename = settings.DEPLOYKEY

    def locald(self, ld):
        return local(ld)

    def remoted(self, rd, sudoif=0):
        # if sudoif == 1:
        #     return sudo(rd, pty=False)
        # else:
        #     return run(rd)
        return run(rd,pty=False)

    def getfile(self, local_dest, remote_dest):
        get(remote_dest, local_dest)

    def putfile(self, local_dest, remote_dest):
        put(local_dest, remote_dest, mode=0o664)

    def isexists(self, rootdir):
        res = int(run(" [ -e {0} ] && echo 1 || echo 0".format(rootdir)))
        return res

    def rsyncd(self, local_dest, remote_dest):
        local(
            "rsync --progress --delete -avzq --rsh=\"sshpass -p {ssh_pass} ssh -p 22 \" "
            "--exclude='assets/sass' --exclude='assets/js/app' "
            "--exclude='scripts' --exclude='node-modules' --exclude='WEB-INF' "
            "{local_dest}/ {ssh_user}@{ssh_host}:{remote_dest}".format(
                local_dest=local_dest,
                remote_dest=remote_dest,
                ssh_user=env.user,
                ssh_host=env.hosts,
                ssh_pass=env.password))
