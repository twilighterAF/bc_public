import sqlite3

class DataBase:

    def get_user(self, user_id):
        try:
            self.__cur.execute(f'SELECT * FROM users WHERE id = {user_id} LIMIT 1')
            res = self.__cur.fetchone()
            if not res:
                return False

            return res
        except sqlite3.Error as e:
            print(f'DB fetch error - {e}')

        return False

    def get_user_by_login(self, login):
        try:
            self.__cur.execute(f'SELECT * FROM users WHERE id = {login} LIMIT 1')
            res = self.__cur.fetchone()
            if not res:
                return False

            return res
        except sqlite3.Error as e:
            print(f'DB fetch error - {e}')