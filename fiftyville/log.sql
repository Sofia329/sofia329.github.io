-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Extract the Description from the Crime_Scene_Reports filter based on July 28, 2025, Humphrey Street
SELECT *
FROM crime_scene_reports
WHERE year = 2025 AND month = 7 AND day = 28
AND street = 'Humphrey Street';
-- Received the key information that theft it is happen in the bakery at 10:15 am
-- there are three witnesses as well

--check the interviews to see what the three witness mentioned about the theft
SELECT *
FROM interviews
WHERE year = 2025 AND month = 7 AND day = 28
/* Interviews Logs from the three withnesses

161   │ Ruth    │ 2025 │ 7     │ 28  │ Sometime within ten minutes of the theft, I saw the thief ge │
│     │         │      │       │     │ t into a car in the bakery parking lot and drive away. If yo │
│     │         │      │       │     │ u have security footage from the bakery parking lot, you mig │
│     │         │      │       │     │ ht want to look for cars that left the parking lot in that t │
│     │         │      │       │     │ ime frame.                                                   │
├─────┼─────────┼──────┼───────┼─────┼──────────────────────────────────────────────────────────────┤
│ 162 │ Eugene  │ 2025 │ 7     │ 28  │ I don't know the thief's name, but it was someone I recogniz │
│     │         │      │       │     │ ed. Earlier this morning, before I arrived at Emma's bakery, │
│     │         │      │       │     │  I was walking by the ATM on Leggett Street and saw the thie │
│     │         │      │       │     │ f there withdrawing some money.                              │
├─────┼─────────┼──────┼───────┼─────┼──────────────────────────────────────────────────────────────┤
│ 163 │ Raymond │ 2025 │ 7     │ 28  │ As the thief was leaving the bakery, they called someone who │
│     │         │      │       │     │  talked to them for less than a minute. In the call, I heard │
│     │         │      │       │     │  the thief say that they were planning to take the earliest  │
│     │         │      │       │     │ flight out of Fiftyville tomorrow. The thief then asked the  │
│     │         │      │       │     │ person on the other end of the phone to purchase the flight  │
│     │         │      │       │     │ ticket.

*/

-- Check the bakery security logs, and check the time within 10 mins of 10:15 am
SELECT *
FROM bakery_security_logs
WHERE year = 2025 AND month = 7 AND day = 28
AND hour = 10
AND minute BETWEEN 15 AND 25;

/* these are the suspicious license_plates

| id  | year | month | day | hour | minute | activity | license_plate |
+-----+------+-------+-----+------+--------+----------+---------------+
| 260 | 2025 | 7     | 28  | 10   | 16     | exit     | 5P2BI95       |
| 261 | 2025 | 7     | 28  | 10   | 18     | exit     | 94KL13X       |
| 262 | 2025 | 7     | 28  | 10   | 18     | exit     | 6P58WS2       |
| 263 | 2025 | 7     | 28  | 10   | 19     | exit     | 4328GD8       |
| 264 | 2025 | 7     | 28  | 10   | 20     | exit     | G412CB7       |
| 265 | 2025 | 7     | 28  | 10   | 21     | exit     | L93JTIZ       |
| 266 | 2025 | 7     | 28  | 10   | 23     | exit     | 322W7JE       |
| 267 | 2025 | 7     | 28  | 10   | 23     | exit     | 0NTHK55

*/

-- check the atm transaction record
SELECT * FROM atm_transactions
WHERE year = 2025 AND month = 7 AND day = 28
AND atm_location = 'Leggett Street'
AND transaction_type = 'withdraw';

/* get the 8 suspicious account_number
 id  | account_number | year | month | day |  atm_location  | transaction_type | amount |
+-----+----------------+------+-------+-----+----------------+------------------+--------+
| 246 | 28500762       | 2025 | 7     | 28  | Leggett Street | withdraw         | 48     |
| 264 | 28296815       | 2025 | 7     | 28  | Leggett Street | withdraw         | 20     |
| 266 | 76054385       | 2025 | 7     | 28  | Leggett Street | withdraw         | 60     |
| 267 | 49610011       | 2025 | 7     | 28  | Leggett Street | withdraw         | 50     |
| 269 | 16153065       | 2025 | 7     | 28  | Leggett Street | withdraw         | 80     |
| 288 | 25506511       | 2025 | 7     | 28  | Leggett Street | withdraw         | 20     |
| 313 | 81061156       | 2025 | 7     | 28  | Leggett Street | withdraw         | 30     |
| 336 | 26013199       | 2025 | 7     | 28  | Leggett Street | withdraw         | 35
*/

