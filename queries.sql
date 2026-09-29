-- select all trades for specific user_id
select * from trades
where user_id = 1;

--select all trades for specific username
select * from trades where user_id = (
    select id from users
    where username = 'sofiamamama'
);

-- select all trades for specific instrument id
select * from trades where instrument_id = (
    select id from instruments
    where symbol = '002594'
);

-- see when the user first join this exchange
 select user_since from users
 where username = 'sofiamamama';

 -- check the balances for the specific user
 select cash from balances where user id = (
    select id from users
    where username = 'sofiamamama'
);

-- check what is the current position for stock 002594 for user sofiamamama
select * from positions
where instrument_id = 1 and user_id = (
    select id from users where username = 'alice'
);

-- add some balance to the user account
update balances set cash = 1000 where user_id = (
    select id from users where username = 'sofiamamama'
);

-- retireve the specific instrument information, by given symbol
select * from instruments where symbol = '002594';

-- see all the top 10 recent filled orders for '002594'
select * from orders
where instrument_id = 1 and status = 'filled'
order by time desc limit 10;

-- see the bid order book for ticker '002594'
select * from order_book_bid
where instrument_id = (select id from instruments where symbol = '002594');

-- see the ask order book for ticker '002594'
select * from order_book_ask
where instrument_id = (select id from instruments where symbol = '158005');

-- insert record in user/trades/instruments/orders tables
-- balances and positions table will be auto update by triggers when insert records in trades table
insert into users(username)
values('sofiamamama');

insert into trades(user_id, instrument_id, price, quantity, side)
values(1,1, 87.81, 5, 'B' )

insert into instruments (symbol, name, type)
values ('KO', 'The Coca Cola Company', 'stock');

insert into orders (user_id, instrument_id, side, price, quantity, order_type, status)
values(1,1,'B', 87.81, 5, 'limit', 'open');
