psql $DB_HEROKU <<SQL
select status,status_state,count(*)
  from candidates
 group by status,status_state
 order by status,status_state;

select p.symbol,c.status,c.status_state,count(*) preVal
  from candidates c, prototypes p
 where c.proto_id=p.id
   and c.status_state='passed'
 group by p.symbol,c.status,c.status_state
 order by p.symbol;

SQL
