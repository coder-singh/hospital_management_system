mysql = {
    'host': 'db',
    'user': 'root',
    'passwd': 'root',
    'db': 'admin'
}

mysql_test = {
    'host': '0.0.0.0',
    'user': 'root',
    'passwd': '',
    'db': 'hms_test'
}

mysqlConfig = "mysql://{}:{}@{}/{}".format(
    mysql['user'],
    mysql['passwd'],
    mysql['host'],
    mysql['db']
)

mysqlConfigTest = "mysql://{}:{}@{}/{}".format(
    mysql_test['user'],
    mysql_test['passwd'],
    mysql_test['host'],
    mysql_test['db']
)

