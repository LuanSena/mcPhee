import time


def insert_person(db_conn, args):
    cursor = db_conn.cursor()
    query = '''
    INSERT INTO person(
            name,
            age,
            document,
            attribute_id,
            address_name,
            address_number,
            address_complement,
            email,
            contact)
    VALUES(
        '{name}',
         {age},
        '{document}',
         {attribute_id},
         '{address_name}',
         '{address_number}',
         '{address_complement}',
         '{email}',
         '{contact}'
         );
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
         per.address_number, per.address_complement, per.email, per.contact,
         per.full_name
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
    person["fullName"] = entry[10]

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
        student.student_id, student.name, cast(strftime('%Y.%m%d', 'now') - strftime('%Y.%m%d', born_date) as int) as age, student.obs, school.fantasy_name as school_name,
        school.school_id as school_id, student_class.class_id
    from
        student, school, student_class, class, student_owners
    where
        student_owners.person_document = {person_document} and
        student.student_id = student_owners.student_id and
        student_class.student_id = student_owners.student_id and
        class.class_id = student_class.class_id and
        school.school_id = class.school_id '''.format(person_document=person['document']))
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
            diary_id, diary.student_id, diary_date, text, stu.name as student_name, title, some_issue
        FROM 
            diary, student as stu
        WHERE
            diary.student_id = {student_id} AND
        stu.student_id = diary.student_id
        ORDER BY diary_date DESC
        LIMIT {size};'''.format(student_id=student_id, size=size))
    diarys = list()
    for row in cursor:
        diary = dict()
        diary["diaryId"] = row[0]
        diary["studentId"] = row[1]
        diary["diaryDate"] = row[2]
        diary["diaryText"] = row[3]
        diary["studentName"] = row[4]
        diary["title"] = row[5]
        diary["someIssue"] = row[6]
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


def get_student_by_id(db_conn, student_id):
    student = dict()
    cursor = db_conn.cursor()
    cursor.execute("""
        select
            student.student_id,
            student.name,
            cast(strftime('%Y.%m%d', 'now') - strftime('%Y.%m%d', born_date) as INT) as age,
            student.grade,
            student.nacionality,
            student.eating_obs,
            student.obs,
            student.created_at
        from
            student
        where student_id={student_id}
    """.format(student_id=student_id))
    for row in cursor:
        student["studentId"] = row[0]
        student["name"] = row[1]
        student["age"] = row[2]
        student["grade"] = row[3]
        student["nacionality"] = row[4]
        student["eatingObs"] = row[5]
        student["obs"] = row[6]
        student["createdAt"] = row[7]
    return student


def get_person_classes_by_id(db_conn, person_id):
    cursor = db_conn.cursor()
    cursor.execute('''
            SELECT 
                person_class.class_id,
                person_class.desc,
                class.name,
                school.school_id,
                school.fantasy_name
            FROM 
                person_class, class, school
            where 
                person_class.person_id = {person_id} AND
                class.class_id = person_class.class_id AND
                school.school_id = class.school_id
            
            ;'''.format(person_id=person_id))
    person_classes = list()

    for row in cursor:
        person_class = dict()
        person_class["classId"] = row[0]
        person_class["description"] = row[1]
        person_class["className"] = row[2]
        person_class["schoolId"] = row[3]
        person_class["schoolFantasyName"] = row[4]
        person_classes.append(person_class)
    return person_classes


def get_student_by_class_id(db_conn, class_id):
    cursor = db_conn.cursor()
    cursor.execute('''
            SELECT
                student_id, class_id
            FROM
                student_class
            WHERE class_id={class_id};'''.format(class_id=class_id))
    students = list()
    for row in cursor:
        student = dict()
        student["student_id"] = row[0]
        students.append(student)
    return students


def insert_diary(db_conn, student, diary_text, diary_title="Diário postado"):
    cursor = db_conn.cursor()
    query = '''
            INSERT INTO diary
                (student_id, title, "text", diary_date)
            VALUES({student_id}, '{diary_title}', '{diary_text}', '{date_time}');
