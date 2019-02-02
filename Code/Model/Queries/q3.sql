echo "select symbol,status,status_state,robust_level,count(*) from strategies group by symbol,status,status_state,robust_level order by symbol,status,robust_level;" | psql $DB_HEROKU
echo "select robust_level,count(*) from strategies group by robust_level order by robust_level;" | psql $DB_HEROKU
echo "select status_state state, count(*)  from candidates group by state order by state;" | psql $DB_HEROKU
