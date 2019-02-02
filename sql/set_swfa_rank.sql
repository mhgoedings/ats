psql $DB_HEROKU <<SQL

update candidates set run_rank = 12 where opt_iterations>5000;
update candidates set run_rank = 8 where opt_iterations<3000;
update candidates set run_rank = 6 where opt_iterations<2000;
update candidates set run_rank = 5 where opt_iterations<1000;
update candidates set run_rank = 4 where opt_iterations<700;
SQL
