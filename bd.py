import json,datetime,time,csv,random
from sys import argv
import MySQLdb as mariadb
import config
from utils import mussum
from query import *
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from app import app

#-----------------------------------------#
# Inicializão DB                          #
#-----------------------------------------#

def init_db():
    try:
        _, cursor = restartconn('init')
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
        escrever_publicacao(random.randint(1,qtdpessoa), random.randint(1,qtdpessoa), mussum(),cursor,db)

#-----------------------------------------#
# (pessoas)                               #
#-----------------------------------------#
def criar_usuario(db, cursor, nome, sobrenome='',email='', genero=None, senha='', bio=''):
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

def procurar_usuario(cursor, email):
    cursor.execute(DB_PROCURAR_USUARIO, (email,))
    id_achado = cursor.fetchall()
    return (id_achado)


#-----------------------------------------#
# (p-amigos)                              #
#-----------------------------------------#

def adicionar_amigo(id_pessoa1,id_pessoa2,cursor,db):
    try:
        par_amigos = sorted([int(id_pessoa1), int(id_pessoa2)])
        cursor.execute(DB_ADICIONAR_AMIGO, (par_amigos[0],par_amigos[1]))
        db.commit()
    except:
        return None

def remover_amigo(id_pessoa1,id_pessoa2,cursor,db):
    try:
        par_amigos = sorted([int(id_pessoa1), int(id_pessoa2)])
        cursor.execute(DB_REMOVER_AMIGO, (par_amigos[0],par_amigos[1]))
        db.commit()
    except:
        return None

def listar_amigos(id_pessoa,cursor):
    try:
        cursor.execute(DB_LISTAR_AMIGOS, (int(id_pessoa),int(id_pessoa)))
        lista = cursor.fetchall()
        lista_tmp = [list(x) for x in lista]
        return lista_tmp
    except:
        print("ERRO Listando Amigos")
        return None    

#-----------------------------------------#
# (p-amigos)                              #
#-----------------------------------------#

def bloquear_pessoa(id_pessoa1,id_pessoa2,cursor,db):
    try:
        par_pessoas = sorted([int(id_pessoa1), int(id_pessoa2)])
        cursor.execute(DB_BLOQUEAR_PESSOA, (par_pessoas[0],par_pessoas[1]))
        cursor.execute(DB_REMOVER_AMIGO, (par_pessoas[0],par_pessoas[1]))
        db.commit()
    except:
        return None

def desbloquear_pessoa(id_pessoa1,id_pessoa2,cursor,db):
    try:
        par_pessoas = sorted([int(id_pessoa1), int(id_pessoa2)])
        cursor.execute(DB_DESBLOQUEAR_PESSOA, (par_pessoas[0],par_pessoas[1]))
        db.commit()
    except:
        return None

def listar_bloqueios(id_pessoa,cursor,db):
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


def escrever_publicacao(id_pessoa_mural, id_pessoa_postador, texto, cursor, db, tipo='publico'):
    try:
        cursor.execute(DB_ESCREVER_PUBLICACAO, (int(id_pessoa_mural), int(id_pessoa_postador), texto, tipo))
        db.commit()
    except:
        print("ERRO Escrevendo Publicacao")
        return None

def excluir_publicacao(id_publicacao, cursor,db):
    try:
        cursor.execute(DB_REMOVER_PUBLICACAO, (int(id_publicacao),))
        db.commit()
    except:
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
    except mariadb.Error as e:
        print(e)
        print("erro listando publicacoes")
        return None
 

@app.route('/')
def homepage():
    db, cursor = restartconn()
    postagens = listar_publicacoes(cursor=cursor, tipo='publico')
    return render_template('feed.html', entries=postagens)

@app.route('/login', methods=['GET', 'POST'])
def login():
    db, cursor = restartconn()
    error = None
    if request.method == 'POST':
        usernam = procurar_usuario(cursor,request.form['email'])
        if usernam:
            if usernam[0][4] == request.form['password']:
                session['logged_in'] = True
                session['userid'] = int(usernam[0][0])
                session['firstname'] = usernam[0][1]
                session['lastname'] = usernam[0][2]
                session['email'] = usernam[0][3]
                session['password'] = usernam[0][4]
                session['gender'] = usernam[0][5]
                session['bio'] = usernam[0][6]
                return redirect(url_for('homepage'))
            else:
                error = "Senha Errada"

        else:
            error = 'Usuario não existe'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Saiu')
    return redirect(url_for('homepage'))


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    error = None
    db, cursor = restartconn()
    if request.method == 'POST':
        usernam = procurar_usuario(cursor,request.form['email'])
        if usernam:
            error = "usuário já existe"
        else:
            criar_usuario(db, cursor, request.form['nome'],request.form['sobrenome'],request.form['email'],request.form['genero'],request.form['password'])

            flash('Conta Criada! Bem vindo!')
            return redirect(url_for('homepage'))
    return render_template('cadastrar.html', error=error)


@app.route('/novo', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/usuario/<idusuario>', methods=['GET', 'POST'])
def perfil():
    pass



if __name__ == "__main__":

    if 'initdb' in argv: init_db(); db, cursor = restartconn()
    if 'import' in argv: import_test_data(); db, cursor = restartconn()

    # 
    db, cursor = restartconn()
 
    if 'w' in argv:
        user = procurar_usuario(cursor, "slibri2@chron.com")
        print(user)
        print(user[0][3])
    