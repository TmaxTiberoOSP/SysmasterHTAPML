import paramiko
from pipeline import logger


def connect(hostname, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username, password=password)
        return ssh
    except Exception as e:
        logger.error(f"SSH 연결 실패: {e}")
        return None


def run_remote_command(ssh, command):
    try:
        stdin, stdout, stderr = ssh.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            return True, stdout.read().decode('utf-8')
        else:
            return False, stderr.read().decode('utf-8')
    except Exception as e:
        return False, str(e)


if __name__ == "__main__":
    conn = connect("hostname", "username", "password")
    logger.info("테스트 코드를 여기서 작성하세요")
