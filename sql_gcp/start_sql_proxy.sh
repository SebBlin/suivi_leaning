source source_env.sh
# source varieous env variables DB_USER, DB_PASS, DB_NAME, CLOUD_SQL_CONNECTION_NAME and DB_HOST

./cloud_sql_proxy -instances=$CLOUD_SQL_CONNECTION_NAME=tcp:3306
