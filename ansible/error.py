# -*- coding: utf-8 -*-
# @Time    : 17-12-27 下午6:08
# @Author  : Wang Chao

__author__ = 'wang chao'


class AnsibleError(Exception):
    MAPS = {
        10000: "income parameters error",
        10001: "project not exists.",
        10002: "host not exists.",
        10003: "user not exists.",
        10004: "deploy permission denied.",
        10005: "Incomplete parameter",
        10006: "Jenkins run error",
        10007: "LDAP auth error",
        10008: "wrong envname",
        10009: "dest_war_path is not exsit on the target host",
        # 远端shell部分
        11000: "pre deploy shell called exception",
        11001: "post deploy shell called exception",
        11002: "restart shell called exception",
        11003: "rsync called exception",
        # 本地shell部分
        12000: "git repo clone exception",
        # 用户部分
        13000: "username or password incorrect",
        13001: "user not exists",
        }

    """
    # use maps
    def __init__(self, rc, msg=None):
        self.rc = rc
        if msg is None:
            self.msg = self.MAPS[rc]
        else:
            self.msg = msg

    def __repr__(self):
        return "%s: %s" % (self.rc, self.msg)
    """

    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return self.msg