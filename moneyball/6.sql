select teams.name, sum(performances.H) as "total hits" from teams
join performances on performances.team_id = teams.id
where performances.year = 2001 group by teams.name order by "total hits" desc limit 5;
