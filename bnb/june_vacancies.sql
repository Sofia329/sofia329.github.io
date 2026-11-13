create view june_vacancies as
select listings.id, property_type, host_name, count(*) as days_vacant from listings
join availabilities on listings.id = availabilities.listing_id
where availabilities.date like '2023-06%' and availabilities.available = 'TRUE'
group by listings.id;