--From the atm_transaction, joint check with bank_accounts table
SELECT *
FROM bank_accounts ba, atm_transactions at
WHERE ba.account_number = at.account_number
AND year = 2025 AND month = 7 AND day = 28
AND atm_location = 'Leggett Street'
AND transaction_type = 'withdraw';

/* get the person_id for these 8 suspicious account_number

 account_number  │person_id  │ creation_year │ id  │ account_number │ year │ month │ day │  atm_location  │ transaction_type │ amount │
├────────────────┼───────────┼───────────────┼─────┼────────────────┼──────┼───────┼─────┼────────────────┼──────────────────┼────────┤
│ 28500762       │ 467400    │ 2014          │ 246 │ 28500762       │ 2025 │ 7     │ 28  │ Leggett Street │ withdraw         │ 48     │
│ 28296815       │ 395717    │ 2014          │ 264 │ 28296815       │ 2025 │ 7     │ 28  │ Leggett Street │ withdraw         │ 20     │
│ 76054385       │ 449774    │ 2015          │ 266 │ 76054385       │ 2025 │ 7     │ 28  │ Leggett Street │ withdraw         │ 60     │
│ 49610011       │ 686048    │ 2010          │ 267 │ 49610011       │ 2025 │ 7     │ 28  │ Leggett Street │ withdraw         │ 50     │
│ 16153065       │ 458378    │ 2012          │ 269 │ 16153065       │ 2025 │ 7     │ 28  │ Leggett Street │ withdraw         │ 80     │
│ 25506511       │ 396669    │ 2014          │ 288 │ 25506511       │ 2025 │ 7     │ 28  │ Leggett Street │ withdraw         │ 20     │
│ 81061156       │ 438727    │ 2018          │ 313 │ 81061156       │ 2025 │ 7     │ 28  │ Leggett Street │ withdraw         │ 30     │
│ 26013199       │ 514354    │ 2012          │ 336 │ 26013199       │ 2025 │ 7     │ 28  │ Leggett Street │ withdraw         │ 35     │

*/

-- accord to the interview from Raymond, the theft called someone for less than a minute
SELECT * FROM phone_calls where year = 2025 AND Month = 7 AND day = 28 AND duration < 60;
-- Check in conjuncture with people table
SELECT * FROM people WHERE phone_number IN (
    SELECT caller FROM phone_calls WHERE year = 2025 AND month = 7 AND day = 28 AND duration < 60
);

/* from checking the phone calls and further check people based on the callers, narrow down to the below 8 suspects

  id     │  name   │  phone_number  │ passport_number │ license_plate │
├────────┼─────────┼────────────────┼─────────────────┼───────────────┤
│ 395717 │ Kenny   │ (826) 555-1652 │ 9878712108      │ 30G67EN       │
│ 398010 │ Sofia   │ (130) 555-0289 │ 1695452385      │ G412CB7       │
│ 438727 │ Benista │ (338) 555-6650 │ 9586786673      │ 8X428L0       │
│ 449774 │ Taylor  │ (286) 555-6063 │ 1988161715      │ 1106N58       │
│ 514354 │ Diana   │ (770) 555-1861 │ 3592750733      │ 322W7JE       │
│ 560886 │ Kelsey  │ (499) 555-9472 │ 8294398571      │ 0NTHK55       │
│ 686048 │ Bruce   │ (367) 555-5533 │ 5773159633      │ 94KL13X       │
│ 907148 │ Carina  │ (031) 555-6622 │ 9628244268      │ Q12B3Z3

*/

-- witness also provied that theft mentioned their plan to flight out of fiftyville tmrw at the earlist flight
SELECT * FROM flights
WHERE year = 2025 AND month = 7 AND day = 29
AND origin_airport_id = (
    SELECT id FROM airports WHERE city = 'Fiftyville'
);

