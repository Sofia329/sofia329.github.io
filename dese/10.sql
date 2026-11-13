select districts.name, expenditures.per_pupil_expenditure from districts
join expenditures on districts.id = expenditures.district_id
where type = 'Public School District'
order by per_pupil_expenditure desc limit 10;
