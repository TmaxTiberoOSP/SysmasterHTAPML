package com.tmaxTibero.htapbm.tpcc;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.sql.*;
import java.time.Instant;

public class TpccStatements {
    private static final Logger logger = LoggerFactory.getLogger(TpccStatements.class);
    public static final int STMT_COUNT = 37;
    private Connection conn;
    private final String[] sql = new String[] {
            // NewOrder statements.
            "SELECT c.c_discount, c.c_last, c.c_credit, w.w_tax FROM customer AS c JOIN warehouse AS w ON c.c_w_id = w_id AND w.w_id = ? AND c.c_w_id = ? AND c.c_d_id = ? AND c.c_id = ?",
            "SELECT d_next_o_id, d_tax FROM district WHERE d_id = ? AND d_w_id = ? FOR UPDATE",
            "UPDATE district SET d_next_o_id = ? + 1 WHERE d_id = ? AND d_w_id = ?",
            "INSERT INTO orders (o_id, o_d_id, o_w_id, o_c_id, o_entry_d, o_ol_cnt, o_all_local) VALUES(?, ?, ?, ?, ?, ?, ?)",
            "INSERT INTO new_orders (no_o_id, no_d_id, no_w_id) VALUES (?,?,?)",
            "SELECT i_price, i_name, i_data FROM item WHERE i_id = ?",
            "SELECT s_quantity, s_data, s_dist_01, s_dist_02, s_dist_03, s_dist_04, s_dist_05, s_dist_06, s_dist_07, s_dist_08, s_dist_09, s_dist_10 FROM stock WHERE s_i_id = ? AND s_w_id = ? FOR UPDATE",
            "UPDATE stock SET s_quantity = ? WHERE s_i_id = ? AND s_w_id = ?",
            "INSERT INTO order_line (ol_o_id, ol_d_id, ol_w_id, ol_number, ol_i_id, ol_supply_w_id, ol_quantity, ol_amount, ol_dist_info) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",

            // Payment statements.
            "UPDATE warehouse SET w_ytd = w_ytd + ? WHERE w_id = ?",
            "SELECT w_street_1, w_street_2, w_city, w_state, w_zip, w_name FROM warehouse WHERE w_id = ?",
            "UPDATE district SET d_ytd = d_ytd + ? WHERE d_w_id = ? AND d_id = ?",
            "SELECT d_street_1, d_street_2, d_city, d_state, d_zip, d_name FROM district WHERE d_w_id = ? AND d_id = ?",
            "SELECT count(c_id) FROM customer WHERE c_w_id = ? AND c_d_id = ? AND c_last = ?",
            "SELECT c_id FROM customer WHERE c_w_id = ? AND c_d_id = ? AND c_last = ? ORDER BY c_first",
            "SELECT c_first, c_middle, c_last, c_street_1, c_street_2, c_city, c_state, c_zip, c_phone, c_credit, c_credit_lim, c_discount, c_balance, c_since FROM customer WHERE c_w_id = ? AND c_d_id = ? AND c_id = ? FOR UPDATE",
            "SELECT c_data FROM customer WHERE c_w_id = ? AND c_d_id = ? AND c_id = ?",
            "UPDATE customer SET c_balance = ?, c_data = ? WHERE c_w_id = ? AND c_d_id = ? AND c_id = ?",
            "UPDATE customer SET c_balance = ? WHERE c_w_id = ? AND c_d_id = ? AND c_id = ?",
            "INSERT INTO history(h_c_d_id, h_c_w_id, h_c_id, h_d_id, h_w_id, h_date, h_amount, h_data) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",

            // OrderStat statements.
            "SELECT count(c_id) FROM customer WHERE c_w_id = ? AND c_d_id = ? AND c_last = ?",
            "SELECT c_balance, c_first, c_middle, c_last FROM customer WHERE c_w_id = ? AND c_d_id = ? AND c_last = ? ORDER BY c_first",
            "SELECT c_balance, c_first, c_middle, c_last FROM customer WHERE c_w_id = ? AND c_d_id = ? AND c_id = ?",
            "SELECT o_id, o_entry_d, COALESCE(o_carrier_id,0) FROM orders WHERE o_w_id = ? AND o_d_id = ? AND o_c_id = ? AND o_id = (SELECT MAX(o_id) FROM orders WHERE o_w_id = ? AND o_d_id = ? AND o_c_id = ?)",
            "SELECT ol_i_id, ol_supply_w_id, ol_quantity, ol_amount, ol_delivery_d FROM order_line WHERE ol_w_id = ? AND ol_d_id = ? AND ol_o_id = ?",

            // Delivery statements.
            "SELECT COALESCE(MIN(no_o_id),0) FROM new_orders WHERE no_d_id = ? AND no_w_id = ?",
            "DELETE FROM new_orders WHERE no_o_id = ? AND no_d_id = ? AND no_w_id = ?",
            "SELECT o_c_id FROM orders WHERE o_id = ? AND o_d_id = ? AND o_w_id = ?",
            "UPDATE orders SET o_carrier_id = ? WHERE o_id = ? AND o_d_id = ? AND o_w_id = ?",
            "UPDATE order_line SET ol_delivery_d = ? WHERE ol_o_id = ? AND ol_d_id = ? AND ol_w_id = ?",
            "SELECT SUM(ol_amount) FROM order_line WHERE ol_o_id = ? AND ol_d_id = ? AND ol_w_id = ?",
            "UPDATE customer SET c_balance = c_balance + ? , c_delivery_cnt = c_delivery_cnt + 1 WHERE c_id = ? AND c_d_id = ? AND c_w_id = ?",

            // Slev statements.
            "SELECT d_next_o_id FROM district WHERE d_id = ? AND d_w_id = ?",
            "SELECT DISTINCT ol_i_id FROM order_line WHERE ol_w_id = ? AND ol_d_id = ? AND ol_o_id < ? AND ol_o_id >= (? - 20)",
            "SELECT count(*) FROM stock WHERE s_w_id = ? AND s_i_id = ? AND s_quantity < ?",

            // These are used in place of pStmts[0] in order to avoid joins
            "SELECT c_discount, c_last, c_credit FROM customer WHERE c_w_id = ? AND c_d_id = ? AND c_id = ?",
            "SELECT w_tax FROM warehouse WHERE w_id = ?"
    };