/* filter down to 5 unique flight id
| id | origin_airport_id | destination_airport_id | year | month | day | hour | minute |
+----+-------------------+------------------------+------+-------+-----+------+--------+
| 18 | 8                 | 6                      | 2025 | 7     | 29  | 16   | 0      |
| 23 | 8                 | 11                     | 2025 | 7     | 29  | 12   | 15     |
| 36 | 8                 | 4                      | 2025 | 7     | 29  | 8    | 20     |
| 43 | 8                 | 1                      | 2025 | 7     | 29  | 9    | 30     |
| 53 | 8                 | 9                      | 2025 | 7     | 29  | 15   | 20     |
+----+-------------------+------------------------+------+-------+-----+------+-------

airport information:

 id | abbreviation |          full_name          |    city    |
+----+--------------+-----------------------------+------------+
| 8  | CSF          | Fiftyville Regional Airport | Fiftyville

*/

--"the thief say that they were planning to take the earliest flight out of fiftyville", therefore, select the earlist flight narrow down to flight id = 36
SELECT *
FROM passengers, flights
WHERE passengers.flight_id = flights.id
AND year = 2025 AND month = 7 AND day = 29
AND flight_id =36;
/*
+-----------+-----------------+------+----+-------------------+------------------------+------+-------+-----+------+--------+
| flight_id | passport_number | seat | id | origin_airport_id | destination_airport_id | year | month | day | hour | minute |
+-----------+-----------------+------+----+-------------------+------------------------+------+-------+-----+------+--------+
| 36        | 7214083635      | 2A   | 36 | 8                 | 4                      | 2025 | 7     | 29  | 8    | 20     |
| 36        | 1695452385      | 3B   | 36 | 8                 | 4                      | 2025 | 7     | 29  | 8    | 20     |
| 36        | 5773159633      | 4A   | 36 | 8                 | 4                      | 2025 | 7     | 29  | 8    | 20     |
| 36        | 1540955065      | 5C   | 36 | 8                 | 4                      | 2025 | 7     | 29  | 8    | 20     |
| 36        | 8294398571      | 6C   | 36 | 8                 | 4                      | 2025 | 7     | 29  | 8    | 20     |
| 36        | 1988161715      | 6D   | 36 | 8                 | 4                      | 2025 | 7     | 29  | 8    | 20     |
| 36        | 9878712108      | 7A   | 36 | 8                 | 4                      | 2025 | 7     | 29  | 8    | 20     |
| 36        | 8496433585      | 7B   | 36 | 8                 | 4                      | 2025 | 7     | 29  | 8    | 20

Theft is flying to destination_airport_id = 4, they are flying to New York City

| id | abbreviation |     full_name     |     city      |
+----+--------------+-------------------+---------------+
| 4  | LGA          | LaGuardia Airport | New York City

*/

--Combining all the tables based on the constraint individually
select DISTINCT p.license_plate, p.passport_number, p.name, p.id, ba.account_number
from people p, bakery_security_logs bsl, phone_calls pc, bank_accounts ba, atm_transactions at, passengers pa, flights fl
where p.license_plate = bsl.license_plate
and p.phone_number = pc.caller
and p.id = ba.person_id
and ba.account_number = at.account_number
and pa.passport_number = p.passport_number
and pa.flight_id = fl.id
and bsl.year = 2025 and bsl.month = 7 and bsl.day = 28
and bsl.hour = 10
and bsl.minute between 15 and 25
and pc.duration < 60
and at.atm_location = 'Leggett Street'
and at.transaction_type = 'withdraw'
and pa.flight_id = 36
and fl.day = 29;

/* the theft is Bruce
| license_plate | passport_number | name  |   id   | account_number |
+---------------+-----------------+-------+--------+----------------+
| 94KL13X       | 5773159633      | Bruce | 686048 | 49610011       |
*/

--the accompliance is the person who Bruce called to
select phone_number from people where name = 'Bruce'
/*
  phone_number  |
+----------------+
| (367) 555-5533
*/

select receiver from phone_Calls
where caller = (select phone_number from people where name = 'Bruce')
and year = 2025 and month = 7 and day = 28 and duration < 60;
/*
    receiver    |
+----------------+
| (375) 555-8161
*/
select name from people
where phone_number = (
    select receiver from phone_Calls
    where caller = (select phone_number from people where name = 'Bruce')
    and year = 2025 and month = 7 and day = 28 and duration < 60
);

/* robin is the accomplice

| name  |
+-------+
| Robin
*/


select rating,
sum(rating),
sum(sum(votes)) over() as window_rating
from ratings
group by rating;

