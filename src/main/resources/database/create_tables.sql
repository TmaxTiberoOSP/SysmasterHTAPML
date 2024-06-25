CREATE TABLE warehouse
(
    w_id NUMBER(5) NOT NULL,
    w_name VARCHAR2(10),
    w_street_1 VARCHAR2(20),
    w_street_2 VARCHAR2(20),
    w_city VARCHAR2(20),
    w_state CHAR(2),
    w_zip CHAR(9),
    w_tax NUMBER(4,2),
    w_ytd NUMBER(12,2),
    CONSTRAINT pk_warehouse PRIMARY KEY (w_id)
);

CREATE TABLE district
(
    d_id        NUMBER(3) NOT NULL, -- tinyint in MySQL is equivalent to NUMBER(3) in Oracle
    d_w_id      NUMBER(5) NOT NULL, -- smallint in MySQL is equivalent to NUMBER(5) in Oracle
    d_name      VARCHAR2(10),
    d_street_1  VARCHAR2(20),
    d_street_2  VARCHAR2(20),
    d_city      VARCHAR2(20),
    d_state     CHAR(2),
    d_zip       CHAR(9),
    d_tax       NUMBER(4, 2),       -- decimal in MySQL is equivalent to NUMBER in Oracle
    d_ytd       NUMBER(12, 2),
    d_next_o_id NUMBER,             -- int in MySQL is equivalent to NUMBER in Oracle
    CONSTRAINT pk_district PRIMARY KEY (d_w_id, d_id)
);

CREATE TABLE customer
(
    c_id NUMBER NOT NULL,                   -- int in MySQL is equivalent to NUMBER in Oracle
    c_d_id NUMBER(3) NOT NULL,              -- tinyint in MySQL is equivalent to NUMBER(3) in Oracle
    c_w_id NUMBER(5) NOT NULL,              -- smallint in MySQL is equivalent to NUMBER(5) in Oracle
    c_first VARCHAR2(16),
    c_middle CHAR(2),
    c_last VARCHAR2(16),
    c_street_1 VARCHAR2(20),
    c_street_2 VARCHAR2(20),
    c_city VARCHAR2(20),
    c_state CHAR(2),
    c_zip CHAR(9),
    c_phone CHAR(16),
    c_since TIMESTAMP,
    c_credit CHAR(2),
    c_credit_lim NUMBER(19),                -- bigint in MySQL is equivalent to NUMBER(19) in Oracle
    c_discount NUMBER(4,2),                 -- decimal in MySQL is equivalent to NUMBER in Oracle
    c_balance NUMBER(12,2),
    c_ytd_payment NUMBER(12,2),
    c_payment_cnt NUMBER(5),                -- smallint in MySQL is equivalent to NUMBER(5) in Oracle
    c_delivery_cnt NUMBER(5),               -- smallint in MySQL is equivalent to NUMBER(5) in Oracle
    c_data CLOB,                            -- text in MySQL is equivalent to CLOB in Oracle for large text
    CONSTRAINT pk_customer PRIMARY KEY (c_w_id, c_d_id, c_id)
);

CREATE TABLE history
(
    h_c_id NUMBER NOT NULL,          -- int in MySQL is equivalent to NUMBER in Oracle
    h_c_d_id NUMBER(3),              -- tinyint in MySQL is equivalent to NUMBER(3) in Oracle
    h_c_w_id NUMBER(5),              -- smallint in MySQL is equivalent to NUMBER(5) in Oracle
    h_d_id NUMBER(3),                -- tinyint in MySQL is equivalent to NUMBER(3) in Oracle
    h_w_id NUMBER(5),                -- smallint in MySQL is equivalent to NUMBER(5) in Oracle
    h_date TIMESTAMP,                -- datetime in MySQL is equivalent to TIMESTAMP in Oracle
    h_amount NUMBER(6,2),            -- decimal in MySQL is equivalent to NUMBER in Oracle
    h_data VARCHAR2(24)
);

CREATE TABLE new_orders
(
    no_o_id NUMBER NOT NULL,         -- int in MySQL is equivalent to NUMBER in Oracle
    no_d_id NUMBER(3) NOT NULL,      -- tinyint in MySQL is equivalent to NUMBER(3) in Oracle
    no_w_id NUMBER(5) NOT NULL,      -- smallint in MySQL is equivalent to NUMBER(5) in Oracle
    CONSTRAINT pk_new_orders PRIMARY KEY (no_w_id, no_d_id, no_o_id)
);

