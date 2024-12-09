import os
import subprocess
import threading

import tibero
from pipeline import logger
import time


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


def stream_output(pipe, output_function):
    # 실시간으로 출력 스트림을 읽어 처리
    for line in iter(pipe.readline, ''):
        output_function(line, end='')
    pipe.close()


# Benchbase 코드 수정 필요.
def run_benchbase(path:str="/home/test/HTAPML/SysmasterHTAPML/source") -> bool:
    start_time = time.time()

    try:
        process = subprocess.Popen(
            ["sh", "tpcc.sh"],
            cwd=path,
            env=os.environ.copy(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,  # 텍스트 모드로 출력 스트림을 처리
            #text=True,
            bufsize=1,  # 실시간 출력
        )

        # 스레드를 사용해 stdout과 stderr를 동시에 처리
        stdout_thread = threading.Thread(target=stream_output, args=(process.stdout, print))
        stderr_thread = threading.Thread(target=stream_output, args=(process.stderr, print))

        stdout_thread.start()
        stderr_thread.start()

        # 프로세스가 종료될 때까지 기다림
        process.wait()

        # 스레드가 모두 종료될 때까지 기다림
        stdout_thread.join()
        stderr_thread.join()

        elapsed_time = time.time() - start_time
        logger.info(f"Benchbase TPC-C 실행 성공, {elapsed_time:.2f} 초")
        return True
    except Exception as e:
        logger.error(f"Benchbase TPC-C 실행 실패: {e}")
        return False

if __name__ == "__main__":
    logger.info("테스트 코드를 여기서 작성하세요")