psql $DB_HEROKU <<SQL
select test_type,status,status_state,count(*)
  from oos_tests
 group by test_type,status,status_state
 order by status,status_state;
SQL
