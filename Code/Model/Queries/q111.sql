echo "select timeframe_1 tf1, timeframe_2 tf2, status,status_state state, count(*)  from candidates group by tf1,tf2,status,state order by tf1,tf2,state;" | psql $DB_HEROKU
echo "select status_state state, count(*)  from candidates group by state order by state;" | psql $DB_HEROKU
echo "select symbol, count(*) passed  from candidates where status_state='passed' group by symbol order by symbol;" | psql $DB_HEROKU
echo "select timeframe_1::text||':'||coalesce(timeframe_2::text,'') tf, count(*) passed  from candidates where status_state='passed' group by tf order by tf;" | psql $DB_HEROKU
