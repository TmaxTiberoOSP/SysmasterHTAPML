import subprocess
from pipeline import logger


def run_docker_compose():
    try:
        result = subprocess.run(["docker-compose", "-f", "docker-compose.yml", "up", "-d"], check=True)
        if result.returncode == 0:
            logger.info("docker-compose 실행 성공")
            return True
        else:
            logger.error(f"docker-compose 실행 실패: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"docker-compose 실행 실패: {e}")
        return False


# Sysmaster 에 수집된 데이터 및 Labeling 데이터를 저장하는 함수.
# 1. PostgreSQL 에 저장되어 있는 데이터를 가져와서 파일로 저장하는 코드 작성.
# 2. 현재 세팅값 설정을 저장하는 코드 작성.
def export_training_dataset():
    try:
        logger.info("모니터링 데이터 저장 성공")
        return True
    except Exception as e:
        logger.error(f"모니터링 데이터 저장 실패: {e}")
        return False


if __name__ == "__main__":
    logger.info("테스트 코드를 여기서 작성하세요")
