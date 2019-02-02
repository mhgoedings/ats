psql $DB_HEROKU <<SQL
select id,
       symbol,
       trade_count,
       (comm_entry_dol+comm_exit_dol+slippage_entry_dol+slippage_exit_dol) costs,
       avg_trade,
       avg_trade / (comm_entry_dol+comm_exit_dol+slippage_entry_dol+slippage_exit_dol) ratio,
       drawdown_intra,
       net_profit,
       net_profit/drawdown_intra*-1 npdd,
       --sharpe_ratio,
       profit_factor,percent_winners,
       avg_winner*percent_winners/100 - avg_loser*(1-percent_winners)/100 Exp
  from oos_tests
 where avg_trade > 0
   and slippage_entry_dol is not null
 order by ratio desc
 --order by npdd desc
 limit 20;
SQL
