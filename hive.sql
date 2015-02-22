CREATE EXTERNAL TABLE hbase_stock(rowkey STRING, code STRING, name STRING, price STRING,
delta STRING, delta_ratio STRING, start STRING, last STRING, height STRING, low STRING, count STRING,
amount STRING, stto STRING, amount_ratio STRING, appoint_than STRING, amplitude STRING, pe STRING, LTSZ STRING, MC STRING, ret_per STRING, net_income STRING, major_income STRING, category STRING, url STRING)
STORED BY 'org.apache.hadoop.hive.hbase.HBaseStorageHandler'
WITH SERDEPROPERTIES ('hbase.columns.mapping' = ':key, cf:code, cf:name, cf:price, cf:delta, cf:delta_ratio, cf:start, cf:last, cf:height, cf:low, cf:count, cf:amount, cf:stto, cf:amount_ratio, cf:appoint_than, cf:amplitude, cf:pe, cf:ltsz, cf:mc, cf:ret_per, cf:net_income, cf:major_income, cf:category, cf:url')
TBLPROPERTIES('hbase.table.name'='stock');

CREATE EXTERNAL TABLE hbase_fund_share(rowkey STRING, code STRING, name STRING, url STRING, percentage STRING, amount STRING, fund STRING)
STORED BY 'org.apache.hadoop.hive.hbase.HBaseStorageHandler'
WITH SERDEPROPERTIES ('hbase.columns.mapping' = ':key, cf:code, cf:name, cf:url, cf:percentage, cf:amount, cf:fund')
TBLPROPERTIES('hbase.table.name'='share');

CREATE EXTERNAL TABLE hbase_stock_new_grade(rowkey STRING, name STRING, code STRING, grade STRING, master STRING, group STRING, date STRING, price STRING, now_price STRING, url STRING)
STORED BY 'org.apache.hadoop.hive.hbase.HBaseStorageHandler'
WITH SERDEPROPERTIES ('hbase.columns.mapping' = ':key, cf:name, cf:code, cf:grade, cf:master, cf:group, cf:date, cf:price, cf:now_price, cf:url')
TBLPROPERTIES('hbase.table.name'='stock_new_grade');