select name, round(avg(salary),2) as "average salary" from teams
join salaries on salaries.team_id = teams.id where salaries.year = 2001
group by name
order by "average salary" limit 5;

