psql $DB_HEROKU <<SQL
select c.id,c.run_rank,p.symbol,c.opt_iterations,c.status,c.status_state,c.proto_id 
  from candidates c, prototypes p
 where c.status='code'   
   and c.status_state='done'  
   and c.proto_id = p.id
 order by run_rank;

SQL
