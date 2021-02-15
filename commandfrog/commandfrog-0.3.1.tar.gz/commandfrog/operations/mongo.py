from commandfrog.drivers.driver import Driver
from .apt import apt_install


def install_mongo(host: Driver):
    host.exec("wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add -", sudo=host.has_sudo)
    host.exec('echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list', sudo=host.has_sudo)
    host.exec("apt-get update -y", sudo=host.has_sudo)
    apt_install(host, ["mongodb-org"])
