with jointable as (
    select players.first_name, players.last_name, salaries.salary, performances.RBI, performances.H from players
    join performances on players.id = performances.player_id
    join salaries on salaries.player_id = performances.player_id and salaries.year = performances.year
    where performances.RBI is not null and performances.RBI !=0 and performances.H is not null and performances.H !=0
    and performances.year = 2001)

select first_name, last_name from jointable where salary/RBI in (select salary/RBI from jointable order by salary/RBI limit 10)
intersect
select first_name, last_name from jointable where salary/H in (select salary/H from jointable order by salary/H limit 10) order by last_name;





