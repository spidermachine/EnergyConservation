CREATE EXTERNAL TABLE hbase_stock(rowkey STRING, code STRING, name STRING, price STRING,
delta STRING, delta_ratio STRING, start STRING, last STRING, height STRING, low STRING, count STRING,
amount STRING, stto STRING, amount_ratio STRING, appoint_than STRING, amplitude STRING, pe STRING, LTSZ STRING, MC STRING, ret_per STRING, net_income STRING, major_income STRING, category STRING, url STRING)
STORED BY 'org.apache.hadoop.hive.hbase.HBaseStorageHandler'
WITH SERDEPROPERTIES ('hbase.columns.mapping' = ':key, cf:code, cf:name, cf:price, cf:delta, cf:delta_ratio, cf:start, cf:last, cf:height, cf:low, cf:count, cf:amount, cf:stto, cf:amount_ratio, cf:appoint_than, cf:amplitude, cf:pe, cf:ltsz, cf:mc, cf:ret_per, cf:net_income, cf:major_income, cf:category, cf:url')
TBLPROPERTIES('hbase.table.name'='stock');