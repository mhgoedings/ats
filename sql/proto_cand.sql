psql $DB_HEROKU <<SQL
select p.id,p.symbol,p.template_version,p.chart_series,p.status,p.status_state,p.start_run,p.end_run,count(c.id) cands from prototypes p full outer join candidates c on p.id = c.proto_id group by p.id,p.symbol,p.template_version,p.chart_series,p.status,p.status_state,p.start_run,p.end_run order by p.symbol;
SQL
