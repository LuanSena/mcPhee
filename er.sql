CREATE TABLE attributes (
 attribute_id CHAR(10) NOT NULL PRIMARY KEY AUTOINCREMENT,
 name CHAR(10)
);


CREATE TABLE message_board (
);


CREATE TABLE person (
 person_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
 name VARCHAR(50),
 age INT,
 document VARCHAR(10) NOT NULL,
 attribute_id INT,
 address_name VARCHAR(500),
 address_number VARCHAR(10),
 address_complement VARCHAR(50),
 email VARCHAR(100),
 password VARCHAR(200),
 contact VARCHAR(100),

 FOREIGN KEY (attribute_id) REFERENCES attributes (attribute_id)
);


CREATE TABLE school (
 school_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
 full_name VARCHAR(60),
 fantasy_name VARCHAR(30),
 created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
 street VARCHAR(100),
 email VARCHAR(60),
 contact VARCHAR(30),
 document VARCHAR(20),
 owner_name VARCHAR(60),
 owner_attribute VARCHAR(60),
 owner_contact VARCHAR(60),

);

CREATE TABLE school_turns (
 school_turns_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
 school_id INTEGER NOT NULL,
 name VARCHAR(60),
 start_time VARCHAR(30),
 created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
 end_time VARCHAR(100),
 obs VARCHAR(60),
 FOREIGN KEY (school_id) REFERENCES school (school_id)
);


CREATE TABLE student (
 student_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
 name VARCHAR(50),
 grade varchar(25),
 born_date DATETIME,
 nacionality varchar(25),
 eating_obs varchar(250),
 obs varchar(250),
 created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE student_owners (
 student_id CHAR(10) NOT NULL,
 person_document VARCHAR(10) NOT NULL,

 PRIMARY KEY (student_id,person_document),

 FOREIGN KEY (student_id) REFERENCES student (student_id)
);


CREATE TABLE class (
 class_id CHAR(10) NOT NULL PRIMARY KEY AUTOINCREMENT,
 school_id INT NOT NULL,

 FOREIGN KEY (school_id) REFERENCES school (school_id)
);


CREATE TABLE diary (
 diary_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
 student_id INT NOT NULL,
 title VARCHAR(50),
 text BLOB,
 some_issue blooean,
 origin INT,
 diary_date DATETIME DEFAULT CURRENT_TIMESTAMP,
 diary_text BLOB,

 FOREIGN KEY (student_id) REFERENCES student (student_id)
);


CREATE TABLE person_school (
 school_id INT NOT NULL,
 person_id INT NOT NULL,
 attribute_id CHAR(10) NOT NULL,

 PRIMARY KEY (school_id,person_id,attribute_id),

 FOREIGN KEY (school_id) REFERENCES school (school_id),
 FOREIGN KEY (person_id) REFERENCES person (person_id),
 FOREIGN KEY (attribute_id) REFERENCES attributes (attribute_id)
);


CREATE TABLE student_class (
 student_id CHAR(10) NOT NULL,
 class_id CHAR(10) NOT NULL,

 PRIMARY KEY (student_id,class_id),

 FOREIGN KEY (student_id) REFERENCES student (student_id),
 FOREIGN KEY (class_id) REFERENCES class (class_id)
);

CREATE TABLE message (
 message_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
 receptor_id int,
 sender_id INT,
 send_date DATETIME DEFAULT CURRENT_TIMESTAMP,
 checked INT,
 checked_date DATETIME,
 message_title CHAR(50),
 message BLOB,

 FOREIGN KEY (receptor_id) REFERENCES person (person_id),
 FOREIGN KEY (sender_id) REFERENCES person (person_id)
);

