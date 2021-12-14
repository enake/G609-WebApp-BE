from flaskr.db import get_db

class Files:
    def __init__(self):
        self.db = get_db()
    
    def __query(self, query, data=None):
        cursor = self.db.cursor()
        try: 
            result = list(cursor.execute(query, data))
            last_id = cursor.lastrowid
            self.db.commit()
            if (last_id):
                return last_id
            else:
                return result
        except Exception as e:
            print (e)
            return e

    def __query_to_dict(self, query, data=None):
        cursor = self.db.cursor()
        if (data):
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        self.db.commit()
        desc = cursor.description
        column_names = [col[0] for col in desc]
        result = [dict(zip(column_names, row))  
                        for row in cursor.fetchall()]
        return result

    def addFile(self, file_data):
        query = "INSERT INTO files (user_id, file_name) VALUES (?, ?);"
        return self.__query(query, file_data)

    def getFiles(self, user_id):
        query = f"SELECT * FROM files WHERE user_id = ?"
        return self.__query_to_dict(query, [user_id])
