select first_name, last_name, salaries.salary, performances.HR, salaries.year
from players
join performances on players.id = performances.player_id
join salaries on salaries.player_id = players.id and salaries.year = performances.year
order by players.id, salaries.year desc, performances.HR desc, salaries.salary desc;
