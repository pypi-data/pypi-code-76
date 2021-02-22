import os

def frp_connect(server_host,server_port,token,password):
    #ssh
    os.system("apt-get -qq update && apt-get -qq install -o=Dpkg::Use-Pty=0 openssh-server pwgen > /dev/null")
    print(server_host)
    os.system("echo root:%s| chpasswd"%(password))
    os.system("mkdir -p /var/run/sshd")
    os.system('echo "PermitRootLogin yes" >> /etc/ssh/sshd_config')
    os.system('echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config')
    os.system('echo "RSAAuthentication yes" >> /etc/ssh/sshd_config')
    os.system('echo "PubkeyAuthentication yes" >> /etc/ssh/sshd_config')
    os.system('echo "AuthorizedKeysFile .ssh/authorized_keys" >> /etc/ssh/sshd_config')
    os.system('echo "LD_LIBRARY_PATH=/usr/lib64-nvidia" >> /root/.bashrc')
    os.system('echo "export LD_LIBRARY_PATH" >> /root/.bashrc')
    os.system('service ssh start')
    #frp
    os.system("kill -9 $(ps aux | grep 'frpc' | awk '{print $2}')")
    os.system('wget https://github.com/fatedier/frp/releases/download/v0.35.1/frp_0.35.1_linux_amd64.tar.gz')
    os.system('tar -zxvf frp_0.35.1_linux_amd64.tar.gz')
    with open('cat frp_0.35.1_linux_amd64/frpc.ini', 'w') as f:
        f.write('''
[common]
server_addr = %s
server_port = %s
token = %s

[ssh]
type = tcp
local_ip = 127.0.0.1
local_port = 22
remote_port = 6000
        '''.strip()%(server_host,server_port,token))
    os.system('./frp_0.35.1_linux_amd64/frpc -c ./frp_0.35.1_linux_amd64/frpc.ini')