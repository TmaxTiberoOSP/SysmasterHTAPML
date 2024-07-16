from datetime import datetime
import subprocess

from pipeline import logger
import psycopg2


def run_docker_compose():
    try:
        result = subprocess.run(["/home/test/release/sysmaster-db","up"], check=True)
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
    we_columns = ["we_buf_wait", "we_buf_write", "we_buf_free", "we_lgwr_archive", "we_lgwr_lnw", "we_log_flush_commit",
                  "we_tsn_sync_commit", "we_log_flush_space", "we_log_flush_req", "we_ckpt_wait", "we_rt_inflow_wait",
                  "we_smr_replay", "we_pe_comm", "we_pe_enq", "we_pe_deq", "we_acf_mtx_rw", "we_svc_tx", "we_tx_reco_suspend",
                  "we_cws_ast", "we_ccc_ast_cr", "we_ccc_ast_cur", "we_cr_buf_busy_local", "we_cr_buf_busy_global",
                  "we_cur_buf_busy_local", "we_cur_buf_busy_global", "we_gv_req", "we_gv_reply", "we_search_space_reply",
                  "we_ddl_csr_inval", "we_ddl_change_undo_ts", "we_peq", "we_alert", "we_wlock_cf", "we_wlock_tx",
                  "we_wlock_st_sgmt", "we_wlock_split", "we_wlock_dml", "we_wlock_user", "we_wlock_dd_obj", "we_wlock_dd_user",
                  "we_wlock_dd_sgmt", "we_wlock_dd_ts", "we_wlock_dd_ts_ref", "we_wlock_dd_objauth", "we_wlock_dd_sysauth",
                  "we_wlock_dd_psmir", "we_wlock_dd_pending_tx", "we_wlock_dd_partobj", "we_wlock_seq_get_nextval",
                  "we_wlock_ddl_create_ts", "we_wlock_ddl_create_df", "we_wlock_ddl_create_con", "we_wlock_xa_bucket",
                  "we_wlock_xa_glb", "we_wlock_xa_bch", "we_wlock_xa_vt", "we_wlock_dx", "we_wlock_ir", "we_wlock_temp_granule",
                  "we_wlock_cleanup_dropped_sgmt", "we_wlock_mv_rfsh", "we_wlock_ddl_recompile", "we_wlock_asysrecompile",
                  "we_wlock_dbms_pipe_list", "we_wlock_dp_temp_sgmt", "we_wlock_standby", "we_wlock_smr", "we_wlock_lnr_reverse_sync",
                  "we_wlock_auto_coalesce", "we_wlock_xtb_timeout_check", "we_wlock_revalidate_obj", "we_wlock_update_user_status",
                  "we_wlock_l1_local_cache", "we_wlock_sc_lru_cache_out", "we_wlock_dbms_lock", "we_wlock_bitmap_index", "we_wlock_bct",
                  "we_wlock_imcs", "we_wlock_imcs_priority_populate", "we_wlock_lgwr_status", "we_wlock_fb", "we_wlock_rmgr",
                  "we_wlock_ts_invalidate", "we_wlock_cf_ts", "we_wlock_job", "we_wlock_sesskey", "we_wlock_context_index",
                  "we_wlock_rt_standby", "we_wlock_usgmt", "we_wlock_rsrc", "we_wlock_setparam", "we_wlock_imt", "we_wlock_expand_rsb",
                  "we_wlock_expand_lkbset", "we_jc_buf_disk_read", "we_jc_buf_disk_readm", "we_jc_ssgmt_read_time",
                  "we_jc_ssgmt_write_time", "we_jc_buf_disk_readm_pga", "we_jc_dpbuf_wait_write", "we_jc_redo_sleep",
                  "we_jc_fdpool_invl", "we_jc_farc_write", "we_spin_buf_bucket", "we_spin_buf_ws", "we_spin_shp_alloc_lc",
                  "we_spin_shp_alloc_dd", "we_spin_shp_alloc_misc", "we_spin_shp_alloc_slab", "we_spin_shp_alloc_super",
                  "we_spin_alloc_lru"]
    stat_columns = ["block_disk_read", "multi_block_disk_read", "consistent_multi_block_gets", "consistent_block_gets",
                    "consistent_block_gets_readonly_pin", "consistent_block_gets_examine", "consistent_block_gets_examine_nowait",
                    "current_block_gets", "current_block_gets_nowait", "current_block_gets_examine", "current_block_gets_examine_nowait",
                    "total_parse_count", "hard_parse_count", "redo_entries", "redo_log_size", "redo_write", "redo_write_multi",
                    "physical_write", "req_service_time", "db_cpu_time", "user_rollbacks", "execute_count",
                    "number_of_wait_locks_granted_from_the_master", "total_round_trip_times_to_grant_wait_lock", "current_block_received",
                    "current_block_received_rtt", "cr_block_received", "cr_block_received_rtt", "current_block_send",
                    "current_block_send_fail", "current_block_send_time", "cr_block_send", "cr_block_send_fail", "cr_block_send_time",
                    "inc_messages_received", "inc_messages_received_time", "inc_messages_received_size", "inc_messages_received_by_retry",
                    "inc_messages_received_by_retry_delay_time", "inc_messages_received_by_batch", "inc_messages_received_by_batch_time",
                    "inc_packets_received", "inc_packets_received_size", "inc_messages_sent", "inc_messages_sent_time",
                    "inc_messages_sent_size", "inc_messages_sent_by_retry", "inc_messages_sent_by_retry_delay_time",
                    "inc_messages_sent_by_batch", "inc_messages_sent_by_batch_success_messages", "inc_messages_sent_from_send_queue_time",
                    "inc_packets_sent", "inc_packets_sent_size"]
    memory_columns = ["sga_usage", "pga_usage", "physical_reads", "logical_reads", "buffer_cache_hit"]
    try:
        connection = psycopg2.connect(conn_string)
        cur = connection.cursor()

        filename = datetime.now().replace(microsecond=0)
        colums = stat_columns + we_columns + memory_columns

        with open(f"{filepath}{filename}.csv", 'w') as file:
            for col in colums:
                cur.execute(f"""
                   SELECT table_name 
                   FROM information_schema.columns 
                   WHERE table_name= (select table_name from information_schema.columns where column_name='{col}' and (table_name like 'db_stat%' or table_name like 'db_event%' or table_name like 'db_memory%') and table_name !~ '[0-9]' limit 1) limit 1;
                """)
                table = cur.fetchone()
                result=[]
                if table:
                    cur.execute(f"SELECT {col} FROM public.{table[0]}")
                    tuples = cur.fetchall()
                    val_list = []
                    for tup in tuples:
                        val = str(tup[0])
                        val_list.append(val)
                    result = ','.join(val_list)
                file.write(f"{col}\n{result}\n")
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