'''.format(student_id=student, diary_text=diary_text, date_time=time.strftime("%Y-%m-%d %H:%M:%S"),
           diary_title=diary_title)
    cursor.execute(query)

    db_conn.commit()
    return True


def insert_school(db_conn, request):
    cursor = db_conn.cursor()
    query = """
        INSERT INTO school (
                full_name,
                fantasy_name,
                street,
                email,
                contact,
                document,
                owner_name,
                owner_attribute,
                owner_contact)
        VALUES(
                '{full_name}',
                '{fantasy_name}',
                '{address}',
                '{email}',
                '{contact}',
                '{document}',
                '{owner_name}',
                '{owner_attribute}',
                '{owner_contact}');

    """.format(full_name=request['fullName'],
               fantasy_name=request['fantasyName'],
               address=request['address'],
               email=request['email'],
               contact=request['contact'],
               document=request['document'],
               owner_name=request['ownerName'],
               owner_attribute=request['ownerAttribute'],
               owner_contact=request['ownerContact'])
    cursor.execute(query)

    db_conn.commit()
    return '0'


def get_managers(db_conn):
    cursor = db_conn.cursor()
    cursor.execute('''
                SELECT
                    person.person_id,
                    person.name,
                    person.document,
                    person.contact,
                    school.school_id,
                    school.fantasy_name
                from
                    person,
                    school,
                    person_school as ps
                WHERE
                    ps.person_id = person.person_id
                    and ps.school_id = school.school_id
                    and ps.attribute_id = 3;''')
    managers = list()
    for row in cursor:
        manager = dict()
        manager["managerId"] = row[0]
        manager["managerName"] = row[1]
        manager["managerDocument"] = row[2]
        manager["managerContact"] = row[3]
        manager["schoolId"] = row[4]
        manager["schoolName"] = row[5]
        managers.append(manager)
    return managers


def get_profs_by_school(db_conn, school_id):
    cursor = db_conn.cursor()
    cursor.execute('''
                SELECT
                    person.person_id,
                    person.name,
                    person.document,
                    person.contact,
                    person.email,
                    school.school_id,
                    school.fantasy_name
                from
                    person,
                    school,
                    person_school as ps
                WHERE
                    ps.person_id = person.person_id
                    and ps.school_id = school.school_id
                    and ps.attribute_id = 2
                    and ps.school_id = {school_id};'''.format(school_id=school_id))
    profs = list()
    for row in cursor:
        prof = dict()
        prof["personId"] = row[0]
        prof["personName"] = row[1]
        prof["personDocument"] = row[2]
        prof["personContact"] = row[3]
        prof["personEmail"] = row[4]
        prof["schoolId"] = row[5]
        prof["schoolName"] = row[6]
        profs.append(prof)
    return profs


def get_classes_by_school(db_conn, school_id):
    cursor = db_conn.cursor()
    cursor.execute('''
                    SELECT
                        class_id,
                        school_id,
                        name
                    FROM class
                    WHERE school_id = {school_id}
                    ;'''.format(school_id=school_id))
    classes = list()
    for row in cursor:
        class_entry = dict()
        class_entry["classId"] = row[0]
        class_entry["schoolId"] = row[1]
        class_entry["className"] = row[2]
        classes.append(class_entry)
    return classes


def get_students_by_schoool(db_conn, param):
    cursor = db_conn.cursor()
    cursor.execute('''
                SELECT
                    student.student_id,
                    student.name,
                    student.grade,
                    cast(strftime('%Y.%m%d', 'now') - strftime('%Y.%m%d', born_date) as INT) as age,
                    student.nacionality,
                    student.eating_obs,
                    student.obs,
                    student.created_at,
                    class.class_id,
                    class.name as class_name
                FROM
                    student,
                    student_class,
                    class,
                    school
                WHERE
                    student_class.student_id = student.student_id AND
                    school.school_id like '{}' AND
                    class.school_id = school.school_id AND
                    class.class_id = student_class.class_id;'''.format(param))
    students = list()
    for row in cursor:
        student = dict()
        student["studentId"] = row[0]
        student["studentName"] = row[1]
        student["studentGrade"] = row[2]
        student["studentAge"] = row[3]
        student["studentNacionality"] = row[4]
        student["studentEatingObs"] = row[5]
        student["studentObs"] = row[6]
        student["studentCreatedAt"] = row[7]
        student["classId"] = row[8]
        student["className "] = row[9]
        students.append(student)
    return students


def get_students_by_professional(db_conn, person_id):
    cursor = db_conn.cursor()
    cursor.execute('''
                    SELECT
                        s.student_id,
                        s.name,
                        s.grade,
                        cast(strftime('%Y.%m%d', 'now') - strftime('%Y.%m%d', born_date) as INT) as age,
                        s.nacionality,
                        s.eating_obs,
                        s.obs,
                        s.created_at
                    FROM
                        person as p,
                        person_class as pc,
                        student as s,
                        student_class as sc
                    WHERE
                        p.person_id = {} AND
                        pc.person_id = p.person_id and
                        sc.class_id =  pc.class_id AND
                        s.student_id = sc.student_id;'''.format(person_id))
    students = list()
    for row in cursor:
        student = dict()
        student["studentId"] = row[0]
        student["studentName"] = row[1]
        student["studentGrade"] = row[2]
        student["studentAge"] = row[3]
        student["studentNacionality"] = row[4]
        student["studentEatingObs"] = row[5]
        student["studentObs"] = row[6]
        student["studentCreatedAt"] = row[7]
        students.append(student)
    return students


def insert_manager(db_conn, person_document, school_id):
    cursor = db_conn.cursor()
    query = '''
        INSERT INTO person_school(
                person_id,
                school_id)
        VALUES(
                {person},
                {school}
             );
        '''.format(person=person_document,
                   school=school_id)
    print(query)
    cursor.execute(query)
    db_conn.commit()
    person = get_person_by_login(db_conn, args["email"], args["password"])
    return person['id']
