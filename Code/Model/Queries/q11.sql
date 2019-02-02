echo "select symbol,timeframe_1 tf1, timeframe_2 tf2, status,status_state state, count(*)  from candidates group by symbol,tf1,tf2,status,state order by symbol,tf1;" | psql $DB_HEROKU