CREATE TABLE orders
(
    o_id NUMBER NOT NULL,            -- int in MySQL is equivalent to NUMBER in Oracle
    o_d_id NUMBER(3) NOT NULL,       -- tinyint in MySQL is equivalent to NUMBER(3) in Oracle
    o_w_id NUMBER(5) NOT NULL,       -- smallint in MySQL is equivalent to NUMBER(5) in Oracle
    o_c_id NUMBER,                   -- int in MySQL is equivalent to NUMBER in Oracle
    o_entry_d TIMESTAMP,             -- datetime in MySQL is equivalent to TIMESTAMP in Oracle
    o_carrier_id NUMBER(3),          -- tinyint in MySQL is equivalent to NUMBER(3) in Oracle
    o_ol_cnt NUMBER(3),              -- tinyint in MySQL is equivalent to NUMBER(3) in Oracle
    o_all_local NUMBER(3),           -- tinyint in MySQL is equivalent to NUMBER(3) in Oracle
    CONSTRAINT pk_orders PRIMARY KEY (o_w_id, o_d_id, o_id)
);


CREATE TABLE order_line
(
    ol_o_id NUMBER NOT NULL,          -- int in MySQL is equivalent to NUMBER in Oracle
    ol_d_id NUMBER(3) NOT NULL,       -- tinyint in MySQL is equivalent to NUMBER(3) in Oracle
    ol_w_id NUMBER(5) NOT NULL,       -- smallint in MySQL is equivalent to NUMBER(5) in Oracle
    ol_number NUMBER(3) NOT NULL,     -- tinyint in MySQL is equivalent to NUMBER(3) in Oracle
    ol_i_id NUMBER,                   -- int in MySQL is equivalent to NUMBER in Oracle
    ol_supply_w_id NUMBER(5),         -- smallint in MySQL is equivalent to NUMBER(5) in Oracle
    ol_delivery_d TIMESTAMP,          -- datetime in MySQL is equivalent to TIMESTAMP in Oracle
    ol_quantity NUMBER(3),            -- tinyint in MySQL is equivalent to NUMBER(3) in Oracle
    ol_amount NUMBER(6,2),            -- decimal in MySQL is equivalent to NUMBER in Oracle
    ol_dist_info CHAR(24),
    CONSTRAINT pk_order_line PRIMARY KEY (ol_w_id, ol_d_id, ol_o_id, ol_number)
);

CREATE TABLE item
(
    i_id NUMBER NOT NULL,            -- int in MySQL is equivalent to NUMBER in Oracle
    i_im_id NUMBER,                  -- int in MySQL is equivalent to NUMBER in Oracle
    i_name VARCHAR2(24),
    i_price NUMBER(5,2),             -- decimal in MySQL is equivalent to NUMBER in Oracle
    i_data VARCHAR2(50),
    CONSTRAINT pk_item PRIMARY KEY (i_id)
);

CREATE TABLE stock
(
    s_i_id NUMBER NOT NULL,             -- int in MySQL is equivalent to NUMBER in Oracle
    s_w_id NUMBER(5) NOT NULL,          -- smallint in MySQL is equivalent to NUMBER(5) in Oracle
    s_quantity NUMBER(5),               -- smallint in MySQL is equivalent to NUMBER(5) in Oracle
    s_dist_01 CHAR(24),
    s_dist_02 CHAR(24),
    s_dist_03 CHAR(24),
    s_dist_04 CHAR(24),
    s_dist_05 CHAR(24),
    s_dist_06 CHAR(24),
    s_dist_07 CHAR(24),
    s_dist_08 CHAR(24),
    s_dist_09 CHAR(24),
    s_dist_10 CHAR(24),
    s_ytd NUMBER(8),                    -- decimal(8,0) in MySQL is equivalent to NUMBER(8) in Oracle
    s_order_cnt NUMBER(5),              -- smallint in MySQL is equivalent to NUMBER(5) in Oracle
    s_remote_cnt NUMBER(5),             -- smallint in MySQL is equivalent to NUMBER(5) in Oracle
    s_data VARCHAR2(50),
    CONSTRAINT pk_stock PRIMARY KEY (s_w_id, s_i_id)
);
