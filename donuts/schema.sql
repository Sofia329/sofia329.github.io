CREATE TABLE ingredients (
    id integer primary key,
    ingredient text not null unique,
    unit text not null,
    price_per_unit real not null
);

CREATE TABLE donuts (
    id integer primary key,
    name text not null,
    gluten_free integer not null,
    price numeric not null
);

--many to many relationship between ingredients and donuts
CREATE TABLE ingredients_donuts(
    ingredient_id integer not null,
    donut_id integer not null,
    primary key(ingredient_id, donut_id),
    foreign key (ingredient_id) references ingredients(id),
    foreign key (donut_id) references donuts(id)
);

CREATE TABLE customers (
    id integer primary key,
    first_name text not null,
    last_name text
);

CREATE TABLE orders (
    id integer primary key,
    order_number text not null unique,
    customer_id integer,
    foreign key(customer_id) references customers(id)
);

--many to many relationship between donuts and orders
CREATE TABLE orders_donuts (
    donut_id integer not null,
    order_id integer not null,
    primary key(donut_id, order_id),
    foreign key (donut_id) references donuts(id),
    foreign key (order_id) references orders(id)
);


