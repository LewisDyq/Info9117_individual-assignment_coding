drop table if exists users;
create table users(
  username text primary key,
  password text not null
);
insert into users values('admin', 'admin');
insert into users values('Lewis', '601601');
insert into users values('test', 'test123');

