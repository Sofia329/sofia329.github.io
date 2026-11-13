select name from districts join expenditures on districts.id = expenditures.district_id group by name order by pupils limit 1;

