psql $DB_HEROKU <<SQL
select o.id,
       o.symbol,
       trade_count,
       (o.comm_entry_dol+o.comm_exit_dol+o.slippage_entry_dol+o.slippage_exit_dol) costs,
       avg_trade,
       avg_trade / (o.comm_entry_dol+o.comm_exit_dol+o.slippage_entry_dol+o.slippage_exit_dol) ratio,
       drawdown_intra,
       net_profit,
       net_profit/drawdown_intra*-1 npdd,
       sharpe_ratio, profit_factor,percent_winners
  from oos_tests o, markets m
 where avg_trade > 0
   and o.slippage_entry_dol is not null
   and o.sec_id = m.id
   and m.group_1 = 'Metals'
 order by npdd desc
 limit 10;
SQL
