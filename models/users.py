class Users:
    def __init__(self, id, username, name, password, course, access_level):
        self.id = id
        self.username = username
        self.name = name
        self.password = password
        self.course = course
        self.access_level = access_level


class Edit_Users_Access_Level:
    def __init__(self, id, username, name, access_level):
        self.id = id
        self.username = username
        self.name = name
        self.access_level = access_level


class Edit_Users_Pass:
    def __init__(self, id, password):
        self.id = id
        self.password = password
