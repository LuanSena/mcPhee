-- select person
select
     per.person_id,
     per.name,
     per.age,
     per.document,
     per.attribute_id as acess_level,
     per.address_name,
     per.address_number,
     per.address_complement,
     per.email,
     per.contact
from 
    person as per;
    

-- select schools per person
select
    person.person_id,
    person.name as person_name,
    school.name as school_name,
    school.document as school_document,
    school.schoolID,
    person_school.attribute_id as school_acess_level
from
    school, person_school, person
where
    person.person_id = :person_id and -- param
    person_school.person_id = person.person_id and
    person_school.school_id = school.schoolID;
    

-- select students per person
select
    student.student_id,
    student.name,
    student.age,
    student.obs,
    school.name as school_name,
    school.schoolID as school_id,
    student_class.class_id
from
    student, school, student_class, class, student_owners
where
    student_owners.person_document = '123456' and
    student.student_id = student_owners.student_id and
    student_class.student_id = student_owners.student_id and
    class.class_id = student_class.class_id and
    school.schoolID = class.school_id;
    
