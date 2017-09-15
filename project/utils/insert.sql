insert into USER(username, document, addressNumber) values("Ablon", "1123685", "777");
insert into PROFESSIONAL(userID, occupation) values (1, "Manager");
insert into LOGIN(userID, emailaddress, password) values(1, "foo@bla.com", "None");
insert into ADDRESS(cep, city, state, name, adjunct) values("21235505", "Rio de janeiro", "RJ", "Street of fools", "None");
insert into ADDRESS_USER values(1, 1);
insert into CONTACT(userID, type, contact_type, contact) values(1, "Phone", "What", "000000000");
insert into CONTACT(userID, type, contact_type, contact) values(1, "Mail", "What", "foo@bla.com");