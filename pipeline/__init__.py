import logging

# 로깅 설정
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 포맷터 설정
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# 파일 핸들러 설정
file_handler = logging.FileHandler('pipeline.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# 콘솔 핸들러 설정
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# 로거에 핸들러 추가
logger.addHandler(file_handler)
logger.addHandler(console_handler)
