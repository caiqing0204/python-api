#!/usr/bin/env python
# 1、python3.6和ansible2.7.8 api环境
# 2、封装ansible2.7.8 api
# by wangchao

import os
import json
import shutil
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
import ansible.constants as C


class ResultCallback(CallbackBase):
    """
    重构输出
    """
    def __init__(self, *args, **kwargs):
        super(ResultCallback, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_ok(self, result, **kwargs):
    	"""成功"""
        self.host_ok[result._host.name] = result._result["stdout"]

    def v2_runner_on_unreachable(self, result, **kwargs):
        """不可达"""
        self.host_unreachable[result._host.name] = result._result["msg"]

    def v2_runner_on_failed(self, result, ignore_errors=False, **kwargs):
        """失败"""
        self.host_failed[result._host.name] = result._result["stderr"]


def runner(ansible_host_path, module, args):
    """
    类似Ad-Hoc命令
    :param ansible_host_path: 一个清单文件，一行一个ip就行
    :param module:
    :param args:
    :return:
    """
    Options = namedtuple('Options',
                         ['connection',
                          'module_path',
                          'forks',
                          'private_key_file',
                          'remote_user',
                          'become',
                          'become_method',
                          'become_user',
                          'check',
                          'diff'])
    options = Options(connection='smart',
                      module_path=None,
                      forks=10,
                      private_key_file="/home/admin/.ssh/id_rsa", # 你的私钥
                      remote_user="admin",      # 远程用户
                      become=True,
                      become_method="sudo",
                      become_user="root",
                      check=False,
                      diff=False)
    # 主要加载设置的变量
    loader = DataLoader()
    # 一个密码参数，可以设置为None，默认即可，没什么影响，我用的是秘钥登录
    passwords = dict(vault_pass='secret')
    # 结果回调
    callback = ResultCallback()
    # 设置传入的机器清单
    inventory = InventoryManager(loader=loader, sources=[ansible_host_path])
    # 加载之前的变量
    variable_manager = VariableManager(loader=loader, inventory=inventory)
    play_source = dict(
            name="Ansible Play",
            hosts="all",           # all表示匹配清单所有机器，看源码发现的
            gather_facts="no",
            tasks=[
                dict(action=dict(module=module, args=args), register='shell_out'),
             ]
        )
    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

    tqm = None
    try:
        tqm = TaskQueueManager(
                  inventory=inventory,
                  variable_manager=variable_manager,
                  loader=loader,
                  options=options,
                  passwords=passwords,
                  stdout_callback=callback,
              )
        result = tqm.run(play)
    finally:
        if tqm is not None:
            tqm.cleanup()
        shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)
    # 重构输出
    result_raw = {'success': {}, 'failed': {}, 'unreachable': {}}
    for host, result in callback.host_ok.items():
        result_raw["success"][host] = result
    for host, result in callback.host_unreachable.items():
        result_raw['failed'][host] = result
    for host, result in callback.host_failed.items():
        result_raw['unreachable'][host] = result
    return json.dumps(result_raw, indent=4)
        

def runner_playbook(playbook_path, ansible_host_path):
    """
    运行playbook
    :param playbook_path: playbook的路径
    :param ansible_host_path:
    :return:
    """
    Options = namedtuple('Options',
                         ['connection',
                          'module_path',
                          'forks',
                          'private_key_file',
                          "become",
                          "become_method",
                          "become_user",
                          'check',
                          'diff',
                          "listhosts",
                          "listtasks",
                          "listtags",
                          "syntax"])
    options = Options(connection='smart',
                      module_path=None,
                      forks=10,
                      private_key_file="/home/admin/.ssh/id_rsa",  # 你的私钥
                      become=True,
                      become_method="sudo",
                      become_user="root",
                      check=False,
                      diff=False,
                      listhosts=None,
                      listtasks=None,
                      listtags=None,
                      syntax=None)

    loader = DataLoader()
    passwords = dict(vault_pass='secret')
    inventory = InventoryManager(loader=loader, sources=[ansible_host_path])
    variable_manager = VariableManager(loader=loader, inventory=inventory)

    pbex = PlaybookExecutor(playbooks=[playbook_path],
                            inventory=inventory,
                            variable_manager=variable_manager,
                            loader=loader,
                            options=options,
                            passwords=passwords)
    results = pbex.run()
    print(results)


if __name__ == "__main__":
    ansible_host_path = os.path.join(os.getcwd(), "hosts")
    data = runner(ansible_host_path, "shell", "whoami")
    print(data)
    playbook_path = os.path.join(os.getcwd(), "wctest.yml")
    runner_playbook(playbook_path, ansible_host_path)
