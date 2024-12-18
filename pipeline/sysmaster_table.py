class SysmasterTable:
    def __init__(self):
        self.all_table = self._generate_tables()

    @staticmethod
    def _generate_tables():
        tables = {"_db_event_backup": [
            "WE_WLOCK_BITMAP_INDEX_TIME",
            "WE_WLOCK_BITMAP_INDEX_COUNT"
        ], "_db_event_cluster": [
            "WE_TSN_SYNC_COMMIT_TIME",
            "WE_TSN_SYNC_COMMIT_COUNT",
            "WE_CCC_AST_CR_TIME",
            "WE_CCC_AST_CR_COUNT",
            "WE_CCC_AST_CUR_TIME",
            "WE_CCC_AST_CUR_COUNT",
            "WE_CR_BUF_BUSY_LOCAL_TIME",
            "WE_CR_BUF_BUSY_LOCAL_COUNT",
            "WE_CR_BUF_BUSY_GLOBAL_TIME",
            "WE_CR_BUF_BUSY_GLOBAL_COUNT",
            "WE_CUR_BUF_BUSY_LOCAL_TIME",
            "WE_CUR_BUF_BUSY_LOCAL_COUNT",
            "WE_CUR_BUF_BUSY_GLOBAL_TIME",
            "WE_CUR_BUF_BUSY_GLOBAL_COUNT",
            "WE_WLOCK_TEMP_GRANULE_TIME",
            "WE_WLOCK_TEMP_GRANULE_COUNT"
        ], "_db_event_concurrency": [
            "WE_BUF_WAIT_TIME",
            "WE_BUF_WAIT_COUNT",
            "WE_BUF_FREE_TIME",
            "WE_BUF_FREE_COUNT",
            "WE_CKPT_WAIT_TIME",
            "WE_CKPT_WAIT_COUNT",
            "WE_WLOCK_TX_TIME",
            "WE_WLOCK_TX_COUNT",
            "WE_WLOCK_SEQ_GET_NEXTVAL_TIME",
            "WE_WLOCK_SEQ_GET_NEXTVAL_COUNT",
            "WE_WLOCK_L1_LOCAL_CACHE_TIME",
            "WE_WLOCK_L1_LOCAL_CACHE_COUNT",
            "WE_SPIN_BUF_BUCKET_TIME",
            "WE_SPIN_BUF_BUCKET_COUNT",
            "WE_SPIN_BUF_WS_TIME",
            "WE_SPIN_BUF_WS_COUNT"
        ], "_db_event_dd": [
            "WE_WLOCK_USER_TIME",
            "WE_WLOCK_USER_COUNT",
            "WE_WLOCK_DD_OBJ_TIME",
            "WE_WLOCK_DD_OBJ_COUNT",
            "WE_WLOCK_DD_USER_TIME",
            "WE_WLOCK_DD_USER_COUNT",
            "WE_WLOCK_DD_TS_TIME",
            "WE_WLOCK_DD_TS_COUNT",
            "WE_WLOCK_DD_OBJAUTH_TIME",
            "WE_WLOCK_DD_OBJAUTH_COUNT",
            "WE_WLOCK_DD_SYSAUTH_TIME",
            "WE_WLOCK_DD_SYSAUTH_COUNT",
            "WE_WLOCK_DD_PSMIR_TIME",
            "WE_WLOCK_DD_PSMIR_COUNT",
            "WE_WLOCK_DD_PENDING_TX_TIME",
            "WE_WLOCK_DD_PENDING_TX_COUNT",
            "WE_WLOCK_DD_PARTOBJ_TIME",
            "WE_WLOCK_DD_PARTOBJ_COUNT"
        ], "_db_event_io": [
            "WE_BUF_WRITE_TIME",
            "WE_BUF_WRITE_COUNT",
            "WE_JC_BUF_DISK_READ_TIME",
            "WE_JC_BUF_DISK_READ_COUNT",
            "WE_JC_BUF_DISK_READM_TIME",
            "WE_JC_BUF_DISK_READM_COUNT",
            "WE_JC_SSGMT_READ_TIME_TIME",
            "WE_JC_SSGMT_READ_TIME_COUNT",
            "WE_JC_SSGMT_WRITE_TIME_TIME",
            "WE_JC_SSGMT_WRITE_TIME_COUNT",
            "WE_JC_BUF_DISK_READM_PGA_TIME",
            "WE_JC_BUF_DISK_READM_PGA_COUNT"
        ], "_db_event_psm": [
            "WE_WLOCK_DDL_RECOMPILE_TIME",
            "WE_WLOCK_DDL_RECOMPILE_COUNT",
            "WE_WLOCK_JOB_TIME",
            "WE_WLOCK_JOB_COUNT"
        ], "_db_event_redo": [
            "WE_LGWR_ARCHIVE_TIME",
            "WE_LGWR_ARCHIVE_COUNT",
            "WE_LOG_FLUSH_COMMIT_TIME",
            "WE_LOG_FLUSH_COMMIT_COUNT",
            "WE_LOG_FLUSH_SPACE_TIME",
            "WE_LOG_FLUSH_SPACE_COUNT"
        ], "_db_event_space": [
            "WE_WLOCK_ST_SGMT_TIME",
            "WE_WLOCK_ST_SGMT_COUNT",
            "WE_WLOCK_USGMT_TIME",
            "WE_WLOCK_USGMT_COUNT"
        ], "_db_event_sql_tac": [
            "WE_SEARCH_SPACE_REPLY_TIME",
            "WE_SEARCH_SPACE_REPLY_COUNT"
        ], "_db_stat": [
            "BLOCK_DISK_READ",
            "MULTI_BLOCK_DISK_READ",
            "CONSISTENT_MULTI_BLOCK_GETS",
            "CONSISTENT_BLOCK_GETS",
            "CONSISTENT_BLOCK_GETS_EXAMINE",
            "CURRENT_BLOCK_GETS",
            "CURRENT_BLOCK_GETS_EXAMINE",
            "REDO_LOG_SIZE",
            "REDO_WRITE",
            "PHYSICAL_WRITE"
        ], "_db_tac_stat": [
            "CURRENT_BLOCK_RECEIVED",
            "CURRENT_BLOCK_RECEIVED_RTT",
            "CR_BLOCK_RECEIVED",
            "CR_BLOCK_RECEIVED_RTT",
            "CURRENT_BLOCK_SEND",
            "CURRENT_BLOCK_SEND_TIME",
            "CR_BLOCK_SEND",
            "CR_BLOCK_SEND_TIME"
        ]}

        # Define the mapping of tables and columns based on the provided enum data
        return tables
