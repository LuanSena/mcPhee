CREATE TABLE attributes (
 attribute_id CHAR(10) NOT NULL,
 name CHAR(10)
);

ALTER TABLE attributes ADD CONSTRAINT PK_attributes PRIMARY KEY (attribute_id);


CREATE TABLE message_board (
);


CREATE TABLE person (
 person_id INT NOT NULL,
 name VARCHAR(50),
 age INT,
 document VARCHAR(10) NOT NULL,
 attribute_id INT,
 address_name VARCHAR(500),
 address_number VARCHAR(10),
 address_complement VARCHAR(50),
 email VARCHAR(100),
 password VARCHAR(200),
 contact VARCHAR(100)
);

ALTER TABLE person ADD CONSTRAINT PK_person PRIMARY KEY (person_id);


CREATE TABLE school (
 schoolID INT NOT NULL,
 name VARCHAR(50),
 document VARCHAR(10)
);

ALTER TABLE school ADD CONSTRAINT PK_school PRIMARY KEY (schoolID);


CREATE TABLE student (
 student_id CHAR(10) NOT NULL,
 name CHAR(10),
 age CHAR(10),
 obs CHAR(10)
);

ALTER TABLE student ADD CONSTRAINT PK_student PRIMARY KEY (student_id);


CREATE TABLE student_owners (
 student_id CHAR(10) NOT NULL,
 person_document VARCHAR(10) NOT NULL
);

ALTER TABLE student_owners ADD CONSTRAINT PK_student_owners PRIMARY KEY (student_id,person_document);


CREATE TABLE class (
 class_id CHAR(10) NOT NULL,
 schoolID INT NOT NULL
);

ALTER TABLE class ADD CONSTRAINT PK_class PRIMARY KEY (class_id);


CREATE TABLE diary (
 diary_id INT NOT NULL,
 student_id CHAR(10) NOT NULL,
 date CHAR(10),
 text CHAR(10),
 status CHAR(10),
 feeding CHAR(10),
 other CHAR(10)
);

ALTER TABLE diary ADD CONSTRAINT PK_diary PRIMARY KEY (diary_id,student_id);


CREATE TABLE person_school (
 school_id INT NOT NULL,
 person_id INT NOT NULL,
 attribute_id CHAR(10) NOT NULL
);

ALTER TABLE person_school ADD CONSTRAINT PK_person_school PRIMARY KEY (school_id,person_id,attribute_id);


CREATE TABLE student_class (
 student_id CHAR(10) NOT NULL,
 class_id CHAR(10) NOT NULL
);

ALTER TABLE student_class ADD CONSTRAINT PK_student_class PRIMARY KEY (student_id,class_id);


ALTER TABLE person ADD CONSTRAINT FK_person_0 FOREIGN KEY (attribute_id) REFERENCES attributes (attribute_id);


ALTER TABLE student_owners ADD CONSTRAINT FK_student_owners_0 FOREIGN KEY (student_id) REFERENCES student (student_id);


ALTER TABLE class ADD CONSTRAINT FK_class_0 FOREIGN KEY (schoolID) REFERENCES school (schoolID);


ALTER TABLE diary ADD CONSTRAINT FK_diary_0 FOREIGN KEY (student_id) REFERENCES student (student_id);


ALTER TABLE person_school ADD CONSTRAINT FK_person_school_0 FOREIGN KEY (school_id) REFERENCES school (schoolID);
ALTER TABLE person_school ADD CONSTRAINT FK_person_school_1 FOREIGN KEY (person_id) REFERENCES person (person_id);
ALTER TABLE person_school ADD CONSTRAINT FK_person_school_2 FOREIGN KEY (attribute_id) REFERENCES attributes (attribute_id);


ALTER TABLE student_class ADD CONSTRAINT FK_student_class_0 FOREIGN KEY (student_id) REFERENCES student (student_id);
ALTER TABLE student_class ADD CONSTRAINT FK_student_class_1 FOREIGN KEY (class_id) REFERENCES class (class_id);


