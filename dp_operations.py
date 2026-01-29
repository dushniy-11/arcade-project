import sqlite3


class Database:
    def __init__(self, username, count):
        self.username = username
        self.count = count
        self.connection = sqlite3.connect("users.db")

    def check_user(self):
        cursor = self.connection.cursor()
        check_result = cursor.execute("""SELECT * FROM players_info WHERE 
                player_name = ?""", (self.username,)).fetchone()
        if check_result:
            self.update_user()
        else:
            self.make_user()

    def make_user(self):
        cursor = self.connection.cursor()
        cursor.execute("""INSERT INTO players_info (player_name, last_count, max_count) VALUES (?, ?, ?)""",
                       (self.username, self.count, self.count))
        self.connection.commit()

    def update_user(self):
        cursor = self.connection.cursor()
        old_max_count = int(
            cursor.execute("""SELECT max_count FROM players_info WHERE player_name = ?""", (self.username,)).fetchone()[
                0])
        if self.count > old_max_count:
            update_max_count = self.count
        else:
            update_max_count = old_max_count
        cursor.execute("""UPDATE players_info SET last_count = ?, max_count = ? WHERE player_name = ?""",
                       (self.count, update_max_count, self.username))
        self.connection.commit()
