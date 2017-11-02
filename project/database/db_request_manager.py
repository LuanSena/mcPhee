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
            school.fantasy_name as school_name,
            school.document as school_document,
            school.school_id,
            person_school.attribute_id as school_acess_level
        from
            school, person_school, person
        where
            person.person_id = {person_id} and
            person_school.person_id = person.person_id and
            person_school.school_id = school.school_id'''.format(person_id=person_id))
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
        student.student_id, student.name, student.age, student.obs, school.fantasy_name as school_name,
        school.school_id as school_id, student_class.class_id
    from
        student, school, student_class, class, student_owners
    where
        student_owners.person_document = {person_document} and
        student.student_id = student_owners.student_id and
        student_class.student_id = student_owners.student_id and
        class.class_id = student_class.class_id and
        school.school_id = class.schoolid '''.format(person_document=person['document']))
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
        student["diarys"] = get_student_diary_by_id(db_conn, student["student_id"])
        students.append(student)
    person["students"] = students

    # GET UNREAD TOP 5 MESSAGES
    person["messages"] = get_person_unread_messages(db_conn, person_id, 5)
    return person


def get_person_unread_messages(db_conn, person_id, size=5):
    cursor = db_conn.cursor()
    cursor.execute('''
    select
        message_id, receptor_id, sender_id, person.name as sender_name, send_date, checked, checked_date, message, message_title 
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
        message["messageTitle"] = row[8]
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


def get_student_diary_by_id(db_conn, student_id, size=5):
    cursor = db_conn.cursor()
    cursor.execute('''
        SELECT 
            diary_id, diary.student_id, diary_date, diary_text, stu.name as student_name
        FROM 
            diary, student as stu
        WHERE
            diary.student_id = {student_id} AND
        stu.student_id = diary.student_id
        LIMIT {size};'''.format(student_id=student_id, size=size))
    diarys = list()
    for row in cursor:
        diary = dict()
        diary["diaryId"] = row[0]
        diary["studentId"] = row[1]
        diary["diaryDate"] = row[2]
        diary["diaryText"] = row[3]
        diary["studentName"] = row[4]
        diarys.append(diary)
    return diarys


def get_persons(db_conn):
    persons = list()
    cursor = db_conn.cursor()
    cursor.execute("select person_id from person")
    for row in cursor:
        person = get_person_by_id(db_conn, row[0])
        persons.append(person)

    return persons


def get_school_by_id(db_conn, school_id):
    cursor = db_conn.cursor()
    cursor.execute('''
        select 
            school_id,
            full_name,
            fantasy_name,
            created_at,
            street,
            email,
            contact,
            document,
            owner_name,
            owner_attribute,
            owner_contact
        from
            school
        where school_id = {school_id};'''.format(school_id=school_id))
    school = dict()
    for row in cursor:
        school["schoolId"] = row[0]
        school["fullName"] = row[1]
        school["fantasyName"] = row[2]
        school["createdAt"] = row[3]
        school["street"] = row[4]
        school["email"] = row[5]
        school["contact"] = row[6]
        school["document"] = row[7]
        school["ownerName"] = row[8]
        school["ownerAttribute"] = row[9]
        school["ownerContact"] = row[10]
    return school


def get_school_turns_by_id(db_conn, school_id):
    cursor = db_conn.cursor()
    cursor.execute('''
        select 
            school_turns_id,
            name,
            start_time,
            end_time,
            obs
        from
            school_turns
        where school_id = {school_id};'''.format(school_id=school_id))
    school_turns = list()

    for row in cursor:
        school_turn = dict()
        school_turn["schoolTurnsId"] = row[0]
        school_turn["name"] = row[1]
        school_turn["startTime"] = row[2]
        school_turn["endTime"] = row[3]
        school_turn["obs"] = row[4]
        school_turns.append(school_turn)
    return school_turns


def get_schools(db_conn):
    schools = list()
    cursor = db_conn.cursor()
    cursor.execute("select school_id from school")
    for row in cursor:
        school = get_school_by_id(db_conn, row[0])
        schools.append(school)

    return schools
