from ._base import PostgreDB
from models.users import Users


class UsersRepository:
    def List(self):
        db = PostgreDB()
        try:
            db.query(f"SELECT * FROM public.users")
            return self.__toList(db.fetchAll())
        except Exception as exp:
            print(exp)
        finally:
            db.close()

    def FindId(self, id):
        db = PostgreDB()
        try:
            db.query(f"SELECT * FROM public.users WHERE id = {id}")
            return self.__toOne(db.fetchOne())
        except Exception as exp:
            print(exp)
        finally:
            db.close()

    def New(self, username, name, access_level):
        db = PostgreDB()
        try:
            insert = f"INSERT INTO public.users(USERNAME, NAME, PASSWORD, COURSE, ACCESS_LEVEL) " \
                     f"VALUES (%s, %s, %s, %s, %s)"
            db.queryParams(insert, (username, name,'pass', 'false', access_level))
        except Exception as exp:
            print(exp)
        finally:
            db.close()

    def Update(self, id, new_username, new_name, new_accessLevel):
        db = PostgreDB()
        try:
            if self.checkDuplication(id) is True:
                return True
            else:
                updating_query = f"UPDATE public.users SET USERNAME=%s, NAME=%s, ACCESS_LEVEL=%s  WHERE id = {id}"
                db.queryParams(
                    updating_query, (new_username, new_name, new_accessLevel))
        except Exception as exp:
            print(exp)
        finally:
            db.close()

    def Delete(self, id):
        db = PostgreDB()
        try:
            db.query(f"DELETE FROM public.users WHERE id = {id}")
        except Exception as exp:
            print(exp)
        finally:
            db.close()

    def checkDuplication(self, item):  # <- Return the info if an Item exists into the table ->
        db = PostgreDB()
        try:
            db.query(f"SELECT name FROM public.users where username = '{item}'")
            return self.__toList(db.fetchAll())
        except Exception as exp:
            print(exp)
        finally:
            db.close()

    def PasswordUpdate(self, id, new_password):
        db = PostgreDB()
        try:
            updating_query = f"UPDATE public.users SET PASSWORD=%s WHERE id={id}"
            db.queryParams(
                updating_query, (new_password,))
        except Exception as exp:
            print(exp)
        finally:
            db.close()

    # Private Methods
    def __toList(self, users):
        def add(item):
            try:
                return self.__toOne(item)
            except Exception as exp:
                print(exp)

        try:
            return list(map(add, users))
        except Exception as exp:
            print(exp)

    def __toOne(self, item):
        try:
            return Users(item[0], item[1], item[2], item[3], item[4], item[5])
        except Exception as exp:
            print(exp)
