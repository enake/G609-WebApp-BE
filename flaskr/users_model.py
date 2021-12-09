from flaskr.db import get_db

class Users:
    def __init__(self):
        self.db = get_db()

    def __query(self, query, data=None):
        cursor = self.db.cursor()
        try: 
            result = list(cursor.execute(query, data))
            self.db.commit()
            return result
        except Exception as e:
            return e

    def __query_to_dict(self, query, data):
        cursor = self.db.cursor()
        cursor.execute(query, data)
        self.db.commit()
        desc = cursor.description
        column_names = [col[0] for col in desc]
        result = [dict(zip(column_names, row))  
                        for row in cursor.fetchall()]
        return result

    def getUsers(self):
        query = "select * from users"
        return self.__query_to_dict(query)

    def getUserByEmail(self, email=None):
        query = "SELECT * FROM users WHERE email = ?;"
        return self.__query_to_dict(query, email)

    def getUserByEmailPassword(self, user_data):
        query = "SELECT * FROM users WHERE email =? AND password =?"
        return self.__query_to_dict(query, user_data)

    def addUser(self, user_data):
        query = """INSERT INTO users (email, first_name, last_name, password)
    VALUES (?, ?, ?, ?);"""
        return self.__query(query, user_data)

