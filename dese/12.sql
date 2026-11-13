select districts.name, expenditures.per_pupil_expenditure, staff_evaluations.exemplary from districts
join expenditures on districts.id = expenditures.district_id
join staff_evaluations on districts.id = staff_evaluations.district_id
where per_pupil_expenditure > (select avg(per_pupil_expenditure) from expenditures)
and exemplary > (select avg(exemplary) from staff_evaluations)
and type = 'Public School District'
order by exemplary desc, per_pupil_expenditure desc;
