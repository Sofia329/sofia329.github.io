drop table if exists temp;
create table temp (
    name text,
    id integer primary key,
    nametype text,
    class text,
    mass real,
    discovery text,
    year real,
    lat real,
    long real
);

-- import meteorites.csv into temp table
.import --csv --skip 1 meteorites.csv temp

-- replacing empty values to NULL for mass, year, lat, long columns
update temp set mass = NULL where mass = '';
update temp set year = NULL where year = '';
update temp set lat = NULL where lat = '';
update temp set long = NULL where long = '';

-- filter out meteorites which nametype = 'Relict'
delete from temp where nametype = 'Relict';

-- then drop nametype column
alter table temp drop column nametype;

-- mass, lat, long columns rounded to 2 decimal places
update temp set mass = round(mass,2);
update temp set lat = round(lat,2);
update temp set long = round(long,2);

-- create meteorites table
drop table if exists meteorites;
create table meteorites (
    id integer primary key,
    name text,
    class text,
    mass real,
    discovery text,
    year real,
    lat real,
    long real
);

--insert into meteorites table with organised and cleaned temp table, order by year, then name
insert into meteorites (name, class, mass, discovery, year, lat, long)
select name, class, mass, discovery, year, lat, long from temp order by year, name;

-- drop temp table
drop table temp;
