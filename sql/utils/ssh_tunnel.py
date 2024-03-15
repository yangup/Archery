# -*- coding:utf-8 -*-
"""
@author: EliasChiang
@license: Apache Licence
@file: ssh_tunnel.py
@time: 2020/05/09
"""
from sshtunnel import SSHTunnelForwarder
from io import StringIO
from paramiko import RSAKey, Ed25519Key, ECDSAKey, DSSKey, PKey
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import ed25519, dsa, rsa, ec
import io


class SSHConnection(object):
    """
    ssh隧道连接类，用于映射ssh隧道端口到本地，连接结束时需要清理
    """

    def __init__(
        self,
        host,
        port,
        tun_host,
        tun_port,
        tun_user,
        tun_password,
        pkey,
        pkey_password,
    ):
        self.host = host
        self.port = int(port)
        self.tun_host = tun_host
        self.tun_port = int(tun_port)
        self.tun_user = tun_user
        self.tun_password = tun_password
        self.pkey = pkey
        self.pkey_password = pkey_password

        if pkey:
            self.private_key = self.get_private_key()
            self.server = SSHTunnelForwarder(
                ssh_address_or_host=(self.tun_host, self.tun_port),
                ssh_username=self.tun_user,
                ssh_pkey=self.private_key,
                remote_bind_address=(self.host, self.port),
            )
        else:
            self.server = SSHTunnelForwarder(
                ssh_address_or_host=(self.tun_host, self.tun_port),
                ssh_username=self.tun_user,
                ssh_password=self.tun_password,
                remote_bind_address=(self.host, self.port),
            )
        self.server.start()

    def __del__(self):
        self.server.close()

    def get_ssh(self):
        """
        获取ssh映射的端口
        :param request:
        :return:
        """
        return "127.0.0.1", self.server.local_bind_port

    def get_private_key(self):
        private_key_file_obj = io.StringIO()
        private_key_file_obj.write(self.pkey)
        private_key_file_obj.seek(0)
        file_obj = private_key_file_obj
        password = self.pkey_password
        file_bytes = bytes(file_obj.read(), "utf-8")
        try:
            key = crypto_serialization.load_ssh_private_key(
                file_bytes,
                password=password,
            )
            file_obj.seek(0)
        except ValueError:
            key = crypto_serialization.load_pem_private_key(
                file_bytes,
                password=password,
            )
            if password:
                encryption_algorithm = crypto_serialization.BestAvailableEncryption(
                    password
                )
            else:
                encryption_algorithm = crypto_serialization.NoEncryption()
            file_obj = StringIO(
                key.private_bytes(
                    crypto_serialization.Encoding.PEM,
                    crypto_serialization.PrivateFormat.OpenSSH,
                    encryption_algorithm,
                ).decode("utf-8")
            )
        if isinstance(key, rsa.RSAPrivateKey):
            private_key = RSAKey.from_private_key(file_obj, password)
        elif isinstance(key, ed25519.Ed25519PrivateKey):
            private_key = Ed25519Key.from_private_key(file_obj, password)
        elif isinstance(key, ec.EllipticCurvePrivateKey):
            private_key = ECDSAKey.from_private_key(file_obj, password)
        elif isinstance(key, dsa.DSAPrivateKey):
            private_key = DSSKey.from_private_key(file_obj, password)
        else:
            raise TypeError
        return private_key
