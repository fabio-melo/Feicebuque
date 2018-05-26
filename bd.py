import json,datetime,time,csv,sys,random
import MySQLdb as mariadb


def init_db(cursor):
    cursor.execute(open('schema.sql', mode='r',encoding="utf8").read())


def import_test_data(cursor):
    cursor.execute("USE social")
    with open('MOCK_DATA.csv', 'r') as file:
        reader = csv.DictReader(file)
        for x in reader:
            cursor.execute("INSERT INTO pessoas(nome, sobrenome,email,senha,bio) VALUES (%s,%s,%s,%s,%s);", (x['first_name'],x['last_name'],x['email'],x['password'],x['bio']) )
        for x in range(50):
            cursor.execute("INSERT INTO p_amigos(id_amigo1, id_amigo2) VALUES (%s,%s);", (random.randint(1,1000),random.randint(1,1000)))
    db.commit()



if __name__ == "__main__":
    db = mariadb.connect(user='root', password='@idk')
    #db.autocommit = True
    cursor = db.cursor()
    
    op = sys.argv[1] if len(sys.argv) >= 2 else 'noop'
    
    if op == 'initdb': init_db(cursor)
    if op == 'import': import_test_data(cursor)
