from database import * 

print('Welcome')
print('---------------')
database.createDbIfNotExist()
while True:
    print('[1] login')
    print('[2] exit')
    loginOrExit = input()
    if loginOrExit == '1':
        db = database()
        db.Login()
    elif loginOrExit == '2':
        exit()
    else:
        print('invalid option')