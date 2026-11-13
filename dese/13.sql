-- find the school name and school district name and the drop rate which the drop rate is above avg drop rate
select schools.name, districts.name, graduation_rates.dropped from schools
join districts on schools.district_id = districts.id
join graduation_rates on graduation_rates.school_id = schools.id
where dropped > (select avg(dropped) from graduation_rates)
and schools.type = 'Public School'
order by dropped desc, schools.name, districts.name limit 10;
