import psycopg2
from models import Course, Users, Enrollment


msdb = psycopg2.connect(
    host='ec2-35-174-127-63.compute-1.amazonaws.com',
    database='d8lfqa1i6n1qrv',
    user='kzzrewbxspnwrp',
    port='5432',
    password='e94cbdbd523b32da7f854e25a9806ba4eac30968471341aef5f37da2a0858047',
)


# <--- Course DEFs beginning --->

def course_list():  # <- List Courses on Courses Page ->
    cursor = msdb.cursor()
    cursor.execute("ROLLBACK")
    cursor.execute(f"SELECT * FROM public.course")
    course = translate_courses(cursor.fetchall())
    return course


def course_find_id(category, id):  # <- ID finder to redirect to Course page ->
    cursor = msdb.cursor()
    cursor.execute("ROLLBACK")
    cursor.execute(f"SELECT * FROM public.{category} where id = {id}")
    find = cursor.fetchone()
    return Course(find[0], find[1])


def course_new(new_register):  # <- Register a new Course in the table ->
    try:
        if check_duplication('course', new_register, id=None) is True:
            return True
        else:
            cursor = msdb.cursor()
            cursor.execute("ROLLBACK")
            insert = f"INSERT INTO public.course (Name) VALUES (%s)"
            record = new_register
            cursor.execute(insert, (record,))
            msdb.commit()
    except:
        TryDBMessage.message()


def course_update(id, new_register):  # <- Update an existent Course ->
    try:
        if check_duplication('course', new_register, id) is True:
            return True
        else:
            cursor = msdb.cursor()
            cursor.execute("ROLLBACK")
            updating_query = f"UPDATE public.course SET name='{new_register}' WHERE id='{id}'"
            cursor.execute(updating_query)
            msdb.commit()
    except:
        TryDBMessage.message()

# <--- Course DEFs ending --->


# <--- Users DEFs beginning --->

def users_list():  # <- List Courses on Courses Page ->
    cursor = msdb.cursor()
    cursor.execute("ROLLBACK")
    cursor.execute(f"SELECT * FROM public.users")
    users = translate_users(cursor.fetchall())
    return users


def users_find_id(id):  # <- ID finder to redirect to Edit page ->
    cursor = msdb.cursor()
    cursor.execute("ROLLBACK")
    cursor.execute(f"SELECT * FROM public.users where id = {id}")
    find = cursor.fetchone()
    return Users(find[0], find[1], find[2], find[3], find[4], find[5])


def users_new(username, name, password, course, access_level):  # <- Register a new User in the table ->
    try:
        if check_duplication('users', username, id=None) is True:
            return True
        else:
            cursor = msdb.cursor()
            cursor.execute("ROLLBACK")
            insert = f"INSERT INTO public.users (USERNAME,NAME, PASSWORD, COURSE, ACCESS_LEVEL) values (%s, %s, %s, %s, %s)"
            cursor.execute(insert, (username, name, password, course, access_level))
            msdb.commit()
    except:
        TryDBMessage.message()


def users_update(id, new_username, new_register, access_level):  # <- Update an existent User ->
    try:
        if check_duplication('users', new_register, id) is True:
            return True
        else:
            cursor = msdb.cursor()
            cursor.execute("ROLLBACK")
            updating_query = f"UPDATE public.users SET USERNAME='{new_username}', NAME='{new_register}', ACCESS_LEVEL='{access_level}' WHERE id='{id}'"
            cursor.execute(updating_query)
            msdb.commit()
    except:
        TryDBMessage.message()


def users_password_update(id, new_password):  # <- Update User's password ->
    try:
        cursor = msdb.cursor()
        cursor.execute("ROLLBACK")
        updating_query = f"UPDATE public.users SET PASSWORD='{new_password}' WHERE id='{id}'"
        cursor.execute(updating_query)
        msdb.commit()
    except:
        TryDBMessage.message()


# <--- Users DEFs ending --->


# <--- Enrollment DEFs beginning --->

def enrollment_list():  # <- List Courses on Courses Page ->
    cursor = msdb.cursor()
    cursor.execute("ROLLBACK")
    cursor.execute(f"SELECT * FROM public.enrolled_courses")
    users = translate_enrollment(cursor.fetchall())
    return users


def insert_enrolled_courses(student_id, course_id):  # <- Insert Enrolled's Table ->
    student_id = int(student_id)
    course_id = int(course_id)
    try:
        cursor = msdb.cursor()
        cursor.execute("ROLLBACK")
        insert = f"INSERT INTO public.enrolled_courses (STUDENT_ID, COURSE_ID) values (%s, %s)"
        cursor.execute(insert, (student_id, course_id))
        msdb.commit()
    except:
        TryDBMessage.message()


