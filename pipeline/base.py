import tibero
import ssh
import smdb
import load
from dotenv import load_dotenv, dotenv_values
import time
from pipeline import logger


# python 3.12 작성.
# 대략적인 파이프라인 코드의 framework 작성.
def main_pipeline():
    # TODO: 실제로는 TAC 환경에서 돌아가야 하기 때문에 2노드 클러스터 환경을 고려해야 함.
    config = dotenv_values(".env")
    hostname = config.get("HOSTNAME")
    username = config.get("USERNAME")
    password = config.get("PASSWORD")
    filepath =config.get("FILEPATH")
    dockerpath = config.get("DOCKER_PATH")
    conn_string = config.get("CONNECTION_STRING")
    benchpath = config.get("BENCH_PATH")
    size = config.get("BUFFERCACHE_SIZE")
    params = {
    }

    quit_pipeline = False
    while not quit_pipeline:
        connection = ssh.connect(hostname, username, password)
        if connection is None:
            break

        if not tibero.database_recovery(connection):
            break

        if not tibero.change_buffer_cache_size(size):
            break

#        if not tibero.run_ddl_statements(params):
#            break

        if not smdb.run_docker_compose(dockerpath):
            break

        if not load.run_benchbase(benchpath):
            break

        if not smdb.export_training_dataset(conn_string, filepath, test_name="sample"):
            break

        if not smdb.clean_postgre_db(conn_string):
            break

        if not smdb.down_docker_compose(dockerpath):
            break

        logger.info("Loop Complete")
        quit_pipeline = True


if __name__ == "__main__":
    load_dotenv()
    main_pipeline()
