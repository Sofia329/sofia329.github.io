drop table if exists temp;
create table temp (
    id integer primary key,
    phrase text not null
);

insert into temp (phrase)
select substr((select sentence from sentences where id = 14), 98,4);
insert into temp (phrase)
select substr((select sentence from sentences where id = 114), 3,5);
insert into temp (phrase)
select substr((select sentence from sentences where id = 618), 72,9);
insert into temp (phrase)
select substr((select sentence from sentences where id = 630), 7,3);
insert into temp (phrase)
select substr((select sentence from sentences where id = 932), 12,5);
insert into temp (phrase)
select substr((select sentence from sentences where id = 2230), 50,7);
insert into temp (phrase)
select substr((select sentence from sentences where id = 2346), 44,10);
insert into temp (phrase)
select substr((select sentence from sentences where id = 3041),14,5);

drop view if exists message;
create view message as
select phrase from temp;

