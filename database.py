import datetime
import sqlite3
from termcolor import colored
import zipfile
from datetime import date
from datetime import datetime
import string
import re

databaseName = 'mycompany.db'

class database:
    def __init__(self):
        self.loggedin_user = None

    def Login(self):
        self.loginName = input('Name: ')
        self.loginPassword = input('Password: ')

        if self.loginName == 'superadmin' and self.loginPassword == 'Admin!23':
            print('logged in as superadmin')
        else:
            self.conn = sqlite3.connect(databaseName) 
            self.cur = self.conn.cursor()
            self.cur.execute("SELECT * from users WHERE username=:username AND password=:password", {"username": database.encrypt(3, self.loginName), "password": database.encrypt(3, self.loginPassword)})
            self.loggedin_user = self.cur.fetchone()
            self.conn.commit()
            self.conn.close()
        database.menu(self.loggedin_user, self.loginName, self.loginPassword)

    def createDbIfNotExist():
        conn = sqlite3.connect(databaseName) 
        cur = conn.cursor()

        tb_create = "CREATE TABLE client (person_id INTEGER PRIMARY KEY, fullname TEXT, address TEXT, emailaddress TEXT, phonenumber TEXT)"
        try:
            cur.execute(tb_create)
            conn.commit()
        except: 
            None

        tb_create = "CREATE TABLE users (user_id INTEGER PRIMARY KEY, username TEXT, password TEXT, fullname TEXT, admin INT, advisor INT);"
        try:
            cur.execute(tb_create)
            conn.commit()
        except: 
            None

        tb_create = "CREATE TABLE logs (username TEXT, date TEXT, time TEXT, description TEXT, information TEXT, suspicious TEXT);"
        try:
            cur.execute(tb_create)
            conn.commit()
        except: 
            None
        
        conn.close()

    def show_all_clients():
        conn = sqlite3.connect(databaseName) 
        cur = conn.cursor()
        cur.execute("SELECT * from client")
        allClients = cur.fetchall()
        clear = "\n" * 100
        print(clear)
        print("-----allClients-----")
        for row in allClients:
            print("ID: " + str(row[0]) + " Fullname: " + database.decrypt(3, row[1]) + " Address: " + database.decrypt(3, row[2]) + " Emailaddress: " + database.decrypt(3, row[3]) + " Phonenumber: " + database.decrypt(3, row[4]))
        print("\n")
        conn.commit()
        conn.close()

    def show_all_users():
        conn = sqlite3.connect(databaseName) 
        cur = conn.cursor()
        cur.execute("SELECT * from users")
        allUsers = cur.fetchall()
        clear = "\n" * 100
        print(clear)
        print("-----allUsers-----")
        for row in allUsers:
            print("ID: " + str(row[0]) + " Username: " + database.decrypt(3, row[1]) + " Password: " + database.decrypt(3, row[2]) + " Fullname: " + database.decrypt(3, row[3]) + " Admin: " + str(row[4]) + " Advisor: " + str(row[5]))
        print("\n")
        conn.commit()
        conn.close()
    
    def add_new_client(loginname):
        fullname = input('fullname: ')
        streetname = input('streetname: ')
        housenumber = input('housenumber: ')
        zipcode = input('zipcode: ')
        print('Choose a city')
        print('Amsterdam', 'Rotterdam', 'Utrecht', 'Den Haag', 'Maastricht', 'Nijmegen', 'Deventer', 'Groningen', 'Almere', 'Delft')
        city = input('city: ')
        emailaddress = input('emailaddress: ')
        phonenumber = input('phonenumber: +31 6')

        clientCheck = database.checkClientInfo(fullname, streetname, housenumber, zipcode, city.lower(), emailaddress, phonenumber)
        while clientCheck[1] != True:
            print(clientCheck[0])
            fullname = input('fullname: ')
            streetname = input('streetname: ')
            housenumber = input('housenumber: ')
            zipcode = input('zipcode: ')
            print('Choose a city')
            print('Amsterdam', 'Rotterdam', 'Utrecht', 'Den Haag', 'Maastricht', 'Nijmegen', 'Deventer', 'Groningen', 'Almere', 'Delft')
            city = input('city: ')
            emailaddress = input('emailaddress: ')
            phonenumber = input('phonenumber: +31 6')
            clientCheck = database.checkClientInfo(fullname, streetname, housenumber, zipcode, city.lower(), emailaddress, phonenumber)

        today = date.today().strftime("%d/%m/%Y")
        time = datetime.now().strftime("%H:%M:%S")
        address = streetname + ' ' + housenumber + ', ' + zipcode + ' ' + city
        conn = sqlite3.connect(databaseName) 
        cur = conn.cursor()
        cur.execute("INSERT INTO client VALUES (NULL, ?, ?, ?, ?)", [database.encrypt(3, fullname), database.encrypt(3, address), database.encrypt(3, emailaddress), database.encrypt(3, phonenumber)])
        print('Added new client succesfully')
        cur.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?)", [database.encrypt(3, loginname), today, time, database.encrypt(3, 'New client is created'), database.encrypt(3, 'Client ' + fullname + ' has been created'), 'No'])
        conn.commit()
        conn.close()

    def add_new_advisor(loginname):
        username = input('username: ')
        userCheck = database.checkUsername(username)
        while userCheck[1] != True:
            print(userCheck[0])
            username = input('username: ')
            userCheck = database.checkUsername(username)

        password = input('password: ')
        passCheck = database.checkPassword(password)
        while passCheck[1] != True:
            print(passCheck[0])
            password = input('password: ')
            passCheck = database.checkPassword(password)

        fullname = input('fullname: ')
        fullnameCheck = database.checkFullname(fullname)
        while fullnameCheck[1] != True:
            print(fullnameCheck[0])
            fullname = input('fullname: ')
            fullnameCheck = database.checkFullname(fullname)

        today = date.today().strftime("%d/%m/%Y")
        time = datetime.now().strftime("%H:%M:%S")
        conn = sqlite3.connect(databaseName) 
        cur = conn.cursor()
        cur.execute("INSERT INTO users VALUES (NULL, ?, ?, ?, ?, ?)", [database.encrypt(3, username), database.encrypt(3, password), database.encrypt(3, fullname), 0, 1])
        print('Added new advisor succesfully')
        cur.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?)", [database.encrypt(3, loginname), today, time, database.encrypt(3, 'New advisor is created'), database.encrypt(3, 'User: ' + username + ' has been created'), 'No'])
        conn.commit()
        conn.close()

    def add_new_admin(loginname):
        username = input('username: ')
        userCheck = database.checkUsername(username)
        while userCheck[1] != True:
            print(userCheck[0])
            username = input('username: ')
            userCheck = database.checkUsername(username)
        
        password = input('password: ')
        passCheck = database.checkPassword(password)
        while passCheck[1] != True:
            print(passCheck[0])
            password = input('password: ')
            passCheck = database.checkPassword(password)

        fullname = input('fullname: ')
        fullnameCheck = database.checkFullname(fullname)
        while fullnameCheck[1] != True:
            print(fullnameCheck[0])
            fullname = input('fullname: ')
            fullnameCheck = database.checkFullname(fullname)

        today = date.today().strftime("%d/%m/%Y")
        time = datetime.now().strftime("%H:%M:%S")
        conn = sqlite3.connect(databaseName) 
        cur = conn.cursor()
        cur.execute("INSERT INTO users VALUES (NULL, ?, ?, ?, ?, ?)", [database.encrypt(3, username), database.encrypt(3, password), database.encrypt(3, fullname), 1, 0])
        print('Added new admin succesfully')
        cur.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?)", [database.encrypt(3, loginname), today, time, database.encrypt(3, 'New admin is created'), database.encrypt(3, 'User: ' + username + ' has been created'), 'No'])
        conn.commit()
        conn.close()

    def update_client(loginname):
        person_id = input('personid: ')
        fullname = input('new fullname: ')
        streetname = input('new streetname: ')
        housenumber = input('new housenumber: ')
        zipcode = input('new zipcode: ')
        print('Choose a city')
        print('Amsterdam', 'Rotterdam', 'Utrecht', 'Den Haag', 'Maastricht', 'Nijmegen', 'Deventer', 'Groningen', 'Almere', 'Delft')
        city = input('new city: ')
        emailaddress = input('new emailaddress: ')
        phonenumber = input('new phonenumber: +31 6')

        clientCheck = database.checkClientInfo(fullname, streetname, housenumber, zipcode, city, emailaddress, phonenumber)
        while clientCheck[1] != True:
            print(clientCheck[0])
            fullname = input('new fullname: ')
            streetname = input('new streetname: ')
            housenumber = input('new housenumber: ')
            zipcode = input('new zipcode: ')
            print('Choose a city')
            print('Amsterdam', 'Rotterdam', 'Utrecht', 'Den Haag', 'Maastricht', 'Nijmegen', 'Deventer', 'Groningen', 'Almere', 'Delft')
            city = input('new city: ')
            emailaddress = input('new emailaddress: ')
            phonenumber = input('new phonenumber: +31 6')
            clientCheck = database.checkClientInfo(fullname, streetname, housenumber, zipcode, city, emailaddress, phonenumber)

        today = date.today().strftime("%d/%m/%Y")
        time = datetime.now().strftime("%H:%M:%S")
        address = streetname + ' ' + housenumber + ', ' + zipcode + ' ' + city
        conn = sqlite3.connect(databaseName) 
        cur = conn.cursor()
        cur.execute("SELECT fullname from client WHERE (person_id=:person_id)", {"person_id": person_id})
        updateClient = cur.fetchone()
        if updateClient != None:
            updateClient = ''.join(updateClient)
            cur.execute("UPDATE client Set fullname=:fullname, address=:address, emailaddress=:emailaddress, phonenumber=:phonenumber WHERE person_id=:person_id", {"person_id": person_id, "fullname": database.encrypt(3, fullname), "address": database.encrypt(3, address), "emailaddress": database.encrypt(3, emailaddress), "phonenumber": database.encrypt(3, phonenumber)})
            print('updated client succesfully')
            cur.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?)", [database.encrypt(3, loginname), today, time, database.encrypt(3, 'Client updated'), database.encrypt(3, 'Client: ' + database.decrypt(3, updateClient) + ' has been updated'), 'No'])
        conn.commit()
        conn.close()

    def update_advisor(loginname):
        user_id = input('user_id: ')
        username = input('new username: ')
        userCheck = database.checkUsername(username)
        while userCheck[1] != True:
            print(userCheck[0])
            username = input('new username: ')
            userCheck = database.checkUsername(username)
        
        password = input('new password: ')
        passCheck = database.checkPassword(password)
        while passCheck[1] != True:
            print(passCheck[0])
            password = input('new password: ')
            passCheck = database.checkPassword(password)

        fullname = input('new fullname: ')
        fullnameCheck = database.checkFullname(fullname)
        while fullnameCheck[1] != True:
            print(fullnameCheck[0])
            fullname = input('new fullname: ')
            fullnameCheck = database.checkFullname(fullname)

        advisor = input('advisor: ')
        advisorCheck = database.checkAdvisorRole(advisor)
        while advisorCheck[1] != True:
            print(advisorCheck[0])
            advisor = input('advisor: ')
            advisorCheck = database.checkAdvisorRole(advisor)
        
        today = date.today().strftime("%d/%m/%Y")
        time = datetime.now().strftime("%H:%M:%S")
        conn = sqlite3.connect(databaseName) 
        cur = conn.cursor()
        cur.execute("SELECT username from users WHERE user_id=:user_id AND advisor='1'", {"user_id": user_id})
        updateAdvisor = cur.fetchone()
        if updateAdvisor != None:
            updateAdvisor = ''.join(updateAdvisor)
            cur.execute("UPDATE users Set username=:username, password=:password, fullname=:fullname, advisor=:advisor WHERE user_id=:user_id", {"user_id":user_id, "username": database.encrypt(3, username), "password": database.encrypt(3, password), "fullname": database.encrypt(3, fullname), "advisor":advisor})
            print('updated advisor succesfully')
            cur.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?)", [database.encrypt(3, loginname), today, time, database.encrypt(3, 'Advisor updated'), database.encrypt(3, 'User: ' + database.decrypt(3, updateAdvisor) + ' has been updated'), 'No'])
        conn.commit()
        conn.close()

    def update_admin(loginname):
        user_id = input('user_id: ')
        username = input('new username: ')
        userCheck = database.checkUsername(username)
        while userCheck[1] != True:
            print(userCheck[0])
            username = input('username: ')
            userCheck = database.checkUsername(username)
        
        password = input('new password: ')
        passCheck = database.checkPassword(password)
        while passCheck[1] != True:
            print(passCheck[0])
            password = input('new password: ')
            passCheck = database.checkPassword(password)

        fullname = input('new fullname: ')
        fullnameCheck = database.checkFullname(fullname)
        while fullnameCheck[1] != True:
            print(fullnameCheck[0])
            fullname = input('new fullname: ')
            fullnameCheck = database.checkFullname(fullname)

        admin = input('admin: ')
        adminCheck = database.checkAdvisorRole(admin)
        while adminCheck[1] != True:
            print(adminCheck[0])
            admin = input('admin: ')
            adminCheck = database.checkAdvisorRole(admin)
        
        today = date.today().strftime("%d/%m/%Y")
        time = datetime.now().strftime("%H:%M:%S")
        conn = sqlite3.connect(databaseName) 
        cur = conn.cursor()
        cur.execute("SELECT username from users WHERE user_id=:user_id AND admin='1'", {"user_id": user_id})
        updateAdmin = cur.fetchone()
        if updateAdmin != None:
            updateAdmin = ''.join(updateAdmin)
            cur.execute("UPDATE users Set username=:username, password=:password, fullname=:fullname, admin=:admin WHERE user_id=:user_id", {"user_id":user_id, "username": database.encrypt(3, username), "password": database.encrypt(3, password), "fullname": database.encrypt(3, fullname), "admin":admin})
            print('updated admin succesfully')
            cur.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?)", [database.encrypt(3, loginname), today, time, database.encrypt(3, 'Admin updated'), database.encrypt(3, 'User: ' + database.decrypt(3, updateAdmin) + ' has been updated'), 'No'])
        conn.commit()
        conn.close()

    def update_user(loginname):
        user_id = input('user_id: ')
        username = input('new username: ')
        userCheck = database.checkUsername(username)
        while userCheck[1] != True:
            print(userCheck[0])
            username = input('username: ')
            userCheck = database.checkUsername(username)
            
        password = input('new password: ')
        passCheck = database.checkPassword(password)
        while passCheck[1] != True:
            print(passCheck[0])
            password = input('new password: ')
            passCheck = database.checkPassword(password)

        fullname = input('new fullname: ')
        fullnameCheck = database.checkFullname(fullname)
        while fullnameCheck[1] != True:
            print(fullnameCheck[0])
            fullname = input('new fullname: ')
            fullnameCheck = database.checkFullname(fullname)

        admin = input('admin: ')
        adminCheck = database.checkAdvisorRole(admin)
        while adminCheck[1] != True:
            print(adminCheck[0])
            admin = input('admin: ')
            adminCheck = database.checkAdvisorRole(admin)

        advisor = input('advisor: ')
        advisorCheck = database.checkAdvisorRole(advisor)
        while advisorCheck[1] != True:
            print(advisorCheck[0])
            advisor = input('advisor: ')
            advisorCheck = database.checkAdvisorRole(advisor)
        
        today = date.today().strftime("%d/%m/%Y")
        time = datetime.now().strftime("%H:%M:%S")
        conn = sqlite3.connect(databaseName) 
        cur = conn.cursor()
        cur.execute("SELECT username from users WHERE user_id=:user_id", {"user_id": user_id})
        updateUser = cur.fetchone()
        if updateUser != None:
            updateUser = ''.join(updateUser)
            cur.execute("UPDATE users Set username=:username, password=:password, fullname=:fullname, admin=:admin, advisor=:advisor WHERE user_id=:user_id", {"user_id":user_id, "username": database.encrypt(3, username), "password": database.encrypt(3, password), "fullname": database.encrypt(3, fullname), "admin":admin, "advisor":advisor})
            print('updated user succesfully')
            cur.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?)", [database.encrypt(3, loginname), today, time, database.encrypt(3, 'User updated'), database.encrypt(3, 'User: ' + database.decrypt(3, updateUser) + ' has been updated'), 'No'])
        conn.commit()
        conn.close()

    def make_a_user_admin(loginname):
        user_id = input('user_id: ')
        conn = sqlite3.connect(databaseName) 
        cur = conn.cursor()
        cur.execute("SELECT username from users WHERE user_id=:user_id AND admin='1'", {"user_id": user_id})
        adminName = cur.fetchone()
        today = date.today().strftime("%d/%m/%Y")
        time = datetime.now().strftime("%H:%M:%S")
        if adminName != None:
            adminName = ''.join(adminName)
            cur.execute("UPDATE users SET admin='1' WHERE user_id=:user_id", {"user_id": user_id})
            print('Made admin succesfully')
            cur.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?)", [database.encrypt(3, loginname), today, time, database.encrypt(3, 'Make admin'), database.encrypt(3, 'User: ' + database.decrypt(3, adminName) + ' has been made admin'), 'No'])
        conn.commit()
        conn.close()

    def make_a_user_advisor(loginname):
        user_id = input('user_id: ')
        conn = sqlite3.connect(databaseName) 
        cur = conn.cursor()
        cur.execute("SELECT username from users WHERE user_id=:user_id AND advisor='1'", {"user_id": user_id})
        advisorName = cur.fetchone()
        today = date.today().strftime("%d/%m/%Y")
        time = datetime.now().strftime("%H:%M:%S")
        if advisorName != None:
            advisorName = ''.join(advisorName)
            cur.execute("UPDATE users SET advisor='1' WHERE user_id=:user_id", {"user_id": user_id})
            print('Made advisor succesfully')
            cur.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?)", [database.encrypt(3, loginname), today, time, database.encrypt(3, 'Make advisor'), database.encrypt(3, 'User: ' + database.decrypt(3, advisorName) + ' has been made advisor'), 'No'])
        conn.commit()
        conn.close()

    def delete_client(loginname):
        person_id = input('person_id: ')
        conn = sqlite3.connect(databaseName) 
        cur = conn.cursor()
        cur.execute("SELECT fullname from client WHERE (person_id=:person_id)", {"person_id": person_id})
        deletedClient = cur.fetchone()
        today = date.today().strftime("%d/%m/%Y")
        time = datetime.now().strftime("%H:%M:%S")
        if deletedClient != None:
            deletedClient = ''.join(deletedClient)
            cur.execute("DELETE FROM client WHERE (person_id=:person_id)", {"person_id": person_id})
            print('deleted client succesfully')
            cur.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?)", [database.encrypt(3, loginname), today, time, database.encrypt(3, 'Client Deleted'), database.encrypt(3, 'Client: ' + database.decrypt(3, deletedClient) + ' has been deleted'), 'No'])
        conn.commit()
        conn.close()

    def delete_advisor(loginname):
        user_id = input('user_id: ')
        conn = sqlite3.connect(databaseName) 
        cur = conn.cursor()
        cur.execute("SELECT username from users WHERE user_id=:user_id AND advisor='1'", {"user_id": user_id})
        deletedAdvisor = cur.fetchone()
        today = date.today().strftime("%d/%m/%Y")
        time = datetime.now().strftime("%H:%M:%S")
        if deletedAdvisor != None:
            deletedAdvisor = ''.join(deletedAdvisor)
            cur.execute("DELETE FROM users WHERE user_id=:user_id", {"user_id": user_id})
            print('deleted advisor succesfully')
            cur.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?)", [database.encrypt(3, loginname), today, time, database.encrypt(3, 'Advisor Deleted'), database.encrypt(3, 'User: ' + database.decrypt(3, deletedAdvisor) + ' has been deleted'), 'No'])
        conn.commit()
        conn.close()

    def delete_admin(loginname):
        user_id = input('user_id: ')
        conn = sqlite3.connect(databaseName) 
        cur = conn.cursor()
        cur.execute("SELECT username from users WHERE user_id=:user_id AND admin='1'", {"user_id": user_id})
        deletedAdmin = cur.fetchone()
        today = date.today().strftime("%d/%m/%Y")
        time = datetime.now().strftime("%H:%M:%S")
        if deletedAdmin != None:
            deletedAdmin = ''.join(deletedAdmin)
            cur.execute("DELETE FROM users WHERE user_id=:user_id", {"user_id": user_id})
            print('deleted admin succesfully')
            cur.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?)", [database.encrypt(3, loginname), today, time, database.encrypt(3, 'Admin Deleted'), database.encrypt(3, 'User: ' + deletedAdmin + ' has been deleted'), 'No'])
        conn.commit()
        conn.close()

    def delete_user(loginname):
        user_id = input('user_id: ')
        conn = sqlite3.connect(databaseName) 
        cur = conn.cursor()
        cur.execute("SELECT username from users WHERE user_id=:user_id", {"user_id": user_id})
        deleteUser = cur.fetchone()
        today = date.today().strftime("%d/%m/%Y")
        time = datetime.now().strftime("%H:%M:%S")
        if deleteUser != None:
            deleteUser = ''.join(deleteUser)
            cur.execute("DELETE FROM users WHERE user_id=:user_id", {"user_id": user_id})
            print('deleted user succesfully')
            cur.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?)", [database.encrypt(3, loginname), today, time, database.encrypt(3, 'User Deleted'), database.encrypt(3, 'User: ' + database.decrypt(3, deleteUser) + ' has been deleted'), 'No'])
        conn.commit()
        conn.close()

    def change_own_password(loggedin_user, loginname):
        password = input('new password: ')
        passCheck = database.checkPassword(password)
        while passCheck[1] != True:
            print(passCheck[0])
            password = input('new password: ')
            passCheck = database.checkPassword(password)

        today = date.today().strftime("%d/%m/%Y")
        time = datetime.now().strftime("%H:%M:%S")
        conn = sqlite3.connect(databaseName) 
        cur = conn.cursor()
        cur.execute("UPDATE users SET password=:password WHERE user_id=:user_id", {"password": database.encrypt(3, password), "user_id": loggedin_user})
        print('Password updated succesfully')
        cur.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?)", [database.encrypt(3, loginname), today, time, database.encrypt(3, 'User updated his own password'), '', 'No'])
        conn.commit()
        conn.close()

    def change_admin_password(loginname):
        user_id = input('user_id: ')
        password = input('new password: ')
        passCheck = database.checkPassword(password)
        while passCheck[1] != True:
            print(passCheck[0])
            password = input('new password: ')
            passCheck = database.checkPassword(password)

        today = date.today().strftime("%d/%m/%Y")
        time = datetime.now().strftime("%H:%M:%S")
        conn = sqlite3.connect(databaseName) 
        cur = conn.cursor()
        cur.execute("SELECT username from users WHERE user_id=:user_id AND admin='1'", {"user_id": user_id})
        adminName = cur.fetchone()
        if adminName != None:
            adminName = ''.join(adminName)
            cur.execute("UPDATE users SET password=:password WHERE user_id=:user_id", {"password": database.encrypt(3, password), "user_id": user_id})
            print('Password updated succesfully')
            cur.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?)", [database.encrypt(3, loginname), today, time, database.encrypt(3, 'Changed admin password'), database.encrypt(3, 'User: ' + database.decrypt(3, adminName) + ' has been updated'), 'No'])
        conn.commit()
        conn.close()

    def change_advisor_password(loginname):
        user_id = input('user_id: ')
        password = input('new password: ')
        passCheck = database.checkPassword(password)
        while passCheck[1] != True:
            print(passCheck[0])
            password = input('new password: ')
            passCheck = database.checkPassword(password)

        today = date.today().strftime("%d/%m/%Y")
        time = datetime.now().strftime("%H:%M:%S")
        conn = sqlite3.connect(databaseName) 
        cur = conn.cursor()
        cur.execute("SELECT username from users WHERE user_id=:user_id AND advisor='1'", {"user_id": user_id})
        advisorName = cur.fetchone()
        if advisorName != None:
            advisorName = ''.join(advisorName)
            cur.execute("UPDATE users SET password=:password WHERE user_id=:user_id", {"password": database.encrypt(3, password), "user_id": user_id})
            print('Password updated succesfully')
            cur.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?)", [database.encrypt(3, loginname), today, time, database.encrypt(3, 'Changed advisor password'), database.encrypt(3, 'User: ' + database.decrypt(3, advisorName) + ' has been updated'), 'No'])
        conn.commit()
        conn.close()
    
    def encrypt(key, plainText):
        plainTextUpper = plainText.upper()
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        result = ""

        for letter in plainTextUpper:
            if letter in alphabet: 
                index = (alphabet.find(letter) + key) % len(alphabet)
                result = result + alphabet[index]
            else:
                result = result + letter

        return result

    def decrypt(key, encryptedText):
        encryptedTextUpper = encryptedText.upper()
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        result = ""

        for letter in encryptedTextUpper:
            if letter in alphabet: 
                index = (alphabet.find(letter) - key) % len(alphabet)
                result = result + alphabet[index]
            else:
                result = result + letter

        return result

    def backupSystem():
        conn = sqlite3.connect(databaseName)
        data = '\n'.join(conn.iterdump())
        conn.close()

        zf = zipfile.ZipFile('systemBackup.zip',
                            mode='w',
                            compression=zipfile.ZIP_DEFLATED)
        zf.writestr('dump.txt', data)
        zf.close()
        print('system backup created')

    def viewLogs():
        conn = sqlite3.connect(databaseName) 
        cur = conn.cursor()
        cur.execute("SELECT * from logs")
        allLogs = cur.fetchall()
        clear = "\n" * 100
        print(clear)
        print('-----System Logs-----')
        i = 0
        for row in allLogs:
            i = i + 1
            print(str(i) + " - Username: " + database.decrypt(3, row[0]) + " - Date: " + row[1] + " - Time: " + row[2] + " - Description of activity: " + database.decrypt(3, row[3]) + " - Additional Information: " + database.decrypt(3, row[4]) + " - Suspicious: " + row[5])
        print("\n")
        conn.commit()
        conn.close()

    def checkUsername(username):
        #check for null/None
        #if username == None:
            #return "Empty username"

        #check for username length
        if(len(username) < 5 or len(username) > 20):
            return "Length must be greater than 4 and smaller than 21", False

        #check if first letter is alphabetic
        if(not username[0].isalpha()):
            return "Must start with letter", False

        #whitelisting the correct characters
        correct_letters = list(string.ascii_letters)
        correct_digits = list(string.digits)
        correct_characters = ['.', '-', '_', '\'']

        #checking if username is accepted through the use of whitelist
        for i in username:
            if i not in correct_letters and i not in correct_digits and i not in correct_characters:
                return "Wrong usage of characters", False
        
        return "correct username", True

    def checkPassword(password):
        #check length of password
        if(len(password) < 7 or len(password) > 31):
            return "Length must be greater than 7 and smaller than 31", False
        #whitelisting correct characters
        correct_lowercase = list(string.ascii_lowercase)
        correct_uppercase = list(string.ascii_uppercase)
        correct_digits = list(string.digits)
        correct_characters = list('~!@#$%^&*_-+=`|\\()\{\}[]:;\'<>,.?/')
        #check for every character if it should be accepted through the use of whitelist
        is_lowercase = False
        is_upercase = False
        is_digit = False
        is_character = False
        for i in password:
            if i in correct_lowercase:
                is_lowercase = True
            if i in correct_uppercase:
                is_upercase = True
            if i in correct_digits:
                is_digit = True
            if i in correct_characters:
                is_character = True
            if is_lowercase and is_upercase and is_digit and is_character:
                return "correct password", True
        
        return "not correct password", False

    def checkFullname(fullname):
        if len(fullname) < 4 or len(fullname) > 34:
            return "Wrong length name", False

        #whitelist characters
        correct_letters = list(string.ascii_letters)
        correct_letters.append(" ")
        correct_characters = ['-', '\'']

        #check fullname if in whitelist
        for i in fullname:
            if i not in correct_letters and i not in correct_characters:
                return "Wrong usage of characters", False

        return "correct username", True
    
    def checkAdvisorRole(chosenOption):
        if chosenOption != "0" and chosenOption != "1":
            return "Choose between 0 or 1", False

        return "Correct", True

    def checkClientInfo(name, streetname, housenumber, zipcode, city, emailaddress, phone):
        correct_lowercase = list(string.ascii_lowercase)
        correct_uppercase = list(string.ascii_uppercase)
        correct_digits = list(string.digits)

        #check for null/None
        # if name or streetname or housenumber or zipcode or city or emailaddress or phone == None:
        #     return "Some value is empty"

        #check name
        if len(name) > 30 or len(name) < 2:
            return "Name length must be > 1 and < 30", False
        for i in name:
            if i not in correct_lowercase and i not in correct_uppercase and i not in list('-\''):
                return "Faulty name", False
        
        #check streetname
        if len(streetname) > 50 or len(streetname) < 6:
            return "Streetname length must be > 5 and < 50", False
        for i in streetname:
            if i not in correct_lowercase and i not in correct_uppercase and i not in list('-\''):
                return "Faulty streetname", False
        
        #check housenumber
        for i in housenumber:
            if i not in correct_digits or len(housenumber) > 4:
                return "Faulty housenumber", False
        
        #check zipcode
        if len(zipcode) != 6:
            return "Faulty zipcode", False
        else:
            for i in range(4):
                if zipcode[i] not in correct_digits:
                    return "Faulty zipcode", False
            if zipcode[4] not in string.ascii_letters or zipcode[5] not in string.ascii_letters:
                return "Faulty zipcode", False
        
        #check city
        list_cities = ['amsterdam', 'rotterdam', 'utrecht', 'den haag', 'maastricht', 'nijmegen', 'deventer', 'groningen', 'almere', 'delft']
        if city not in list_cities:
            return "Faulty city", False
        
        #check emailaddress
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(not re.match(regex, emailaddress)):
            return "Faulty emailaddress", False
        
        #check phonenumber
        phone = str(phone)
        if len(phone) != 8:
            return "The phonenumber must be 8 digits", False
        for i in phone:
            if i not in correct_digits:
                return "Faulty phonenumber", False
        
        return "Correct information!", True
    
    def menu(loggedin_user, loginname, loginpassword):
        today = date.today().strftime("%d/%m/%Y")
        time = datetime.now().strftime("%H:%M:%S")
        if loggedin_user == None and loginname != 'superadmin':
            conn = sqlite3.connect(databaseName) 
            cur = conn.cursor()
            cur.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?)", [database.encrypt(3, loginname), today, time, database.encrypt(3, 'unsuccessful login'), database.encrypt(3, 'Password ' + loginpassword + ' is tried in combination with Username: ' +  loginname), 'yes'])
            conn.commit()
            conn.close()
            print('Wrong username or password')
        #super admin login
        elif loginname == 'superadmin' and loginpassword == 'Admin!23':
            conn = sqlite3.connect(databaseName) 
            cur = conn.cursor()
            cur.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?)", [database.encrypt(3, loginname), today, time, database.encrypt(3, 'logged in'), '', 'no'])
            conn.commit()
            conn.close()

            while True:
                print('[0] check users and roles')
                print('[1] add a new advisor')
                print('[2] update excisting advisor')
                print('[3] delete excisting advisor')
                print('[4] reset excisting advisor password')
                print('[5] add a new admin')
                print('[6] update excisting admin')
                print('[7] delete excisting admin')
                print('[8] reset excisting admin password')
                print('[9] make backup of the system')
                print('[10] view system log files')
                print('[11] add a new client')
                print('[12] update excisting client')
                print('[13] delete excisting client')
                print('[14] list excisting clients')
                print('[15] make a user admin')
                print('[16] make a user advisor')
                print('[17] update excisting user')
                print('[18] delete excisting user')
                print('[19] logout')
                choice = input()
                if choice == '0': database.show_all_users()
                if choice == '1': database.add_new_advisor(loginname)
                if choice == '2': database.update_advisor(loginname)
                if choice == '3': database.delete_advisor(loginname)
                if choice == '4': database.change_advisor_password(loginname)
                if choice == '5': database.add_new_admin(loginname)
                if choice == '6': database.update_admin(loginname)
                if choice == '7': database.delete_admin(loginname)
                if choice == '8': database.change_admin_password(loginname)
                if choice == '9': database.backupSystem()
                if choice == '10': database.viewLogs()
                if choice == '11': database.add_new_client(loginname)
                if choice == '12': database.update_client(loginname)
                if choice == '13': database.delete_client(loginname)
                if choice == '14': database.show_all_clients()
                if choice == '15': database.make_a_user_admin(loginname)
                if choice == '16': database.make_a_user_advisor(loginname)
                if choice == '17': database.update_user(loginname)
                if choice == '18': database.delete_user(loginname)
                if choice == '19': return
        #admin login
        elif loggedin_user != None and loggedin_user[4] == 1:
            conn = sqlite3.connect(databaseName) 
            cur = conn.cursor()
            cur.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?)", [database.encrypt(3, loginname), today, time, database.encrypt(3, 'logged in'), '', 'no'])
            conn.commit()
            conn.close()

            while True:
                print('[0] update own password')
                print('[1] check users and roles')
                print('[2] add a new advisor')
                print('[3] update excisting advisor')
                print('[4] delete excisting advisor')
                print('[5] reset excisting advisor password')
                print('[6] make backup of the system')
                print('[7] view system log files')
                print('[8] add a new client')
                print('[9] update excisting client')
                print('[10] delete excisting client')
                print('[11] list excisting clients')
                print('[12] make a user advisor')
                print('[13] logout')
                choice = input()
                if choice == '0': database.change_own_password(loggedin_user[0], loginname)
                if choice == '1': database.show_all_users()
                if choice == '2': database.add_new_advisor(loginname)
                if choice == '3': database.update_advisor(loginname)
                if choice == '4': database.delete_advisor(loginname)
                if choice == '5': database.change_advisor_password(loginname)
                if choice == '6': database.backupSystem()
                if choice == '7': database.viewLogs()
                if choice == '8': database.add_new_client(loginname)
                if choice == '9': database.update_client(loginname)
                if choice == '10': database.delete_client(loginname)
                if choice == '11': database.show_all_clients()
                if choice == '12': database.make_a_user_advisor(loginname)
                if choice == '13': return
        #advisor login
        elif loggedin_user != None and loggedin_user[5] == 1:
            conn = sqlite3.connect(databaseName) 
            cur = conn.cursor()
            cur.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?)", [database.encrypt(3, loginname), today, time, database.encrypt(3, 'logged in'), '', 'no'])
            conn.commit()
            conn.close()

            while True:
                print('[0] update own password')
                print('[1] add a new client')
                print('[2] update excisting client')
                print('[3] list excisting clients')
                print('[4] logout')
                choice = input()
                if choice == '0': database.change_own_password(loggedin_user[0], loginname)
                if choice == '1': database.add_new_client(loginname)
                if choice == '2': database.update_client(loginname)
                if choice == '3': database.show_all_clients()
                if choice == '4': return
        else:
            conn = sqlite3.connect(databaseName) 
            cur = conn.cursor()
            cur.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?)", [database.encrypt(3, loginname), today, time, database.encrypt(3, 'unsuccessful login'), database.encrypt(3, 'Password ' + loginpassword + ' is tried in combination with Username: ' +  loginname), 'yes'])
            conn.commit()
            conn.close()
            print('Wrong username or password')