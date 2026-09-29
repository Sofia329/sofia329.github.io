-- create a mysql database for Shenzhen Stock Exchange, all currency defaults to CNY
create table `trades`(
    `id` bigint auto_increment primary key,
    `time` datetime not null default current_timestamp,
    `user_id` bigint not null,
    `instrument_id` bigint not null,
    `order_id` bigint not null,
    `price` decimal (18,2) unsigned not null check (`price` > 0),
    `quantity` int unsigned not null check (`quantity` > 0 ),
    `side` enum('S','B') not null,
    foreign key(`user_id`) references `users`(`id`),
    foreign key(`instrument_id`) references `instruments`(`id`),
    foreign key(`order_id`) references `orders`(`id`)
);

create table `users`(
    `id` bigint auto_increment primary key,
    `username` varchar(50) unique not null ,
    `user_since` datetime not null default current_timestamp
);

create table `balances`(
    `user_id` bigint primary key,
    `cash` decimal (18,2) not null default 0 check (cash >=0),
    foreign key(`user_id`) references `users`(`id`)
);

create table `positions`(
    `user_id` bigint not null,
    `instrument_id` bigint not null,
    `shares` int unsigned not null check (`shares` >= 0 ),
    primary key(`user_id`, `instrument_id`),
    foreign key(`user_id`) references `users`(`id`),
    foreign key(`instrument_id`) references `instruments`(`id`)
);

create table `instruments` (
    `id` bigint auto_increment primary key,
    `symbol` varchar(20) unique not null,
    `name` varchar(255) not null,
    `type` enum('stock', 'future','option', 'etf') not null
);

create table `orders` (
    `id` bigint auto_increment primary key,
    `user_id` bigint not null,
    `instrument_id` bigint not null,
    `side` enum('S','B') not null,
    `price` decimal (18,2) unsigned not null check (`price` > 0),
    `quantity` int unsigned not null check (`quantity` > 0 ),
    `order_type` enum('limit','market') not null,
    `status` enum('open','filled') not null,
    `time` datetime not null default current_timestamp,
    foreign key(`user_id`) references `users`(`id`),
    foreign key(`instrument_id`) references `instruments`(`id`)
);

-- create view to derive order book for a specific stock
-- show the top 5 levels of its best bid for each instrument
create view `order_book_bid` as
with `ranked_temp_table` as (
    select `instrument_id`, `side`, `price`, `quantity`, `time`,
    row_number() over(partition by `instrument_id`, `side` order by
    case when `side` = 'S' then `price`
         when `side` = 'B' then -`price` end asc, `time` desc) as `ranked`
    from `orders`
    where `status` = 'open' and `order_type` = 'limit'
),
`bid_table` as (
    select `instrument_id`, `price` as 'bid', `quantity` as 'bid_size'
    from `ranked_temp_table`
    where `ranked` <= 5 and `side` = 'B'
)
select * from `bid_table`;

-- create view to derive order book for a specific stock
-- show the top 5 levels of its best ask for each instrument
create view `order_book_ask` as
with `ranked_temp_table` as (
    select `instrument_id`, `side`, `price`, `quantity`, `time`,
    row_number() over(partition by `instrument_id`, `side` order by
    case when `side` = 'S' then `price`
         when `side` = 'B' then -`price` end asc, time desc) as `ranked`
    from `orders`
    where `status` = 'open' and `order_type` = 'limit'
),
`ask_table` as (
    select `instrument_id`, `price` as 'ask', `quantity` as 'ask_size'
    from `ranked_temp_table`
    where `ranked` <= 5 and `side` = 'S'
)
select * from `ask_table`;

-- set trigger once buy/sell trade, update user's cash balances
-- if balance < 0, the trigger will rollback to not update user and balance tables
delimiter //
create trigger `update_balance`
after insert on `trades`
for each row
begin
update `balances` set `cash` =
case
    when NEW.side = 'S' then `cash` + NEW.price * NEW.quantity
    else `cash` - NEW.price * NEW.quantity
end
where `user_id` = NEW.user_id;
-- if no row existed in balance table, insert a new row in balance table
insert into `balances` (`user_id`, `cash`)
select NEW.user_id, case when NEW.side = 'S' then NEW.price * NEW.quantity else -NEW.price * NEW.quantity end
where not exists (select 1 from `balances` where `user_id` = NEW.user_id);
end//
delimiter ;


-- set trigger once buy/sell trade, update user's holding positions
-- if shares < 0 in position table, trigger will rollback, which will not insert on trades
delimiter //
create trigger `update_position`
after insert on `trades`
for each row
begin
update `positions` set `shares` =
case
    when NEW.side = 'S' then `shares` - NEW.quantity
    else `shares` + NEW.quantity
end
where `user_id` = NEW.user_id
and `instrument_id` = NEW.instrument_id;
-- if no row existed in position table, insert a new row in position
insert into `positions`(`user_id`, `instrument_id`, `shares`)
select NEW.user_id, NEW.instrument_id, case when NEW.side = 'B' then NEW.quantity else -NEW.quantity end
where not exists (select 1 from `positions` where `user_id` = NEW.user_id and `instrument_id` = NEW.instrument_id);
end//
delimiter ;


-- create index for optimization
create index `search_by_username` on `users`(`username`);
create index `search_by_symbol` on `instruments`(`symbol`);
create index `idx_for_order_book` on `orders`(`status`, `order_type`);
create index `idx_for_order_book_ranking` on `orders`(`instrument_id`, `side`);
