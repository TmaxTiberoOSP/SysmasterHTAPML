from datetime import datetime
import os
import subprocess

from pipeline import logger
import psycopg2
import sysmaster_table
from datetime import datetime, timedelta, timezone


script_dir = os.path.dirname(os.path.abspath(__file__))


def run_docker_compose(dockerpath):
    try:
        result = subprocess.run(["sudo", "docker", "compose", "-f", f"{dockerpath}/docker-compose.yml", "up", "-d"],
                                check=True)

        if result.returncode == 0:
            logger.info("docker-compose 실행 성공")
            return True
        else:
            logger.error(f"docker-compose 실행 실패: {result.stderr}")
            return False

    except Exception as e:
        logger.error(f"docker-compose 실행 실패: {e}")
        return False


def down_docker_compose(dockerpath):
    try:
        result = subprocess.run(["sudo", "docker", "compose", "-f", f"{dockerpath}/docker-compose.yml", "down"],
                                check=True)
        if result.returncode == 0:
            logger.info("docker-compose 종료 성공")
            return True
        else:
            logger.error(f"docker-compose 종료 실패: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"docker-compose 종료 실패: {e}")
        return False


def create_table(conn_string):
    connection = psycopg2.connect(conn_string)
    cur = connection.cursor()

    schema_file_path = os.path.join(script_dir, "schema.sql")
    with open(schema_file_path, "r") as schema_file:
        schema_sql = schema_file.read()

    # 읽은 SQL 스크립트를 실행
    cur.execute(schema_sql)
    cur.close()
    connection.close()


def clean_postgre_db(conn_string):
    try:
        connection = psycopg2.connect(conn_string)
        cur = connection.cursor()

        for table, columns in sysmaster_table.all_table.items():
            if len(columns) == 0:
                continue
            cur.execute(f"""
                TRUNCATE TABLE public.{table} 
            """)

        connection.commit()
        logger.info(f"postgre 초기화 성공")
        schema_file_path = os.path.join(script_dir, "schema.sql")
        with open(schema_file_path, "r") as schema_file:
            schema_sql = schema_file.read()

        # 읽은 SQL 스크립트를 실행
        cur.execute(schema_sql)
        cur.close()
        connection.close()
        return True
    except Exception as e:
        logger.error(f"postgre 초기화 실패: {e}")
        return False


# Sysmaster 에 수집된 데이터 및 Labeling 데이터를 저장하는 함수.
# 1. PostgreSQL 에 저장되어 있는 데이터를 가져와서 파일로 저장하는 코드 작성.
# 2. 현재 세팅값 설정을 저장하는 코드 작성.
def export_training_dataset(conn_string, filepath, test_name):
    try:
        connection = psycopg2.connect(conn_string)
        cur = connection.cursor()
        filename = test_name + datetime.now().replace(microsecond=0).strftime("%m%d%H%M%S")
        res = "R001"

        start_time = datetime.now(timezone.utc) - timedelta(minutes=2)

        with open(f"{filepath}{filename}.csv", 'w') as file:
            for table, columns in sysmaster_table.all_table.items():
                if len(columns) == 0:
                    continue
                cols = ",".join(columns)
                cur.execute(f"""
                SELECT LOG_TIME,{cols} FROM public.{table} 
                WHERE RES_ID = '{res}' AND LOG_TIME > '{start_time}'
                ORDER BY LOG_TIME DESC
                LIMIT 120 
                """)
                tuples = cur.fetchall()
                file.write("nums," + cols + "\n")

                for i, row in enumerate(tuples, start=1):
                    line = f"{i}," + ','.join(map(str, row))
                    file.write(line + '\n')

        connection.commit()

        logger.info(f"모니터링 데이터 저장 성공: {filename}")
        cur.close()
        connection.close()
        return True
    except Exception as e:
        logger.error(f"모니터링 데이터 저장 실패: {e}")
        return False


if __name__ == "__main__":
    from dotenv import load_dotenv, dotenv_values
    config = dotenv_values(".env")
    conn_string = config.get("CONNECTION_STRING")
    filepath =config.get("FILEPATH")
    create_table(conn_string)
    export_training_dataset(conn_string, filepath)
