insert into role (id, name, role_permission) values (1, 'admin', 0x7);
insert into role (id, name, role_permission) values (2, 'user', 0x1);
insert into users (id, username, password, role_id, account_permission) values (1, 'admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 1, 0);