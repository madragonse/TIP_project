from datetime import date
import mysql.connector

db_IP = "192.168.1.56"


class TIPDb:

    def __init__(self):
        self.mydb = mysql.connector.connect(host=db_IP, user="home", password="Pudzian123", database="tipdb")

    def __del__(self):
        self.mydb.close()

    def create_db(self):
        mycursor = self.mydb.cursor()

        mycursor.execute('''create table if not exists user
                            (userId integer primary key AUTO_INCREMENT,
                            username varchar(15) unique not null, 
                            password varchar(64) not null,
                            email varchar(255) unique not null,
                            joined DATE not null
                            );''')
        mycursor.execute('''create table if not exists friends
                             (friendId integer primary key AUTO_INCREMENT,
                             user1 integer not null, 
                             user2 integer not null, 
                             state VARCHAR(3) NOT NULL,
                             FOREIGN KEY (user1) REFERENCES user(userId),
                             FOREIGN KEY (user2) REFERENCES user(userId)
                             );''')

        mycursor.close()

    def add_user(self, username, password, email):
        mycursor = self.mydb.cursor(buffered=False)

        sql_user = ("INSERT INTO user"
                    "(username, password, email, joined) "
                    "VALUES (%s, %s, %s, CURRENT_DATE())")

        data_user = (username, password, email)
        mycursor.execute(sql_user, data_user)
        self.mydb.commit()
        mycursor.close()

    def get_user_by_id(self, user_id):
        mycursor = self.mydb.cursor(buffered=False)

        sql_find = ("SELECT * FROM user WHERE user.userID = %s")

        data_find = (user_id,)
        mycursor.execute(sql_find, data_find)
        result = mycursor.fetchone()
        mycursor.close()
        return result

    def get_user_by_email(self, email):
        mycursor = self.mydb.cursor(buffered=False)

        sql_find = ("SELECT * FROM user WHERE user.email = %s")

        data_find = (email,)
        mycursor.execute(sql_find, data_find)
        result = mycursor.fetchone()
        mycursor.close()
        return result

    def get_user(self, username):
        mycursor = self.mydb.cursor(buffered=False)
        sql_find = ("SELECT * FROM user WHERE user.username = %s")

        data_find = (username,)
        mycursor.execute(sql_find, data_find)
        result = mycursor.fetchone()
        mycursor.close()
        return result

    def are_friends(self, user_id, friend_id):
        mycursor = self.mydb.cursor(buffered=False)
        sql_find = """SELECT state FROM friends WHERE (user1 = %s AND user2 = %s) OR (user1 = %s AND user2 = %s)"""
        print(sql_find)
        data_find = (str(user_id), str(friend_id), str(friend_id), str(user_id))
        mycursor.execute(sql_find, data_find)
        result = mycursor.fetchall()
        mycursor.close()
        return result

    # assumes that an valid friendship exists
    # returns true if inviter was the one that invited the invitee
    # false if other way around
    def did_user_invite(self, inviter, invitee):
        mycursor = self.mydb.cursor(buffered=False)
        sql_find = ("""SELECT state FROM friends
                              WHERE (user1 = %s AND user2 = %s)
                              """)

        data_find = (inviter, invitee)
        mycursor.execute(sql_find, data_find)
        result = mycursor.fetchone()
        mycursor.close()
        return result is not None

    def accept_friend(self, inviter, invitee):
        mycursor = self.mydb.cursor(buffered=False)
        sql_update = """UPDATE friends SET state = 'ACT' WHERE (user1 = %s AND user2 = %s) AND state = 'REQ'"""

        data_update = (inviter, invitee)
        mycursor.execute(sql_update, data_update)
        self.mydb.commit()
        mycursor.close()

    def decline_friend(self, user1, user2):
        mycursor = self.mydb.cursor(buffered=False)
        sql_update = """UPDATE friends SET state = 'DEC' WHERE (user1 = %s AND user2 = %s OR user1 = %s AND user2 = %s) AND state = 'REQ'"""

        data_update = (user1, user2, user2, user1)
        mycursor.execute(sql_update, data_update)
        self.mydb.commit()
        mycursor.close()

    def invite_friend(self, inviter_id, invetee_id):
        mycursor = self.mydb.cursor(buffered=False)
        sql_find = ("""INSERT INTO friends 
                       (user1,user2,state)
                        VALUES(%s,%s,'REQ')""")

        data_find = (inviter_id, invetee_id)
        mycursor.execute(sql_find, data_find)
        self.mydb.commit()
        mycursor.close()

    def remove_friends(self, user1, user2):
        mycursor = self.mydb.cursor(buffered=False)
        sql_find = ("""DELETE FROM Friends 
                       WHERE (user1 = %s AND user2 = %s)
                       OR (user1 = %s AND user2 = %s) """)

        data_find = (user1, user2, user2, user1)
        mycursor.execute(sql_find, data_find)
        self.mydb.commit()
        mycursor.close()

    def count_friends(self, user_id, state):
        mycursor = self.mydb.cursor(buffered=False)

        # sent requests
        if state == "SREQ":
            sql_find = ("""SELECT COUNT(t.friendId) FROM (SELECT friendId,user2 as user,state FROM Friends WHERE user1 = %s AND state = 'REQ') t""")
            data_find = (user_id,)

        # received requests
        elif state == "RREQ":
            sql_find = ("""SELECT COUNT(t.friendId) FROM (SELECT friendId,user1 as user,state FROM Friends WHERE user2 = %s AND state = 'REQ') t""")
            data_find = (user_id, )
        # all other (currently active/declined)
        else:
            sql_find = ("""SELECT COUNT(friendId) FROM (
                                   (SELECT friendId,user2 as user,state FROM Friends as f1
                                   WHERE user1 = %s AND state = %s)
                                   UNION
                                   (SELECT friendId,user1 as user,state FROM Friends as f2
                                   WHERE user2 = %s AND state = %s)) b
                                   """)
            data_find = (user_id, state, user_id, state)

        mycursor.execute(sql_find, data_find)
        result = mycursor.fetchall()
        mycursor.close()
        return result[0][0]

    def get_friends(self, user_id, state, start, end):
        mycursor = self.mydb.cursor(buffered=False)

        # sent requests
        if state == "SREQ":
            sql_find = ("""SELECT username,state FROM (
                           SELECT friendId,user2 as user,state FROM Friends as f1
                           WHERE user1 = %s AND state = 'REQ') b
                           INNER JOIN User u ON u.userId = b.user 
                           ORDER BY b.friendId
                           LIMIT %s,%s""")
            data_find = (user_id, start, end)
        # received requests
        elif state == "RREQ":
            sql_find = ("""SELECT username,state FROM (
                                     SELECT friendId,user1 as user,state FROM Friends as f1
                                     WHERE user2 = %s AND state = 'REQ') b
                                     INNER JOIN User u ON u.userId = b.user 
                                     ORDER BY b.friendId
                                     LIMIT %s,%s""")
            data_find = (user_id, start, end)
        # all other (currently active/declined)
        else:
            sql_find = ("""SELECT username,state FROM (
                            (SELECT friendId,user2 as user,state FROM Friends as f1
                            WHERE user1 = %s AND state = %s)
                            UNION
                            (SELECT friendId,user1 as user,state FROM Friends as f2
                            WHERE user2 = %s AND state = %s)) b
                            INNER JOIN User u ON u.userId = b.user 
                            ORDER BY b.friendId
                            LIMIT %s,%s""")
            data_find = (user_id, state, user_id, state, start, end)

        mycursor.execute(sql_find, data_find)
        result = mycursor.fetchall()
        mycursor.close()
        return result


# initialize DB if it has not yet been done
tempDB = TIPDb()
tempDB.create_db()
