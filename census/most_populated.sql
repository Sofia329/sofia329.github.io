create view most_populated as
select district, sum(families), sum(households), sum(population), sum(male), sum(female) from census
group by district order by sum(population) desc;
