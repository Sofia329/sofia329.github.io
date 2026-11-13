CREATE TABLE users (
    id int auto_increment primary key,
    first_name varchar(20) not null,
    last_name varchar(10) not null,
    username varchar(20) unique not null,
    password varchar(255) not null
);


CREATE TABLE schools (
    id int auto_increment primary key,
    school varchar(255) not null,
    type enum('Primary', 'Secondary','Higher Education') not null,
    location varchar(255),
    year_founded year
);

CREATE TABLE companies (
    id int auto_increment primary key,
    company varchar(255) not null,
    industry enum('Technology', 'Education', 'Business') not null,
    location varchar(50)
);


CREATE TABLE school_connections(
    user_id int not null,
    school_id int not null,
    start_date date not null ,
    end_date date,
    type enum('BA', 'MA', 'PhD') not null,
    primary key(user_id, school_id),
    foreign key (user_id) references users(id),
    foreign key (school_id) references schools(id)
);

CREATE TABLE people_connections (
    follower int not null,
    following int not null,
    start_date date,
    created_at timestamp default current_timestamp,
    primary key(follower, following),
    foreign key(follower) references users(id),
    foreign key (following) references users(id),
    check (follower != following)
);

CREATE TABLE company_connections (
    user_id int not null,
    company_id int not null,
    start_date date,
    primary key( user_id, company_id),
    foreign key(user_id) references users(id),
    foreign key(company_id) references companies(id)
);
