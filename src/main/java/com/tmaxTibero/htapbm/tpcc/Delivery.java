package com.tmaxTibero.htapbm.tpcc;

import java.sql.*;
import java.util.Calendar;
import java.util.Date;

import org.slf4j.LoggerFactory;
import org.slf4j.Logger;

public class Delivery implements TpccConstants {
    private static final Logger logger = LoggerFactory.getLogger(Driver.class);
    private static final boolean DEBUG = logger.isDebugEnabled();
    private static final boolean TRACE = logger.isTraceEnabled();

    private TpccStatements pStmts;

    public Delivery(TpccStatements pStmts) {
        this.pStmts = pStmts;
    }

    public int delivery(int w_id_arg, int o_carrier_id_arg) {
        try {
            // Start a transaction.
            pStmts.setAutoCommit(false);
            if (DEBUG) logger.debug("Transaction:	Delivery");
            int w_id = w_id_arg;
            int o_carrier_id = o_carrier_id_arg;
            int d_id = 0;
            int c_id = 0;
            int no_o_id = 0;
            float ol_total = 0;

            Calendar calendar = Calendar.getInstance();
            Date now = calendar.getTime();
            Timestamp currentTimeStamp = new Timestamp(now.getTime());

            for (d_id = 1; d_id <= DIST_PER_WARE; d_id++) {


                // Get the prepared statement.
                //"SELECT COALESCE(MIN(no_o_id),0) FROM new_orders WHERE no_d_id = ? AND no_w_id = ?"
                if (TRACE)
                    logger.trace("SELECT COALESCE(MIN(no_o_id),0) FROM new_orders WHERE no_d_id = " + d_id + " AND no_w_id = " + w_id);
                try (PreparedStatement pstmt = pStmts.prepareStatement(pStmts.getSqlString(25))) {
                    pstmt.setInt(1, d_id);
                    pstmt.setInt(2, w_id);

                    try (ResultSet rs = pstmt.executeQuery()) {
                        if (rs.next()) {
                            no_o_id = rs.getInt(1);
                        }
                    }
                } catch (SQLException e) {
                    logger.error("SELECT COALESCE(MIN(no_o_id),0) FROM new_orders WHERE no_d_id = " + d_id + " AND no_w_id = " + w_id, e);
                    throw new Exception("Delivery Select transaction error", e);
                }


                if (no_o_id == 0) {
                    continue;
                } else {
                    if (DEBUG) logger.debug("No_o_id did not equal 0 -> " + no_o_id);
                }

                //Get the prepared statement
                //"DELETE FROM new_orders WHERE no_o_id = ? AND no_d_id = ? AND no_w_id = ?"
                if (TRACE)
                    logger.trace("DELETE FROM new_orders WHERE no_o_id = " + no_o_id + " AND no_d_id = " + d_id + " AND no_w_id = " + w_id);
                try (PreparedStatement pstmt = pStmts.prepareStatement(pStmts.getSqlString(26))) {
                    pstmt.setInt(1, no_o_id);
                    pstmt.setInt(2, d_id);
                    pstmt.setInt(3, w_id);
                    pstmt.executeUpdate();
                } catch (SQLException e) {
                    logger.error("DELETE FROM new_orders WHERE no_o_id = " + no_o_id + " AND no_d_id = " + d_id + " AND no_w_id = " + w_id, e);
                    throw new Exception("Delivery Delete transaction error", e);
                }

                //Get the prepared statement
                //"SELECT o_c_id FROM orders WHERE o_id = ? AND o_d_id = ? AND o_w_id = ?"
                try (PreparedStatement pstmt = pStmts.prepareStatement(pStmts.getSqlString(27))) {
                    pstmt.setInt(1, no_o_id);
                    pstmt.setInt(2, d_id);
                    pstmt.setInt(3, w_id);

                    try (ResultSet rs = pstmt.executeQuery()) {
                        if (rs.next()) {
                            c_id = rs.getInt(1);
                        }
                    }
                } catch (SQLException e) {
                    logger.error("SELECT o_c_id FROM orders WHERE o_id = " + no_o_id + " AND o_d_id = " + d_id + " AND o_w_id = " + w_id, e);
                    throw new Exception("Delivery Select transaction error", e);
                }


                //Get the prepared Statement
                //"UPDATE orders SET o_carrier_id = ? WHERE o_id = ? AND o_d_id = ? AND o_w_id = ?"
                if (TRACE)
                    logger.trace("UPDATE orders SET o_carrier_id = " + o_carrier_id + " WHERE o_id = " + no_o_id + " AND o_d_id = " + d_id + " AND o_w_id = " + w_id);
                try (PreparedStatement pstmt = pStmts.prepareStatement(pStmts.getSqlString(28))) {
                    pstmt.setInt(1, o_carrier_id);
                    pstmt.setInt(2, no_o_id);
                    pstmt.setInt(3, d_id);
                    pstmt.setInt(4, w_id);
                    pstmt.executeUpdate();
                } catch (SQLException e) {
                    logger.error("UPDATE orders SET o_carrier_id = " + o_carrier_id + " WHERE o_id = " + no_o_id + " AND o_d_id = " + d_id + " AND o_w_id = " + w_id, e);
                    throw new Exception("Delivery Update transaction error", e);
                }

                //Get the prepared Statement
                //"UPDATE order_line SET ol_delivery_d = ? WHERE ol_o_id = ? AND ol_d_id = ? AND ol_w_id = ?"
                try (PreparedStatement pstmt = pStmts.prepareStatement(pStmts.getSqlString(29))) {
                    pstmt.setTimestamp(1, currentTimeStamp);
                    pstmt.setInt(2, no_o_id);
                    pstmt.setInt(3, d_id);
                    pstmt.setInt(4, w_id);
                    pstmt.executeUpdate();
                } catch (SQLException e) {
                    logger.error("UPDATE order_line SET ol_delivery_d = " + currentTimeStamp + " WHERE ol_o_id = " + no_o_id + " AND ol_d_id = " + d_id + " AND ol_w_id = " + w_id, e);
                    throw new Exception("Delivery Update transaction error", e);
                }

                //Get the prepared Statement
                //"SELECT SUM(ol_amount) FROM order_line WHERE ol_o_id = ? AND ol_d_id = ? AND ol_w_id = ?"
                if (TRACE)
                    logger.trace("SELECT SUM(ol_amount) FROM order_line WHERE ol_o_id = " + no_o_id + " AND ol_d_id = " + d_id + " AND ol_w_id = " + w_id);
                try (PreparedStatement pstmt = pStmts.prepareStatement(pStmts.getSqlString(30))) {
                    pstmt.setInt(1, no_o_id);
                    pstmt.setInt(2, d_id);
                    pstmt.setInt(3, w_id);

                    try (ResultSet rs = pstmt.executeQuery()) {
                        if (rs.next()) {
                            ol_total = rs.getFloat(1);
                        }
                    }
                } catch (SQLException e) {
                    logger.error("SELECT SUM(ol_amount) FROM order_line WHERE ol_o_id = " + no_o_id + " AND ol_d_id = " + d_id + " AND ol_w_id = " + w_id, e);
                    throw new Exception("Delivery Select transaction error", e);
                }

                try (PreparedStatement pstmt = pStmts.prepareStatement(pStmts.getSqlString(31))) {
                    pstmt.setFloat(1, ol_total);
                    pstmt.setInt(2, c_id);
                    pstmt.setInt(3, d_id);
                    pstmt.setInt(4, w_id);
                    pstmt.executeUpdate();
                } catch (SQLException e) {
                    logger.error("UPDATE customer SET c_balance = c_balance + " + ol_total + ", c_delivery_cnt = c_delivery_cnt + 1 WHERE c_id = " + c_id + " AND c_d_id = " + d_id + " AND c_w_id = " + w_id, e);
                    throw new Exception("Delivery Update transaction error", e);
                }
            }

            // Commit.
            pStmts.commit();

            return 1;

        } catch (Exception e) {
            try {
                // Rollback if an aborted transaction, they are intentional in some percentage of cases.
                pStmts.rollback();
                return 0;
            } catch (Throwable th) {
                throw new RuntimeException("Delivery error", th);
            } finally {
                logger.error("Delivery error", e);
            }
        }
    }

}
