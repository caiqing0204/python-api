import paramiko, json, os


def ssh(ip, port, username, password, cmd, passkey=None):
    try:
        ssh = paramiko.SSHClient()  # 创建ssh对象
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if passkey:
            ssh.connect(hostname=ip, port=int(port), username=username, pkey=passkey, )
        else:
            ssh.connect(hostname=ip, port=int(port), username=username, password=password, )

        stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)

        result = stdout.read()
        result1 = result.decode()
        error = stderr.read().decode('utf-8')

        if not error:
            ret = {"ip": ip, "data": result1}
            ssh.close()
            return ret
    except Exception as e:
        error = "账号或密码错误,{}".format(e)
        ret = {"ip": ip, "data": error}
        return ret


def sftp(ip, port, username, password, local_path, server_path):
    try:
        t = paramiko.Transport(ip, port)
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(local_path, server_path)
        t.close()
        ret = {"ip": ip, "data": "上传成功"}
        return ret
    except Exception as e:
        error = "上传失败,{}".format(e)
        ret = {"ip": ip, "data": error}
        return ret


def sftp_down_file(ip, port, username, password, local_path, server_path):
    try:
        t = paramiko.Transport(ip, port)
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.get(server_path, local_path, )
        t.close()
        ret = {"ip": ip, "data": "下载成功"}
        return ret
    except Exception as e:
        error = "下载失败,{}".format(e)
        ret = {"ip": ip, "data": error}
        return ret
