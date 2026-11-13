CREATE TABLE users (
    id integer primary key,
    first_name text not null,
    last_name text not null,
    username text unique,
    password text not null
);

CREATE TABLE schools (
    id integer primary key,
    school text not null,
    type text not null,
    start_date numeric not null,
    end_date numeric not null,
    location text,
    year_founded integer

);

CREATE TABLE companies (
    id integer primary key,
    company text not null,
    industry text not null,
    location text
);
CREATE TABLE school_connections(
    user_id integer not null,
    school_id integer not null,
    start_date text,
    primary key(user_id, school_id),
    foreign key (user_id) references users(id),
    foreign key (school_id) references schools(id)
);

CREATE TABLE people_connections (
    follower integer not null,
    following integer not null,
    start_date text,
    primary key(follower, following),
    foreign key(follower) references users(id),
    foreign key (following) references users(id),
    check (follower != following)
);


CREATE TABLE company_connections (
    user_id integer not null,
    company_id integer not null,
    start_date text,
    primary key( user_id, company_id)
    foreign key(user_id) references users(id),
    foreign key(company_id) references companies(id)

);
