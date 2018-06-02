import json,datetime,time,csv,random
from sys import argv
import MySQLdb as mariadb
import config
from utils import mussum
from query import *
from flask import render_template
from app import app

#-----------------------------------------#
# Inicializão DB                          #
#-----------------------------------------#

def init_db():
    try:
        cursor.execute(open('schema.sql', mode='r',encoding="utf8").read())
        print("Banco de Dados Inicializado")
    except:
        print("Erro na Importacao")

def restartconn(init=False):
    if 'db' in globals():
        globals()['db'].close()
        
    db = mariadb.connect(**config.DATABASE_CONFIG)
    cursor = db.cursor()
    if not init:
        cursor.execute("USE social;")

    return db, cursor
#-----------------------------------------#
# TESTES                                  #
#-----------------------------------------#
def import_test_data():
    cursor.execute("USE social;")
    with open('MOCK_DATA.csv', 'r') as file:
        reader = csv.DictReader(file)
        for x in reader:
            cursor.execute(DB_CRIAR_USUARIO, (x['first_name'],x['last_name'],x['email'],x['gender'],x['password'],x['bio']) )
        #for x in range(50):
        #    for y in range(random.randint(1,10)): 
        #        cursor.execute(DB_ADICIONAR_AMIGO, (int(x), int(y+1)))
    db.commit()
    import_test_publications(qtdpub=200,qtdpessoa=100)
    print("Dados de Teste Importados")


def import_test_publications(qtdpub=1, qtdpessoa=5):
    for _ in range(qtdpub):
        escrever_publicacao(random.randint(1,qtdpessoa), random.randint(1,qtdpessoa), mussum())

#-----------------------------------------#
# (pessoas)                               #
#-----------------------------------------#
def criar_usuario(nome, sobrenome='',email='', genero=None, senha='', bio=''):
    try:
        cursor.execute(DB_CRIAR_USUARIO, (nome, sobrenome, email, genero, senha, bio))
        db.commit()
    except:
        print("ERRO CRIANDO USUÁRIO")
        return None

def excluir_usuario(id_pessoa):
    try:
        cursor.execute(DB_EXCLUIR_USUARIO, (id_pessoa))
        db.commit()
    except:
        print("ERRO EXCLUINDO USUÁRIO")

#-----------------------------------------#
# (p-amigos)                              #
#-----------------------------------------#

def adicionar_amigo(id_pessoa1,id_pessoa2):
    try:
        par_amigos = sorted([int(id_pessoa1), int(id_pessoa2)])
        cursor.execute(DB_ADICIONAR_AMIGO, (par_amigos[0],par_amigos[1]))
        db.commit()
    except:
        return None

def remover_amigo(id_pessoa1,id_pessoa2):
    try:
        par_amigos = sorted([int(id_pessoa1), int(id_pessoa2)])
        cursor.execute(DB_REMOVER_AMIGO, (par_amigos[0],par_amigos[1]))
        db.commit()
    except:
        return None

def listar_amigos(id_pessoa):
    try:
        cursor.execute(DB_LISTAR_AMIGOS, (int(id_pessoa),int(id_pessoa)))
        lista = cursor.fetchall()
        db.commit()
        lista_tmp = [list(x) for x in lista]
        return lista_tmp
    except:
        print("ERRO Listando Amigos")
        return None    

#-----------------------------------------#
# (p-amigos)                              #
#-----------------------------------------#

def bloquear_pessoa(id_pessoa1,id_pessoa2):
    try:
        par_pessoas = sorted([int(id_pessoa1), int(id_pessoa2)])
        cursor.execute(DB_BLOQUEAR_PESSOA, (par_pessoas[0],par_pessoas[1]))
        cursor.execute(DB_REMOVER_AMIGO, (par_pessoas[0],par_pessoas[1]))
        db.commit()
    except:
        return None

def desbloquear_pessoa(id_pessoa1,id_pessoa2):
    try:
        par_pessoas = sorted([int(id_pessoa1), int(id_pessoa2)])
        cursor.execute(DB_DESBLOQUEAR_PESSOA, (par_pessoas[0],par_pessoas[1]))
        db.commit()
    except:
        return None

def listar_bloqueios(id_pessoa):
    try:
        cursor.execute(DB_LISTAR_BLOQUEIOS, (int(id_pessoa),int(id_pessoa)))
        lista = cursor.fetchall()
        db.commit()
        lista_tmp = [list(x) for x in lista]
        return lista_tmp  
    except:
        print("ERRO Listando Bloqueios")
        return None    

#-----------------------------------------#
# (p_publicacoes)                         #
#-----------------------------------------#


def escrever_publicacao(id_pessoa_mural, id_pessoa_postador, texto, tipo='publico'):
    try:
        cursor.execute(DB_ESCREVER_PUBLICACAO, (int(id_pessoa_mural), int(id_pessoa_postador), texto, tipo))
        db.commit()
    except:
        print("ERRO Escrevendo Publicacao")
        return None

def excluir_publicacao(id_publicacao):
    try:
        cursor.execute(DB_REMOVER_PUBLICACAO, (int(id_publicacao),))
        db.commit()
    except:
        print("erro excluindo publicacao")

def listar_publicacoes(tipo='publico'):
    # se nenhum argumento for enviado, mostra a linha publica, caso contrario, pega o numero (ID) do mural
    try:
        if tipo == 'publico':
            cursor.execute(DB_LISTAR_PUBLICACOES_PUBLICAS)
            lista = cursor.fetchall()
        else:
            cursor.execute(DB_LISTAR_PUBLICACOES_MURAL, (int(tipo),))
            lista = cursor.fetchall()
        db.commit()
        lista_tmp = [list(x) for x in lista]
        return lista_tmp       
    except mariadb.Error as e:
        print(e)
        print("erro listando publicacoes")
        return None
 

@app.route('/')
def homepage():
    db, cursor = restartconn()
    cursor.execute("USE social;") 
    postagens = listar_publicacoes(1)
    print(postagens)
    return render_template('feed.html', entries=postagens)


if __name__ == "__main__":

    if 'initdb' in argv: init_db(); db, cursor = restartconn()
    if 'import' in argv: import_test_data(); db, cursor = restartconn()

    # 

    if 'test1' in argv:
        cursor.execute("USE social;") 
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
        remover_amigo(8,5)
        bloquear_pessoa(9,5)
    if 'tes' in argv: 
        cursor.execute("USE social;") 
        #listar_amigos(1)
        #escrever_publicacao(1, mussunificador())
        #escrever_publicacao(2, mussunificador())
        #criar_usuario(nome="John", genero='Masculino')

    if 'bla' in argv:
        cursor.execute("USE social;") 
        excluir_usuario('1')
    if 'idk' in argv:
        cursor.execute("USE social;") 
        print(listar_publicacoes(1))
        
