create view frequently_reviewed as
select listings.id, property_type, host_name, count(*) as reviews from listings
join reviews on listings.id = reviews.listing_id
group by listings.id
order by reviews desc, property_type, host_name limit 100;
