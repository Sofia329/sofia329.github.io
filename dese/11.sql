select name, per_pupil_expenditure, graduated from schools
join expenditures on schools.district_id = expenditures.district_id
join graduation_rates on graduation_rates.school_id = schools.id
order by per_pupil_expenditure desc, name;
