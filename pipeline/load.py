import os
import subprocess

import tibero
from pipeline import logger, ssh


def run_script():
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

def run_benchbase(path):
    try:
        result = subprocess.run(["sh","tpcc.sh"],env=os.environ.copy(),cwd=path, check=True)
        print(result)

        if result.returncode == 0:
            logger.info("Benchbase TPC-C 실행 성공")
            return True
        else:
            logger.error(f"Benchbase TPC-C 실행 실패: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"Benchbase TPC-C 실행 실패: {e}")
        return False


if __name__ == "__main__":
    logger.info("테스트 코드를 여기서 작성하세요")