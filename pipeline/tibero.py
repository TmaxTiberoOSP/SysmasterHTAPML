import subprocess

from dotenv import dotenv_values

from pipeline import logger
import ssh
import requests


# HTAP 최적화를 위한 정답 (label)을 DDL을 통해 수행합니다.
# DDL 스크립트를 파일로 작성하여 실행합니다.
def run_ddl_statements(argc, **params):
    ddl_script = "ddl_statements.sql"
    with open(ddl_script, "w") as file:
        file.write("""
        CREATE TABLE example (
            id NUMBER PRIMARY KEY,
            data VARCHAR2(100)
        );
        ALTER TABLE example ADD created_date DATE;
        quit;
        """)
        file.close()
        return run_sqlplus_command(ddl_script)

def change_buffer_cache_size(size):
    ddl_script = "buffer_cache_statements.sql"

    with open(ddl_script, "w") as file:
        file.write(f"""
        ALTER SYSTEM SET DB_CACHE_SIZE_TARGET={size};
        quit;
        """)
    file.close()
    return run_sqlplus_command(ddl_script)

def database_recovery(ssh_client):
    command = "sh recovery_db.sh"
    success, output = ssh.run_remote_command(ssh_client, command)
    if success:
        logger.info("Recovery tool 성공")
    else:
        logger.error(f"Recovery 실패: {output}")
    return success

# tpmagent 를 어떻게 원격으로 킬 것인가?
def run_tpmagent(ssh_client):
    command = "export TB_SID=tibero; cd HTAPML/tpmagent_dist; ./tpmagent"
    success, output = ssh.run_remote_command(ssh_client, command)
    if success:
        print(output)
        logger.info("Tpmagent 실행 성공")
    else:
        logger.error(f"Tpmagent 실행 실패: {output}")
    return success


def run_sqlplus_command(sql_script):
    try:
        config = dotenv_values(".env")
        db_address = config.get("DB_ADDRESS")
        db_username = config.get("DB_USERNAME")
        db_password = config.get("DB_PASSWORD")
        db_service = config.get("DB_SERVICE")
        result = subprocess.run(["tbsql", "-s", f"{db_username}/{db_password}@{db_address}:8620/{db_service}", f"@{sql_script}"],check=True)
        if result.returncode == 0:
            logger.info(f"{sql_script} 수행 성공")
            return True
        else:
            logger.error(f"{sql_script} 수행 실패: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"{sql_script} 수행 실패: {e}")
        return False


if __name__ == "__main__":
    logger.info("테스트 코드를 작성하세요")
