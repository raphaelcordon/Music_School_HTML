from ._base import PostgreDB
from models.enrollment import Enrollment


class EnrollmentRepository:
    def List(self):
        db = PostgreDB()
        try:
            db.query(f"SELECT * FROM public.enrolled_courses")
            return self.__toList(db.fetchAll())
        except Exception as exp:
            print(exp)
        finally:
            db.close()

    def FindUserId(self, id):
        db = PostgreDB()
        try:
            db.query(f"SELECT * FROM public.ENROLLED_COURSES where STUDENT_ID = {id}")
            return self.__toList(db.fetchAll())
        except Exception as exp:
            print(exp)
        finally:
            db.close()

    def New(self, student_id, course_id):
        db = PostgreDB()
        student_id = int(student_id)
        course_id = int(course_id)
        try:
            insert = f"INSERT INTO public.enrolled_courses (STUDENT_ID, COURSE_ID) " \
                     f"VALUES (%s, %s)"
            db.queryParams(insert, (student_id, course_id))
        except Exception as exp:
            print(exp)
        finally:
            db.close()

    def DeleteById(self, id):
        db = PostgreDB()
        student_id = int(id)
        try:
            db.query(f"DELETE FROM public.enrolled_courses WHERE STUDENT_ID={student_id}")
        except Exception as exp:
            print(exp)
        finally:
            db.close()

    def DeleteByCourse(self, id):
        db = PostgreDB()
        course_id = int(id)
        try:
            db.query(f"DELETE FROM public.enrolled_courses WHERE COURSE_ID={course_id}")
        except Exception as exp:
            print(exp)
        finally:
            db.close()

    # Private Methods
    def __toList(self, enroll):
        def add(item):
            try:
                return self.__toOne(item)
            except Exception as exp:
                print(exp)

        try:
            return list(map(add, enroll))
        except Exception as exp:
            print(exp)

    def __toOne(self, item):
        try:
            return Enrollment(item[0], item[1])
        except Exception as exp:
            print(exp)