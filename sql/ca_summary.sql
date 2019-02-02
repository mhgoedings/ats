psql $DB_HEROKU <<SQL

select symbol,count(*) from strategies group by symbol order by symbol;
select robust_level,count(*) from strategies group by robust_level order by robust_level;

select symbol,robust_level,count(*) from strategies group by symbol,robust_level order by robust_level,symbol;

#select symbol,robust_level,count(*) from strategies group by grouping sets (symbol,robust_level,());

select symbol,robust_level,count(*)
  from strategies
 group by rollup (symbol,robust_level)
 order by robust_level,symbol;
SQL
