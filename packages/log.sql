
-- *** The Lost Letter ***

sqlite> select * from addresses where address = '900 Somerville Avenue';
+-----+-----------------------+-------------+
| id  |        address        |    type     |
+-----+-----------------------+-------------+
| 432 | 900 Somerville Avenue | Residential |

sqlite> select * from packages where from_address_id = 432;
+------+-----------------------+-----------------+---------------+
|  id  |       contents        | from_address_id | to_address_id |
+------+-----------------------+-----------------+---------------+
| 384  | Congratulatory letter | 432             | 854           |
| 2437 | String                | 432             | 484           |
| 3529 | Letter opener         | 432             | 585           |
| 5436 | Whiteboard            | 432             | 4984          |
+------+-----------------------+-----------------+---------------+

sqlite> select * from scans where package_id = 384;
+----+-----------+------------+------------+--------+----------------------------+
| id | driver_id | package_id | address_id | action |         timestamp          |
+----+-----------+------------+------------+--------+----------------------------+
| 54 | 1         | 384        | 432        | Pick   | 2023-07-11 19:33:55.241794 |
| 94 | 1         | 384        | 854        | Drop   | 2023-07-11 23:07:04.432178 |
+----+-----------+------------+------------+--------+----------------------------+

sqlite> select * from addresses where id = 854;
+-----+-------------------+-------------+
| id  |      address      |    type     |
+-----+-------------------+-------------+
| 854 | 2 Finnigan Street | Residential |

-- *** The Devious Delivery ***
sqlite> select * from packages where from_address_id is null;
+------+---------------+-----------------+---------------+
|  id  |   contents    | from_address_id | to_address_id |
+------+---------------+-----------------+---------------+
| 5098 | Duck debugger | NULL            | 50            |

sqlite> select * from addresses where id = 50;
+----+-------------------+-------------+
| id |      address      |    type     |
+----+-------------------+-------------+
| 50 | 123 Sesame Street | Residential |

sqlite> select * from scans where package_id = 5098;
+-------+-----------+------------+------------+--------+----------------------------+
|  id   | driver_id | package_id | address_id | action |         timestamp          |
+-------+-----------+------------+------------+--------+----------------------------+
| 30123 | 10        | 5098       | 50         | Pick   | 2023-10-24 08:40:16.246648 |
| 30140 | 10        | 5098       | 348        | Drop   | 2023-10-24 10:08:55.610754 |
+-------+-----------+------------+------------+--------+----------------------------+

sqlite> select * from addresses where id = 348;
+-----+------------------+----------------+
| id  |     address      |      type      |
+-----+------------------+----------------+
| 348 | 7 Humboldt Place | Police Station |
+-----+------------------+----------------+

-- *** The Forgotten Gift ***

sqlite> select * from addresses where address = '728 Maple Place';
+------+-----------------+-------------+
|  id  |     address     |    type     |
+------+-----------------+-------------+
| 4983 | 728 Maple Place | Residential |

sqlite> select * from addresses where address = '109 Tileston Street';
+------+---------------------+-------------+
|  id  |       address       |    type     |
+------+---------------------+-------------+
| 9873 | 109 Tileston Street | Residential |
+------+---------------------+-------------+

sqlite> select * from packages where from_address_id = 9873 and to_address_id = 4983;
+------+----------+-----------------+---------------+
|  id  | contents | from_address_id | to_address_id |
+------+----------+-----------------+---------------+
| 9523 | Flowers  | 9873            | 4983          |

-- drop to wrong address_id of 7432 instead of 4983, so driver 17 re-picked it up
sqlite> select * from scans where package_id = 9523;
+-------+-----------+------------+------------+--------+----------------------------+
|  id   | driver_id | package_id | address_id | action |         timestamp          |
+-------+-----------+------------+------------+--------+----------------------------+
| 10432 | 11        | 9523       | 9873       | Pick   | 2023-08-16 21:41:43.219831 |
| 10500 | 11        | 9523       | 7432       | Drop   | 2023-08-17 03:31:36.856889 |
| 12432 | 17        | 9523       | 7432       | Pick   | 2023-08-23 19:41:47.913410 |
+-------+-----------+------------+------------+--------+----------------------------+

sqlite> select * from drivers where id = 11;
+----+--------+
| id |  name  |
+----+--------+
| 11 | Maegan |

sqlite> select * from drivers where id = 17;
+----+-------+
| id | name  |
+----+-------+
| 17 | Mikel |
+----+-------+
