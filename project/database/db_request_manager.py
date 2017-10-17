import sqlite3


def insert_person(*args):
    pass


def get_person_by_id(db_conn, person_id):
    cursor = db_conn.cursor()
    cursor.execute('''
    select
         per.person_id, per.name, per.age, per.document, per.attribute_id as acess_level, per.address_name,
         per.address_number, per.address_complement, per.email, per.contact
    from 
         person as per
    where 
         per.person_id = {person_id}'''.format(person_id=person_id))

    person = dict()

    entry = cursor.fetchone()
    person['id'] = entry[0]
    person['name'] = entry[1]
    person["age"] = entry[2]
    person["document"] = entry[3]
    person["atribute"] = entry[4]
    person["addressName"] = entry[5]
    person["addresNumber"] = entry[6]
    person["addressComplement"] = entry[7]
    person["email"] = entry[8]
    person["contact"] = entry[9]

    cursor.execute('''
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
            person.person_id = {person_id} and
            person_school.person_id = person.person_id and
            person_school.school_id = school.schoolID'''.format(person_id=person_id))
    schools = list()
    for row in cursor:
        school = dict()
        school["school_name"] = row[2]
        school["school_id"] = row[4]
        school["school_acess"] = row[5]
        schools.append(school)
    person["schools"] = schools

    cursor.execute('''
    select
        student.student_id, student.name, student.age, student.obs, school.name as school_name,
        school.schoolID as school_id, student_class.class_id
    from
        student, school, student_class, class, student_owners
    where
        student_owners.person_document = {person_document} and
        student.student_id = student_owners.student_id and
        student_class.student_id = student_owners.student_id and
        class.class_id = student_class.class_id and
        school.schoolID = class.schoolID '''.format(person_document=person['document']))

    students = list()
    for row in cursor:
        student = dict()
        student["student_id"] = row[0]
        student["name"] = row[1]
        student["age"] = row[2]
        student["obs"] = row[3]
        student["school_name"] = row[4]
        student["school_id"] = row[5]
        student["class_id"] = row[6]
        students.append(student)
    person["students"] = students
    return person


def get_person_by_login(db_conn, user, password):
    cursor = db_conn.cursor()
    cursor.execute('''
    SELECT 
        * 
    FROM
        person
    WHERE 
        (email = '{user}' AND password = '{password}') OR
        (document = '{user}' and password = '{password}')'''.format(user=user,
                                                                    password=password))

    entry = cursor.fetchone()
    if entry:
        return get_person_by_id(db_conn, entry[0])
    else:
        return "False"


conn = sqlite3.connect("/home/luan/workspace/mcPhee/new_mcphee.sqlite")
# print(get_person_by_id(conn, 4))
print(get_person_by_login(conn, "66666", "ADMIN"))
