-- alter the password of the admin account to be 'oops!'
update users set password = '982c0381c279d139fd221fce974916e7' where username = 'admin';

-- erase logs of the above password changes
delete from user_logs where type='update' and new_password = '982c0381c279d139fd221fce974916e7';

-- add false data to user_logs as if admin account has password updated to emily33's password.
insert into user_logs (type, old_username, new_username, old_password, new_password)
select 'update', 'admin', 'admin', 'e10adc3949ba59abbe56e057f20f883e', (select password from users where username = 'emily33');
