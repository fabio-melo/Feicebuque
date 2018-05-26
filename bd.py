import json,datetime,time,csv,sys,random
import MySQLdb as mariadb


def init_db(cursor):
    cursor.execute(open('schema.sql', mode='r',encoding="utf8").read())


def import_test_data(cursor):
    cursor.execute("USE social;")
    with open('MOCK_DATA.csv', 'r') as file:
        reader = csv.DictReader(file)
        for x in reader:
            cursor.execute("INSERT INTO pessoas(nome, sobrenome,email,senha,bio) VALUES (%s,%s,%s,%s,%s);", (x['first_name'],x['last_name'],x['email'],x['password'],x['bio']) )
        #for x in range(50):
        #    cursor.execute("INSERT INTO p_amigos(id_amigo1, id_amigo2) VALUES (%s,%s);", (random.randint(1,1000),random.randint(1,1000)))
    db.commit()

#-----------------------------------------#
# Operações de Amizade (p_amigos)         #
#-----------------------------------------#
def adicionar_amigo(id_amigo1,id_amigo2):
    par_amigos = sorted([int(id_amigo1), int(id_amigo2)])
    cursor.execute("INSERT INTO p_amigos(id_amigo1,id_amigo2) VALUES (%s,%s);", (par_amigos[0],par_amigos[1]))
    db.commit()

def remover_amigo(id_amigo1,id_amigo2):
    par_amigos = sorted([int(id_amigo1), int(id_amigo2)])
    cursor.execute("DELETE FROM p_amigos WHERE id_amigo1 = %s AND id_amigo2 = %s;", (par_amigos[0],par_amigos[1]))
    db.commit()

def listar_amigos(id_pessoa):
    cursor.execute("SELECT * FROM p_amigos WHERE (id_amigo1 LIKE %s OR id_amigo2 LIKE %s);", (int(id_pessoa),int(id_pessoa)))
    lista = cursor.fetchall()
    print(lista)
    db.commit()
#-----------------------------------------#
# Operações de Amizade (p_amigos)         #
#-----------------------------------------#





if __name__ == "__main__":
    db = mariadb.connect(user='root', password='@idk')
    #db.autocommit = True
    cursor = db.cursor()
    
    op = sys.argv[1] if len(sys.argv) >= 2 else 'noop'
    
    if op == 'initdb': init_db(cursor)
    if op == 'import': import_test_data(cursor)

    cursor.execute("USE social;")  

    if op == 'test':    
        adicionar_amigo(1,4)
        adicionar_amigo(1,5)
        adicionar_amigo(1,6)
        adicionar_amigo(1,8)
        adicionar_amigo(2,4)
        adicionar_amigo(2,5)
        adicionar_amigo(5,4)
        adicionar_amigo(6,5)
        adicionar_amigo(9,10)
        adicionar_amigo(9,5)
        adicionar_amigo(9,3)
        adicionar_amigo(8,5)
    if op == 'lis': listar_amigos(5)
