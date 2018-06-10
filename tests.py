# -*- coding: utf-8 -*-
#pylint: disable=unused-variable

from IPython import embed
import json,datetime,time,csv,random
from sys import argv
import MySQLdb as mariadb
import config
from utils import lerolero, coxinha, mussum
from sql import * # pylint: disable=unused-wildcard-import 


#-----------------------------------------#
# Inicializão DB                          #
#-----------------------------------------#

def init_db():
    try:
        _, cursor = restartconn('init')
        cursor.execute(open('schema.sql', mode='r',encoding="utf8").read())
        print("Banco de Dados Inicializado")
    except Exception as e:
        print("Erro na Importacao")
        print(e)

def restartconn(init=False):
        
    db = mariadb.connect(**config.DATABASE_CONFIG)
    cursor = db.cursor()
    if not init:
        cursor.execute("USE social;")

    return db, cursor
#-----------------------------------------#
# TESTES                                  #
#-----------------------------------------#
def import_test_data():
    db, cursor = restartconn()
    with open('MOCK_DATA.csv', 'r') as file:
        reader = csv.DictReader(file)
        for x in reader:
            cursor.execute(DB_CRIAR_USUARIO, (x['first_name'],x['last_name'],x['email'],x['gender'],x['password'],x['bio']))
    db.commit()
    for i in range(1,100):
            gerar_amigos(i,db,cursor)
    for _ in range(3):
        for i in range(100):
            escrever_publicacao(i, random.randint(1,100), lerolero(),cursor,db, tipo='publico')
        for i in range(100):
            escrever_publicacao(i, random.randint(1,100), mussum(),cursor,db, tipo='amigos')      
    for _ in range(5):
        for x in range(600):
            escrever_comentario(x,random.randint(1,100),coxinha(), cursor,db )
    gerar_grupos(cursor,db)
    print("Dados de Teste Importados")


def gerar_amigos(idpessoa, db, cursor,qtdamigos=10, totalpessoasdb=100):
    possiveis = [i for i in range(totalpessoasdb)]
    possiveis.remove(idpessoa)
    random.shuffle(possiveis)
    x = 0
    while x < qtdamigos:
        add = possiveis.pop(0)    
        adicionar_amigo(idpessoa,add,cursor,db)
        x += 1
        
def gerar_grupos(cursor,db):
    cursor.execute(DB_CRIAR_GRUPO,("Eu gosto de Maçã", "Comunidade dedicada aos gostadores de Maçã"))
    cursor.execute(DB_CRIAR_GRUPO,("Reporter João Pessoa", "O Reporter de Jampa"))
    cursor.execute(DB_CRIAR_GRUPO,("Video-Games", "para os fãs de video-game"))
    cursor.execute(DB_CRIAR_GRUPO,("Todos Contra o Futebol", ""))
    cursor.execute(DB_CRIAR_GRUPO,("A E S T H E T I C ", "para os fãs da estética"))
    cursor.execute(DB_CRIAR_GRUPO,("Eu odeio acordar cedo (ORKUT OFICIAL)", ""))
    cursor.execute(DB_CRIAR_GRUPO,("Gatinhos Fofos", ""))
    cursor.execute(DB_CRIAR_GRUPO,("Brasil 2050", ""))
    cursor.execute(DB_CRIAR_GRUPO,("Choque de Cultura", ""))
    cursor.execute(DB_CRIAR_GRUPO,("Sem-Tetos UFPB", ""))
    cursor.execute(DB_CRIAR_GRUPO,("Sofrência Estudantil", ""))

    db.commit()
    for x in range(1,11):
        for _ in range(5):
            cursor.execute(DB_GRUPO_ESCREVER_PUBLICACAO, (x, random.randint(1,100), mussum()))

    for x in range(1,11):
        cursor.execute(DB_GRUPO_ADICIONAR_MEMBRO, (x,random.randint(1,10),"Administrador"))
    
    for x in range(1,11):
        for y in range(20):
            try:
                cursor.execute(DB_GRUPO_ADICIONAR_MEMBRO, (x,random.randint(1,100), "Comum"))
            except:
                continue

    db.commit()

#-----------------------------------------#
# (pessoas)                               #
#-----------------------------------------#
def criar_usuario(db, cursor, nome, sobrenome='',email='', genero=None, senha='', bio=''):
    try:
        cursor.execute(DB_CRIAR_USUARIO, (nome, sobrenome, email, genero, senha, bio))
        db.commit()
    except Exception as e: 
       # print("ERRO CRIANDO USUÁRIO")
       # print(e)
        return None

def excluir_usuario(id_pessoa):
    try:
        cursor.execute(DB_EXCLUIR_USUARIO, (id_pessoa))
        db.commit()
    except Exception as e: 
       # print("ERRO EXCLUINDO USUÁRIO")
       # print(e)
        return None

def procurar_usuario(cursor, email=False, userid=False):
    if email:
        cursor.execute(DB_PROCURAR_USUARIO, (email,))
    elif userid:
        cursor.execute(DB_PROCURAR_USUARIO_POR_ID, (userid,))
    else: 
        return None

    id_achado = cursor.fetchall()
    lista_tmp = [list(x) for x in id_achado]
    if lista_tmp: lista_tmp = lista_tmp[0]
    return lista_tmp 

