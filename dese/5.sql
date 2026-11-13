select city, count(*) from schools where type = 'Public School' group by city having count(*) <=3 order by count(*) desc, city;
