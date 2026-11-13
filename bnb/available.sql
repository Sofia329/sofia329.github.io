create view available as
select listings.id, property_type, host_name, date from listings
join availabilities on listings.id = availabilities.listing_id
where availabilities.available = 'TRUE';
