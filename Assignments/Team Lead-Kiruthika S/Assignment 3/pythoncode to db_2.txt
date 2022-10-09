import ibm_db
import sys


def get_connection():
    db_name = ""
    db_host_name = ""
    db_port = ""
    db_protocol = ""
    db_username = ""
    db_password = ""

    try:
        conn = ibm_db.connect(
        f"DATABASE = {db_name}; HOSTNAME = {db_host_name}; PORT = {db_port}; PROTOCOL = {db_protocol}; "
        f"UID = {db_username}; PWD = {db_password};", "", "")
        return conn
    except:
        print("no connection:", ibm_db.conn_errormsg())
        sys.exit(1)

get_connection()