def listar_usuarios(cursor):
    try:
        cursor.execute(DB_LISTAR_USUARIOS)
        lista = cursor.fetchall()
        lista_tmp = [list(x) for x in lista]
        return lista_tmp
    except Exception as e: 
        print("ERRO Listando Amigos")
        print(e)
        return None    

#-----------------------------------------#
# (p-amigos)                              #
#-----------------------------------------#

def adicionar_amigo(id_pessoa1,id_pessoa2,cursor,db):
    try:
        par_amigos = sorted([int(id_pessoa1), int(id_pessoa2)])
        cursor.execute(DB_ADICIONAR_AMIGO, (par_amigos[0],par_amigos[1]))
        db.commit()
    except Exception as e:
        #print(e)
        return None

def remover_amigo(id_pessoa1,id_pessoa2,cursor,db):
    try:
        par_amigos = sorted([int(id_pessoa1), int(id_pessoa2)])
        cursor.execute(DB_REMOVER_AMIGO, (par_amigos[0],par_amigos[1]))
        db.commit()
    except Exception as e: 
        print(e)
        return None

def listar_amigos(id_pessoa,cursor):
    try:
        cursor.execute(DB_LISTAR_AMIGOS, (int(id_pessoa),int(id_pessoa)))
        lista = cursor.fetchall()
        return [x[0] for x in lista]
    except Exception as e: 
        print("ERRO Listando Amigos")
        print(e)
        return None    

#-----------------------------------------#
# (p-bloquear)                            #
#-----------------------------------------#

def bloquear_pessoa(id_pessoa1,id_pessoa2,cursor,db):
    try:
        par_pessoas = sorted([int(id_pessoa1), int(id_pessoa2)])
        cursor.execute(DB_BLOQUEAR_PESSOA, (par_pessoas[0],par_pessoas[1]))
        cursor.execute(DB_REMOVER_AMIGO, (par_pessoas[0],par_pessoas[1]))
        db.commit()
    except Exception as e: 
        print(e)
        return None

def desbloquear_pessoa(id_pessoa1,id_pessoa2,cursor,db):
    try:
        par_pessoas = sorted([int(id_pessoa1), int(id_pessoa2)])
        cursor.execute(DB_DESBLOQUEAR_PESSOA, (par_pessoas[0],par_pessoas[1]))
        db.commit()
    except Exception as e: 
        print(e)
        return None

def listar_bloqueios(id_pessoa,cursor):
    try:
        cursor.execute(DB_LISTAR_BLOQUEIOS, (int(id_pessoa),int(id_pessoa)))
        lista = cursor.fetchall()
        return [list(x) for x in lista] 
    except Exception as e: 
        print("ERRO Listando Bloqueios")
        print(e)
        return None    

#-----------------------------------------#
# (p_publicacoes)                         #
#-----------------------------------------#


def escrever_publicacao(id_pessoa_mural, id_pessoa_postador, texto, cursor, db, tipo='publico'):
    try:
        cursor.execute(DB_ESCREVER_PUBLICACAO, (int(id_pessoa_mural), int(id_pessoa_postador), texto, tipo))
        db.commit()
    except Exception as e:
        #print(e)
        #print("ERRO Escrevendo Publicacao")
        return None

def excluir_publicacao(id_publicacao, cursor,db):
    try:
        cursor.execute(DB_REMOVER_PUBLICACAO, (int(id_publicacao),))
        db.commit()
    except Exception as e:
        print(e) 
        print("erro excluindo publicacao")

def listar_publicacoes(cursor, tipo='publico'):
    # se nenhum argumento for enviado, mostra a linha publica, caso contrario, pega o numero (ID) do mural
    try:
        if tipo == 'publico':
            cursor.execute(DB_LISTAR_PUBLICACOES_PUBLICAS)
            lista = cursor.fetchall()
        else:
            cursor.execute(DB_LISTAR_PUBLICACOES_MURAL, (int(tipo),))
            lista = cursor.fetchall()
        lista_tmp = [list(x) for x in lista]
        return lista_tmp       
    except Exception as e: 
        print(e)
        print("erro listando publicacoes")
        return None
 


#-----------------------------------------#
# (p_comentarios)                         #
#-----------------------------------------#


def escrever_comentario(id_publicacao, id_pessoa_postador, texto, cursor, db):
    try:
        cursor.execute(DB_ESCREVER_COMENTARIO, (int(id_publicacao), int(id_pessoa_postador), texto))
        db.commit()
    except Exception as e:
       # print(e)
       # print("ERRO Escrevendo comentario")
        return None

def excluir_comentario(id_comentario, cursor,db):
    try:
        cursor.execute(DB_REMOVER_COMENTARIO, (int(id_comentario),))
        db.commit()
    except Exception as e:
        print(e) 
        print("erro excluindo comentario")

def listar_comentarios(id_comentario,cursor):
    # se nenhum argumento for enviado, mostra a linha publica, caso contrario, pega o numero (ID) do mural
    try:
        cursor.execute(DB_LISTAR_COMENTARIOS, (int(id_comentario),))
        lista = cursor.fetchall()
        return [list(x) for x in lista]     
    except Exception as e: 
        print(e)
        print("erro listando publicacoes")
        return None
 


#-----------------------------------------#
# IPYTHON E LINHA DE COMANDO              #
#-----------------------------------------#


if __name__ == "__main__":

    if 'initdb' in argv: init_db()
    if 'import' in argv: import_test_data()

    # 
    db, cursor = restartconn()
    if 'i' in argv: embed()
 
