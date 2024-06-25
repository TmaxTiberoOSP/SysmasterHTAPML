import subprocess

import tibero
from pipeline import logger

def run_tpch(max):
    for i in range(1,max):
        success = tibero.run_sqlplus_command(f"/root/HTAPML/TPC-H V3.0.1/dbgen/queries/{i}.sql")
        if success:
            try:
               with open("output.txt", "r") as file:
                data = file.read()
                logger.info("TPC-H 스크립트 수행 성공")
                return True, data
            except Exception as e:
                logger.error(f"TPC-H 스크립트 수행 실패: {e}")
                return False, None
        else:
            return False, None
    return True

def run_tpcc():
    # TPCC / TPC-H / TPC-DS 등의 벤치마크를 수행하는 코드 작성
    custom_script = "custom_script.sql"
    with open(custom_script, "w") as file:
        file.write("""
quit;
        """)
    success = tibero.run_sqlplus_command(custom_script)
    if success:
        try:
            with open("output.txt", "r") as file:
                data = file.read()
            logger.info("임의의 스크립트 수행 성공")
            return True, data
        except Exception as e:
            logger.error(f"임의의 스크립트 수행 실패: {e}")
            return False, None
    else:
        return False, None


if __name__ == "__main__":
    logger.info("테스트 코드를 여기서 작성하세요")