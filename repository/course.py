from ._base import PostgreDB
from models.course import Course


class CourseRepository:

    def List(self):
        db = PostgreDB()
        try:
            db.query(f"SELECT * FROM public.course")
            return self.__toList(db.fetchAll())
        except Exception as exp:
            print(exp)
        finally:
            db.close()

    def ListPerName(self, name):
        db = PostgreDB()
        try:
            db.query(f"SELECT * FROM public.course where name = '{name}'")
            return self.__toList(db.fetchAll())
        except Exception as exp:
            print(exp)
        finally:
            db.close()

    def FindId(self, id):
        db = PostgreDB()
        try:
            db.query(f"SELECT * FROM public.course WHERE id = {id}")
            return self.__toOne(db.fetchOne())
        except Exception as exp:
            print(exp)
        finally:
            db.close()

    def New(self, new_register):
        db = PostgreDB()
        try:
            insert = f"INSERT INTO public.course(Name) VALUES (%s)"
            db.queryParams(insert, (new_register,))
        except Exception as exp:
            print(exp)
        finally:
            db.close()

    def Update(self, id, newCourseName):
        db = PostgreDB()
        try:
            updating_query = f"UPDATE public.course SET NAME=%s WHERE id = {id}"
            db.queryParams(
                updating_query, (newCourseName,))
        except Exception as exp:
            print(exp)
        finally:
            db.close()

    def Delete(self, id):
        db = PostgreDB()
        try:
            db.query(f"DELETE FROM public.course WHERE id = {id}")
        except Exception as exp:
            print(exp)
        finally:
            db.close()

    def checkDuplication(self, item):  # <- Return the info if an Item exists into the table ->
        db = PostgreDB()
        try:
            db.query(f"SELECT name FROM public.course where name = '{item}'")
            return self.__toList(db.fetchAll())
        except Exception as exp:
            print(exp)
        finally:
            db.close()

    # Private Methods
    def __toList(self, course):
        def add(item):
            try:
                return self.__toOne(item)
            except Exception as exp:
                print(exp)

        try:
            return list(map(add, course))
        except Exception as exp:
            print(exp)

    def __toOne(self, item):
        try:
            return Course(item[0], item[1])
        except Exception as exp:
            print(exp)