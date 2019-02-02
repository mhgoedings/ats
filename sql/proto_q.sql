psql $DB_HEROKU <<SQL
select id,run_rank,symbol,chart_series,status,status_state
  from prototypes 
 where status='code'   
   and status_state='done'  
 order by run_rank,id;

SQL
