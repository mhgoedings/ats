psql $DB_HEROKU <<SQL
select p.id,p.symbol,p.template,p.timeframe_1,p.status,p.status_state,p.start_run,p.end_run,c.status_state,count(c.id) cands
  from prototypes p full outer join candidates c on p.id = c.proto_id
 where p.id>90
group by p.id,p.symbol,p.template,p.timeframe_1,p.status,p.status_state,p.start_run,p.end_run,c.status_state order by p.id;
SQL
