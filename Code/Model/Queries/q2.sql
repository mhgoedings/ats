echo "select proto_id,symbol,timeframe_1 tf1, timeframe_2 tf2, input_vars, status,status_state state, count(*)  from candidates group by proto_id,symbol,tf1,tf2,input_vars,status,state order by proto_id;" | psql $DB_HEROKU