Template = """[Unit]
Description=The Salt Minion
Documentation=man:salt-minion(1) file:///usr/share/doc/salt/html/contents.html https://docs.saltstack.com/en/latest/contents.html
After=network.target salt-master.service

[Service]
KillMode=process
Type=notify
NotifyAccess=all
LimitNOFILE=8192
ExecStart={service_bin} {service_bin_args}

[Install]
WantedBy=multi-user.target
"""


def disable(hub):
    ...


def enable(hub):
    ...


def start(hub):
    ...


def stop(hub):
    ...


def restart(hub):
    ...
