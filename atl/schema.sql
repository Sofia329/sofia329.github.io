CREATE TABLE passengers (
    "id" integer primary key,
    "first_name" text not null,
    "last_name" text not null,
    "age" integer,
    "checkin_datetime" numeric not null,
    "flight_id" integer not null,
    foreign key ("flight_id") references flights("id")
);

CREATE TABLE flights (
    "id" integer primary key,
    "flight_number" text not null,
    "airline" text not null,
    "checkin_closing_datetime" numeric not null,
    "checkin_concourse" text not null,
    "departure_airport_code" text not null,
    "destination_airport_code" text not null,
    "departure_datetime" numeric not null,
    "arrival_datetime" numeric not null
);