def enrolled_find_user_id(id):  # <- ID finder to redirect to Edit page ->
    cursor = msdb.cursor()
    cursor.execute("ROLLBACK")
    cursor.execute(f"SELECT * FROM public.ENROLLED_COURSES where STUDENT_ID = {id}")
    find = translate_enrollment(cursor.fetchall())
    if find:
        return find


def enroled_deleting_by_id(student_id):  # <- ID finder to redirect to Edit page ->
    student_id = int(student_id)
    try:
        cursor = msdb.cursor()
        cursor.execute("ROLLBACK")
        deleting_query = f"DELETE FROM public.enrolled_courses WHERE STUDENT_ID={student_id}"
        cursor.execute(deleting_query)
        msdb.commit()
    except:
        TryDBMessage.message()


def enroled_deleting_by_course(course_id):  # <- ID finder to redirect to Edit page ->
    course_id = int(course_id)
    try:
        cursor = msdb.cursor()
        cursor.execute("ROLLBACK")
        deleting_query = f"DELETE FROM public.enrolled_courses WHERE COURSE_ID={course_id}"
        cursor.execute(deleting_query)
        msdb.commit()
    except:
        TryDBMessage.message()


# <--- Enrollment DEFs ending --->


#       <--- Supporting DEFs beginning --->
class DeletingDB:
    def __init__(self, category, item):   # <- Delete an Item on DB ->
        try:
            cursor = msdb.cursor()
            cursor.execute("ROLLBACK")
            deleting_query = f"DELETE FROM public.{category} WHERE id='{item}'"
            cursor.execute(deleting_query)
            msdb.commit()
            if category == 'users':
                enroled_deleting_by_id(item)
            elif category == 'course':
                enroled_deleting_by_course(item)
        except:
            TryDBMessage.message()


def check_duplication(category, item, id):   # <- Return the info if an Item exists into the table ->
    cursor = msdb.cursor()
    cursor.execute("ROLLBACK")
    name = 'name'
    if category == 'username':
        name = 'username'

    try:
        cursor.execute("ROLLBACK")
        consulting_query = f"SELECT {name} FROM public.{category} where {name} = '{item}'"
        cursor.execute(consulting_query)
        list = cursor.fetchall()

        consulting_query = f"SELECT {name} FROM public.{category} where {name} = '{item}' and id='{id}'"
        cursor.execute(consulting_query)
        list_sameID = cursor.fetchall()

        if list_sameID:
            pass
        elif list:
            return True
    except:
        TryDBMessage.message()


class FindId:
    def __init__(self, category, id):  # <- ID finder to redirect to Edit page ->
        self.cursor = msdb.cursor()
        self.cursor.execute("ROLLBACK")
        self.category = category
        self.id = id
        self.cursor.execute(f"SELECT * FROM public.{self.category} where id = {self.id}")
        self.find = self.cursor.fetchall()
        self.return_id()

    def return_id(self):
        if self.category == 'course':
            return translate_courses(self.find)
        elif self.category == 'users':
            return translate_users(self.find)


class TryDBMessage:
    @staticmethod
    def message():  # <- Raise an error on the log if the table isn't found ->
        return f'The connection with the database filed.\n' \
               f" Make sure you have executed the script 'db_script.sql' in MySQL."


# <--- Translating DB beginning --->

def translate_courses(course):  # <- Converts DB data (course) into Tuple ->
    def create_course_with_tuple(tuple):
        return Course(tuple[0], tuple[1])
    return list(map(create_course_with_tuple, course))


def translate_users(users):  # <- Converts DB data (users) into Tuple ->
    def create_users_with_tuple(tuple):
        return Users(tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5])
    return list(map(create_users_with_tuple, users))


def translate_enrollment(users):  # <- Converts DB data (enrollment) into Tuple ->
    def create_enrollment_with_tuple(tuple):
        return Enrollment(tuple[0], tuple[1])
    return list(map(create_enrollment_with_tuple, users))

# <--- Translating DB Ending --->


#       <--- Supporting DEFs ending --->


# <--- Authentication DEFs beginning --->

def authenticate(username):
    try:
        cursor = msdb.cursor()
        cursor.execute("ROLLBACK")
        cursor.execute(f"SELECT * FROM public.users where username = '{username}'")
        find = cursor.fetchone()
        return Users(find[0], find[1], find[2], find[3], find[4], find[5])
    except:
        TryDBMessage.message()


# <--- Authentication DEFs Ending --->
