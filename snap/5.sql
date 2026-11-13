select friend_id from friends where user_id = (
    select id from users where username = 'lovelytrust487'
)
intersect
select friend_id from friends where user_id = (
    select id from users where username = 'exceptionalinspiration482'
);

