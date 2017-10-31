def insert_person(db_conn, args):
    cursor = db_conn.cursor()
    query = '''
    INSERT INTO
        person(name, age, document, attribute_id, address_name, address_number, address_complement, email, contact)
    VALUES('{name}', {age}, '{document}', {attribute_id}, '{address_name}', '{address_number}', '{address_complement}', '{email}', '{contact}');
    '''.format(name=args["name"],
               age=args["age"],
               document=args["document"],
               attribute_id=args["attributeId"],
               address_name=args["addressName"],
               address_number=args["addressNumber"],
               address_complement=args["addressComplement"],
               email=args["email"],
               contact=args["contact"])
    print(query)
    cursor.execute(query)
    db_conn.commit()
    person = get_person_by_login(db_conn, args["email"], args["password"])
    return person['id']


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
    person["attribute"] = entry[4]
    person["addressName"] = entry[5]
    person["addressNumber"] = entry[6]
    person["addressComplement"] = entry[7]
    person["email"] = entry[8]
    person["contact"] = entry[9]

    # GET SCHOOLS
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

    # GET STUDENTS
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

    # GET UNREAD TOP 5 MESSAGES
    person["messages"] = get_person_unread_messages(db_conn, person_id, 5)
    return person


def get_person_unread_messages(db_conn, person_id, size=5):
    cursor = db_conn.cursor()
    cursor.execute('''
    select
        message_id, receptor_id, sender_id, person.name as sender_name, send_date, checked, checked_date, message 
    from
        message, person
    where
        sender_id=person.person_id AND
        receptor_id={person_id}
    LIMIT {size};'''.format(person_id=person_id, size=size))
    messages = list()
    for row in cursor:
        message = dict()
        message["messageId"] = row[0]
        message["senderName"] = row[3]
        message["sendDate"] = row[4]
        message["checked"] = row[5]
        message["checkedDate"] = row[6]
        message["message"] = row[7]
        messages.append(message)
    return messages


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
        return False


# conn = sqlite3.connect("/home/luan/workspace/mcPhee/new_mcphee.sqlite")
# # print(get_person_by_id(conn, 4))
# print(get_person_by_login(conn, "66666", "ADMIN"))
def get_persons(db_conn):
    persons = list()
    cursor = db_conn.cursor()
    cursor.execute("select person_id from person")
    for row in cursor:
        person = get_person_by_id(db_conn, row[0])
        persons.append(person)

    return persons
