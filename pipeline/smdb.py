from datetime import datetime
import subprocess

from pipeline import logger
import psycopg2


def run_docker_compose():
    try:
        result = subprocess.run(["/root/HTAPML/SysmasterHTAPML/release/sysmaster-db","up"], check=True)
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
def export_training_dataset(conn_string,filepath):
    we_tables = ["WE_BUF_WAIT", "WE_BUF_WRITE", "WE_BUF_FREE", "WE_LGWR_ARCHIVE", "WE_LGWR_LNW", "WE_LOG_FLUSH_COMMIT",
                 "WE_TSN_SYNC_COMMIT", "WE_LOG_FLUSH_SPACE", "WE_LOG_FLUSH_REQ", "WE_CKPT_WAIT", "WE_RT_INFLOW_WAIT",
                 "WE_SMR_REPLAY", "WE_PE_COMM", "WE_PE_ENQ", "WE_PE_DEQ", "WE_ACF_MTX_RW", "WE_SVC_TX", "WE_TX_RECO_SUSPEND",
                 "WE_CWS_AST", "WE_CCC_AST_CR", "WE_CCC_AST_CUR", "WE_CR_BUF_BUSY_LOCAL", "WE_CR_BUF_BUSY_GLOBAL",
                 "WE_CUR_BUF_BUSY_LOCAL", "WE_CUR_BUF_BUSY_GLOBAL", "WE_GV_REQ", "WE_GV_REPLY", "WE_SEARCH_SPACE_REPLY",
                 "WE_DDL_CSR_INVAL", "WE_DDL_CHANGE_UNDO_TS", "WE_PEQ", "WE_ALERT", "WE_WLOCK_CF", "WE_WLOCK_TX",
                 "WE_WLOCK_ST_SGMT", "WE_WLOCK_SPLIT", "WE_WLOCK_DML", "WE_WLOCK_USER", "WE_WLOCK_DD_OBJ", "WE_WLOCK_DD_USER",
                 "WE_WLOCK_DD_SGMT", "WE_WLOCK_DD_TS", "WE_WLOCK_DD_TS_REF", "WE_WLOCK_DD_OBJAUTH", "WE_WLOCK_DD_SYSAUTH",
                 "WE_WLOCK_DD_PSMIR", "WE_WLOCK_DD_PENDING_TX", "WE_WLOCK_DD_PARTOBJ", "WE_WLOCK_SEQ_GET_NEXTVAL",
                 "WE_WLOCK_DDL_CREATE_TS", "WE_WLOCK_DDL_CREATE_DF", "WE_WLOCK_DDL_CREATE_CON", "WE_WLOCK_XA_BUCKET",
                 "WE_WLOCK_XA_GLB", "WE_WLOCK_XA_BCH", "WE_WLOCK_XA_VT", "WE_WLOCK_DX", "WE_WLOCK_IR", "WE_WLOCK_TEMP_GRANULE",
                 "WE_WLOCK_CLEANUP_DROPPED_SGMT", "WE_WLOCK_MV_RFSH", "WE_WLOCK_DDL_RECOMPILE", "WE_WLOCK_ASYSRECOMPILE",
                 "WE_WLOCK_DBMS_PIPE_LIST", "WE_WLOCK_DP_TEMP_SGMT", "WE_WLOCK_STANDBY", "WE_WLOCK_SMR", "WE_WLOCK_LNR_REVERSE_SYNC",
                 "WE_WLOCK_AUTO_COALESCE", "WE_WLOCK_XTB_TIMEOUT_CHECK", "WE_WLOCK_REVALIDATE_OBJ", "WE_WLOCK_UPDATE_USER_STATUS",
                 "WE_WLOCK_L1_LOCAL_CACHE", "WE_WLOCK_SC_LRU_CACHE_OUT", "WE_WLOCK_DBMS_LOCK", "WE_WLOCK_BITMAP_INDEX", "WE_WLOCK_BCT",
                 "WE_WLOCK_IMCS", "WE_WLOCK_IMCS_PRIORITY_POPULATE", "WE_WLOCK_LGWR_STATUS", "WE_WLOCK_FB", "WE_WLOCK_RMGR",
                 "WE_WLOCK_TS_INVALIDATE", "WE_WLOCK_CF_TS", "WE_WLOCK_JOB", "WE_WLOCK_SESSKEY", "WE_WLOCK_CONTEXT_INDEX",
                 "WE_WLOCK_RT_STANDBY", "WE_WLOCK_USGMT", "WE_WLOCK_RSRC", "WE_WLOCK_SETPARAM", "WE_WLOCK_IMT", "WE_WLOCK_EXPAND_RSB",
                 "WE_WLOCK_EXPAND_LKBSET", "WE_JC_BUF_DISK_READ", "WE_JC_BUF_DISK_READM", "WE_JC_SSGMT_READ_TIME",
                 "WE_JC_SSGMT_WRITE_TIME", "WE_JC_BUF_DISK_READM_PGA", "WE_JC_DPBUF_WAIT_WRITE", "WE_JC_REDO_SLEEP",
                 "WE_JC_FDPOOL_INVL", "WE_JC_FARC_WRITE", "WE_SPIN_BUF_BUCKET", "WE_SPIN_BUF_WS", "WE_SPIN_SHP_ALLOC_LC",
                 "WE_SPIN_SHP_ALLOC_DD", "WE_SPIN_SHP_ALLOC_MISC", "WE_SPIN_SHP_ALLOC_SLAB", "WE_SPIN_SHP_ALLOC_SUPER",
                 "WE_SPIN_ALLOC_LRU"]
    stat_tables = ["BLOCK_DISK_READ", "MULTI_BLOCK_DISK_READ", "CONSISTENT_MULTI_BLOCK_GETS", "CONSISTENT_BLOCK_GETS",
                   "CONSISTENT_BLOCK_GETS_READONLY_PIN", "CONSISTENT_BLOCK_GETS_EXAMINE", "CONSISTENT_BLOCK_GETS_EXAMINE_NOWAIT",
                   "CURRENT_BLOCK_GETS", "CURRENT_BLOCK_GETS_NOWAIT", "CURRENT_BLOCK_GETS_EXAMINE", "CURRENT_BLOCK_GETS_EXAMINE_NOWAIT",
                   "TOTAL_PARSE_COUNT", "HARD_PARSE_COUNT", "REDO_ENTRIES", "REDO_LOG_SIZE", "REDO_WRITE", "REDO_WRITE_MULTI",
                   "PHYSICAL_WRITE", "REQ_SERVICE_TIME", "DB_CPU_TIME", "USER_ROLLBACKS", "EXECUTE_COUNT",
                   "NUMBER_OF_WAIT_LOCKS_GRANTED_FROM_THE_MASTER", "TOTAL_ROUND_TRIP_TIMES_TO_GRANT_WAIT_LOCK", "CURRENT_BLOCK_RECEIVED",
                   "CURRENT_BLOCK_RECEIVED_RTT", "CR_BLOCK_RECEIVED", "CR_BLOCK_RECEIVED_RTT", "CURRENT_BLOCK_SEND",
                   "CURRENT_BLOCK_SEND_FAIL", "CURRENT_BLOCK_SEND_TIME", "CR_BLOCK_SEND", "CR_BLOCK_SEND_FAIL", "CR_BLOCK_SEND_TIME",
                   "INC_MESSAGES_RECEIVED", "INC_MESSAGES_RECEIVED_TIME", "INC_MESSAGES_RECEIVED_SIZE", "INC_MESSAGES_RECEIVED_BY_RETRY",
                   "INC_MESSAGES_RECEIVED_BY_RETRY_DELAY_TIME", "INC_MESSAGES_RECEIVED_BY_BATCH", "INC_MESSAGES_RECEIVED_BY_BATCH_TIME",
                   "INC_PACKETS_RECEIVED", "INC_PACKETS_RECEIVED_SIZE", "INC_MESSAGES_SENT", "INC_MESSAGES_SENT_TIME",
                   "INC_MESSAGES_SENT_SIZE", "INC_MESSAGES_SENT_BY_RETRY", "INC_MESSAGES_SENT_BY_RETRY_DELAY_TIME",
                   "INC_MESSAGES_SENT_BY_BATCH", "INC_MESSAGES_SENT_BY_BATCH_SUCCESS_MESSAGES", "INC_MESSAGES_SENT_FROM_SEND_QUEUE_TIME",
                   "INC_PACKETS_SENT", "INC_PACKETS_SENT_SIZE"]
    try:
        connection = psycopg2.connect(conn_string)
        cur = connection.cursor()
        filename = datetime.now().replace(microsecond=0)

        with open(f"{filepath}{filename}.csv", 'w') as file:
            for we_table in we_tables:
                cur.execute(f"SELECT * FROM information_schema.tables WHERE table_name='{we_table}';")
                result = cur.fetchall()
                file.write(f"{we_table}\n{str(result)}\n")
            for stat_table in stat_tables:
                cur.execute(f"SELECT * FROM information_schema.tables WHERE table_name='{stat_table}';")
                result = cur.fetchall()
                file.write(f"{stat_table}\n{str(result)}\n")
        connection.commit()

        logger.info(f"모니터링 데이터 저장 성공: {filename}")
        cur.close()
        connection.close()
        return True
    except Exception as e:
        logger.error(f"모니터링 데이터 저장 실패: {e}")
        return False


if __name__ == "__main__":
    logger.info("테스트 코드를 여기서 작성하세요")
