echo "select robust_level,count(*) from strategies group by robust_level order by robust_level;" | psql $DB_HEROKU
