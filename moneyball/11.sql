select players.first_name, players.last_name, (salaries.salary/performances.H) as "dollars per hit" from salaries
join performances on performances.player_id = salaries.player_id and performances.year = salaries.year
join players on players.id = salaries.player_id
where performances.year = 2001 and performances.H is not null and performances.H != 0
order by "dollars per hit" , players.first_name, players.last_name limit 10;

