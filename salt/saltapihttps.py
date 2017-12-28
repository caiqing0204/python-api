#!/usr/bin/env python
# coding=utf-8
import json, re
import urllib
import urllib2
import ssl


ssl._create_default_https_context = ssl._create_unverified_context


class SaltAPI(object):
    def __init__(self, url, username, password):
        self.__url = url  # salt-api监控的地址和端口
        self.__user = username  # salt-api用户名
        self.__password = password  # salt-api用户密码
        self.__token_id = self.salt_login()

    def salt_login(self):
        '''获取token'''
        params = {'eauth': 'pam', 'username': self.__user, 'password': self.__password}
        print(params)
        encode = urllib.urlencode(params)
        obj = urllib.unquote(encode)
        headers = {'X-Auth-Token': ''}
        url = self.__url + '/login'
        print("url:", url)
        req = urllib2.Request(url, obj, headers)
        opener = urllib2.urlopen(req)
        print (opener)
        content = json.loads(opener.read())
        try:
            token = content['return'][0]['token']
            print("token:", token)
            return token
        except KeyError:
            raise KeyError

    def postRequest(self, obj, prefix='/'):
        '''发送请求'''
        url = self.__url + prefix
        headers = {'X-Auth-Token': self.__token_id, }
        print(url, obj, headers)
        req = urllib2.Request(url, obj, headers)
        # print(req)
        opener = urllib2.urlopen(req)
        content = json.loads(opener.read())
        return content

    def saltCmd(self, params):
        '''命令执行'''
        print(params)
        obj = urllib.urlencode(params)
        print("obj", obj, type(obj))
        obj, number = re.subn("arg\d", 'arg', obj)
        res = self.postRequest(obj)
        return res['return']

    def list_all_key(self):
        '''所有key'''
        params = {'client': 'wheel', 'fun': 'key.list_all'}
        obj = urllib.urlencode(params)
        obj, number = re.subn("arg\d", 'arg', obj)
        content = self.postRequest(obj)
        # print(content)
        minions = content['return'][0]['data']['return']['minions']
        minions_pre = content['return'][0]['data']['return']['minions_pre']
        return minions, minions_pre

    def accept_key(self, node_name):
        '''接受key'''
        params = {'client': 'wheel', 'fun': 'key.accept', 'match': node_name}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret

    def delete_key(self, node_name):
        '''删除key'''
        params = {'client': 'wheel', 'fun': 'key.delete', 'match': node_name}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret

    def async_deploy(self, tgt, arg):

        params = {'client': 'local_async', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg}
        obj = urllib.urlencode(params)
        print("obj is %s" % obj)
        content = self.postRequest(obj)
        print("content is %s" % content)
        jid = content['return'][0]['jid']
        return jid

    def target_deploy(self, tgt, arg):
        ''' 部署模块 '''
        params = {'client': 'local_async', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg, 'expr_form': 'nodegroup'}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        jid = content['return'][0]['jid']
        return jid


def main():
    sapi = SaltAPI(url='https://192.168.1.240:8888', username='saltapi', password='xxxxxx')
    # params = {'client':'local', 'fun':'test.ping', 'tgt':'某台服务器的key'}
    params = {'client': 'local', 'fun': 'test.ping', 'tgt': '*'}
    # params = {'client':'local', 'fun':'cmd.run', 'tgt':'*','arg1':'ifconfig'}
    # params = {'client':'local', 'fun':'test.echo', 'tgt':'*', 'arg1':'hello'}
    # params = {'client':'local', 'fun':'test.ping', 'tgt':'某组服务器的组名', 'expr_form':'nodegroup'}
    test = sapi.saltCmd(params)
    # test = sapi.list_all_key()
    print (test)


if __name__ == '__main__':
    main()
