import json
import ibm_db

SSL_DSN = "DATABASE=BLUDB;HOSTNAME=db2w-tiggaci.us-east.db2w.cloud.ibm.com;PORT=50001;PROTOCOL=TCPIP;UID=bluadmin;PWD=H1_8dZY@YOuHF9BHmT7ZWhdBdQX@k;Security=SSL;"


def get_connection(ssl_dsn=None):
    if ssl_dsn is None:
        conn = ibm_db.connect(SSL_DSN, "", "")
    else:
        conn = ibm_db.connect(ssl_dsn, "", "")
    # ibm_db.autocommit(conn, ibm_db.SQL_AUTOCOMMIT_OFF)

    return conn


def execute_query(config, sql):

    db = config.get("DATABASE")
    host = config.get("HOSTNAME")
    port = config.get("PORT")
    protocol = config.get("PROTOCOL")
    uid = config.get("UID")
    password = config.get("PASSWORD")
    security = config.get("SECURITY")

    ssl_dsn = "DATABASE={};HOSTNAME={};PORT={};PROTOCOL={};UID={};PWD={};Security={};".format(
        db, host, port, protocol, uid, password, security)

    conn = get_connection(ssl_dsn=ssl_dsn)

    stmt = ibm_db.exec_immediate(conn, sql)
    data = ibm_db.fetch_assoc(stmt)

    dict_list = []

    # if data:
    #     print(data['BRANCH_CODE'])
    #     # dict_list.append(data)
    #     data = ibm_db.fetch_both(stmt)

    while data:
        dict_list.append(data)
        data = ibm_db.fetch_assoc(stmt)

    
    return dict_list


def execute(config, sql):

    try:
        db = config.get("DATABASE")
        host = config.get("HOSTNAME")
        port = config.get("PORT")
        protocol = config.get("PROTOCOL")
        uid = config.get("UID")
        password = config.get("PASSWORD")
        security = config.get("SECURITY")

        ssl_dsn = "DATABASE={};HOSTNAME={};PORT={};PROTOCOL={};UID={};PWD={};Security={};".format(
            db, host, port, protocol, uid, password, security)

        conn = get_connection(ssl_dsn=ssl_dsn)
        ibm_db.exec_immediate(conn, sql)
        # ibm_db.bind_param(stmt, 1, animal)
    except:
        print
        "Transaction couldn't be completed:", ibm_db.stmt_errormsg()
    else:
        print
        "Transaction complete."

    return "SUCCESS"


if __name__ == "__main__":
    DB2_CONFIG = {
        "DATABASE": "BLUDB",
        "HOSTNAME": "db2w-tiggaci.us-east.db2w.cloud.ibm.com",
        "PORT": 50001,
        "PROTOCOL": "TCPIP",
        "UID": "bluadmin",
        "PASSWORD": "H1_8dZY@YOuHF9BHmT7ZWhdBdQX@k",
        "SECURITY": "SSL"
    }
    
    result = execute_query(DB2_CONFIG, 
        "Select parent, child from everestschema.REF_CONTRACT_CHECKLIST where version='v1'")
    print (result)
    # SQL = "INSERT INTO REQUEST (encoded_id, submission_id, entity_name, country_code, status) VALUES ('XXXX', 1, 'Test', 'US', 'ACTIVE')"
    # execute(SQL)
