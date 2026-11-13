select round(2026 - avg(birth_year) ,2) as "Average Age" from players where debut >= '2000-01-01';