    String jdbcUrl;
    String dbUser;
    String dbPassword;
    int fetchSize;
    Long lastResetTime = Instant.now().toEpochMilli();

    public TpccStatements(Connection conn, int fetchSize) {
        this.conn = conn;
        this.jdbcUrl = Tpcc.jdbcUrl;
        this.dbUser = Tpcc.dbUser;
        this.dbPassword = Tpcc.dbPassword;
        this.fetchSize = fetchSize;
    }

    public PreparedStatement prepareStatement(String sql) throws SQLException {
        if (sql.startsWith("SELECT")) {
            return conn.prepareStatement(sql, ResultSet.TYPE_FORWARD_ONLY, ResultSet.CONCUR_READ_ONLY);
        } else {
            return conn.prepareStatement(sql, PreparedStatement.NO_GENERATED_KEYS);
        }
    }

    public String getSqlString(int idx) throws SQLException {
        return sql[idx];
    }

    public void setAutoCommit(boolean b) throws SQLException {
        conn.setAutoCommit(b);
    }

    /**
     * Commit a transaction.
     */
    public void commit() throws SQLException {
        logger.trace("COMMIT");
        conn.commit();
        resetConnection();
    }

    /**
     * Rollback a transaction.
     */
    public void rollback() throws SQLException {
        logger.trace("ROLLBACK");
        conn.rollback();
        resetConnection();
    }

    public void closeConnection() {
        try {
            if (conn != null) {
                conn.close();
            }
        } catch (SQLException e) {
            logger.error("Error closing connection", e);
        }
    }

    private void resetConnection() throws SQLException {
        Long now = Instant.now().toEpochMilli();
        if ((now - lastResetTime) < 1000) {
            return;
        }

        closeConnection();

        // Retry logic
        final int maxTries = 10;
        for (int attempt = 1; attempt <= maxTries; attempt++) {
            try {
                conn = DriverManager.getConnection(jdbcUrl, dbUser, dbPassword);
                lastResetTime = Instant.now().toEpochMilli();
                return;
            } catch (SQLException e) {
                lastResetTime = Instant.now().toEpochMilli();
                if (attempt == maxTries) {
                    throw e; // Throw the exception after the last attempt
                }
                try {
                    // Delay before retrying
                    Thread.sleep(100); // 0.1 second delay
                } catch (InterruptedException ie) {
                    Thread.currentThread().interrupt(); // Restore the interrupted status
                    throw new SQLException("Interrupted while retrying connection", ie);
                }
            }
        }
    }
}
