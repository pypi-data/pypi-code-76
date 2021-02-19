
BROKER_SERVER_URL = 'amqp://public:Happy123@10.192.225.185'

FTP_SER_HOST = "c21iLXN3bGFiLmNuLXN6aDAyLm54cC5jb20="
FTP_CRED = ('bWN1eHByZXNzbw==', 'bWN1X254cF8yMDIw')

DAPENG_INSTANCE = {
    "prod1": {
        "ip": "dapeng.cn-sha02.nxp.com",
        "state_exchange": "dapeng.cn-sha02.nxp.com.dapeng.state",
    },

    "prod2": {
        "ip": "dapeng.ap.freescale.net",
        "state_exchange": "dapeng.dapeng.state",
    },

    "stage": {
        "ip": "lsv11069.swis.cn-sha01.nxp.com",
        "state_exchange": "lsv11069.swis.cn-sha01.nxp.com.dapeng.state",
    }
}

DPC_REPOS = {
    'stationscript': "ssh://git@bitbucket.sw.nxp.com/msvc/stationscript.git",
    'pymcutk': "ssh://git@bitbucket.sw.nxp.com/msvc/pymcutk.git",
}

DPC_ROOTS = {
    'windows': "C:/Dpc",
    'linux': "/opt/Dpc",
    'darwin': "/usr/local/Dpc"
}
