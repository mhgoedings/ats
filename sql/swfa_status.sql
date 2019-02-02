psql $DB_HEROKU <<SQL
select c.run_rank,proto_id,c.id,p.symbol,p.chart_series,c.status,c.status_state,
       opt_iterations,reopt_bars,reopt_days,
       c.start_run,c.end_run-c.start_run duration
  from candidates c, prototypes p
 where c.proto_id=p.id
 order by c.id;

select p.symbol,c.status,c.status_state,count(*)
  from candidates c, prototypes p
 where c.proto_id=p.id
 group by p.symbol,c.status,c.status_state
 order by p.symbol;

SQL
