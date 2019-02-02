psql $DB_HEROKU <<SQL

select id,market_session_id sess,
       data_set d_set,data_block d_blk,
       symbol sym,chart_series,
       prestart_dt,start_dt,end_dt,
       bt_start_dt,bt_end_dt,
       status,status_state
  from prototypes
 order by id;

SQL
