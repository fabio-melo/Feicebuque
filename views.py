#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" views.py - paginas e endpoints do Flask """

from app import app
from utils import mussum,coxinha
from sql import * # pylint: disable=unused-wildcard-import 
import MySQLdb as mariadb
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from config import DATABASE_CONFIG



def reload_conn():
    """Metodo: Recarrega a conexão com a db e retornar o db e o cursor """    
    db = mariadb.connect(**DATABASE_CONFIG)
    cursor = db.cursor()
    cursor.execute("USE social;")

    return db, cursor


""" Métodos de Carregamento de Páginas """

# MÉTODOS DE LEITURA

@app.route('/',methods=['GET', 'POST'])
def homepage():
    """Flask: Carrega a Página Inicial do Sistema """
    _, cursor = reload_conn()
    postagens = []
    todos_amigos = []
    if session and session['logged_in']:

        cursor.execute(DB_LISTAR_PUBLICACOES_MURAL, (int(session['userid']),))
        postagens = cursor.fetchall()

        cursor.execute(DB_LISTAR_AMIGOS, (session['userid'],session['userid']))
        lista_amigos = cursor.fetchall()
        lista_amigos = list(*zip(*lista_amigos)) # desempacota a tupla de tuplas
        for x in lista_amigos:
            cursor.execute(DB_PROCURAR_USUARIO_POR_ID, (x,))
            uma_pessoa = cursor.fetchall()
            uma_pessoa = list(*zip(*zip(*uma_pessoa)))
            todos_amigos.append(uma_pessoa)
    else:
        cursor.execute(DB_LISTAR_PUBLICACOES_PUBLICAS)
        postagens = cursor.fetchall()
        cursor.execute(DB_LISTAR_USUARIOS)
        todos_amigos = cursor.fetchall()

    return render_template('feed.html', entries=postagens,amigos=todos_amigos)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Autenticacao de Usuario """
    _, cursor = reload_conn()
    error = None

    if request.method == 'POST':

        cursor.execute(DB_PROCURAR_USUARIO, (request.form['email'],))
        user = cursor.fetchall()
        user = list(*zip(*zip(*user)))

        if user:
            if user[4] == request.form['password']:
                session['logged_in'] = True
                session['userid'] = int(user[0])
                session['firstname'] = user[1]
                session['lastname'] = user[2]
                session['email'] = user[3]
                session['password'] = user[4]
                session['gender'] = user[5]
                session['bio'] = user[6]
                return redirect(url_for('homepage'))
            else:
                error = "Senha Errada"

        else:
            error = 'Usuario não existe'

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    """ limpa os dados e sai da sessão """
    session.clear()
    session['logged_in'] = False
    flash('Saiu')
    return redirect(url_for('homepage'))


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    """ Cria usuário no sistema """
    error = None
    db, cursor = reload_conn()

    if request.method == 'POST':
        cursor.execute(DB_PROCURAR_USUARIO, (request.form['email'],))
        user = cursor.fetchall()
        user = list(*zip(*zip(*user)))        
        
        if user:
            error = "usuário já existe"
        else:
            cursor.execute(DB_CRIAR_USUARIO, (request.form['nome'],\
                            request.form['sobrenome'],request.form['email'], \
                            request.form['genero'],request.form['password'], \
                            request.form['bio']))
            db.commit()
            flash('Conta Criada! Bem vindo!')

            # setar cookies do navegador
            session['logged_in'] = True
            session['firstname'] = request.form['nome']
            session['lastname'] = request.form['sobrenome']
            session['email'] = request.form['email']
            session['password'] = request.form['password']
            session['gender'] = request.form['genero']
            session['bio'] = request.form['bio']

            # retornar o id de ssesão do usuario recem criado
            user = cursor.execute(DB_PROCURAR_USUARIO, (request.form['email'],))
            user = cursor.fetchall()
            user = list(*zip(*zip(*user)))
            session['userid'] = user[0]
            return redirect(url_for('homepage'))

    return render_template('cadastrar.html', error=error)


@app.route('/perfil/<idusuario>/', methods=['GET', 'POST'])
def perfil(idusuario):
    """ Carrega o Perfil do usuario em (idusuario) """
    _, cursor = reload_conn()
    cursor.execute(DB_LISTAR_PUBLICACOES_MURAL, (idusuario,))
    postagens = cursor.fetchall()

    cursor.execute(DB_LISTAR_AMIGOS, (idusuario,idusuario))
    lista_amigos = cursor.fetchall()
    lista_amigos = list(*zip(*lista_amigos)) # desempacota a tupla de tuplas
    todos_amigos = []
    for x in lista_amigos:
        cursor.execute(DB_PROCURAR_USUARIO_POR_ID, (x,))
        uma_pessoa = cursor.fetchall()
        uma_pessoa = list(*zip(*zip(*uma_pessoa)))
        todos_amigos.append(uma_pessoa)

    cursor.execute(DB_PROCURAR_USUARIO_POR_ID, (idusuario,))
    pessoa = cursor.fetchall()
    pessoa = list(*zip(*zip(*pessoa)))

    return render_template('perfil.html', entries=postagens,amigos=todos_amigos, pessoa=pessoa)


@app.route('/postar_publicacao', methods=['POST'])
def add_post():
    """ POST: Postar Publicacao """

    if not session.get('logged_in'):
        abort(401)

    db, cursor = reload_conn()
    cursor.execute(DB_ESCREVER_PUBLICACAO, (session['userid'],session['userid']\
                   , request.form['text'], request.form['privacidade']))
    db.commit()

    flash('Postado com Sucesso!')
    return redirect(url_for('homepage'))

@app.route('/postar_amigo/<id_amigo>', methods=['POST'])
def add_post_amigo(id_amigo):
    """ POST: Adicionar postagem na pagina de outra pessoa """
    if not session.get('logged_in'):
        abort(401)
    db, cursor = reload_conn()
    cursor.execute(DB_ESCREVER_PUBLICACAO, (id_amigo, session['userid'], \
                                            request.form['text'], \
                                            request.form['privacidade']))
    db.commit()

    flash('Postado com Sucesso!')
    return redirect(url_for('perfil',idusuario=id_amigo))


@app.route('/remover_publicacao/<idpublicacao>', methods=['POST'])
def remover_publicacao(idpublicacao):
    """ POST: Excluir Publicacao """

    if not session.get('logged_in'):
        abort(401)

    db, cursor = reload_conn()
    cursor.execute(DB_REMOVER_PUBLICACAO, (idpublicacao,))
    db.commit()

    flash('Removido com Sucesso!')
    return redirect(url_for('homepage'))


@app.route('/postar_comentario/<id_publicacao>', methods=['POST'])
def add_comentario(id_publicacao):
    """ POST: Comentar uma publicacao """
    if not session.get('logged_in'):
        abort(401)
    db, cursor = reload_conn()
    cursor.execute(DB_ESCREVER_COMENTARIO, (id_publicacao, session['userid'],\
                                            request.form['text']))
    db.commit()
    flash('Postado com Sucesso!')
    return redirect(url_for('page_comentarios',idpublicacao=id_publicacao))


@app.route('/amigos', methods=['GET', 'POST'])
def page_amigos():
    """ Parte dos Requisitos: Pagina que lista amigos e membros da rede social """
    _, cursor = reload_conn()
    amigos = []
    if session and session['logged_in']:
        cursor.execute(DB_LISTAR_AMIGOS, (session['userid'],session['userid']))
        lista_amigos = cursor.fetchall()
        lista_amigos = list(*zip(*lista_amigos)) # desempacota a tupla de tuplas
        for x in lista_amigos:
            cursor.execute(DB_PROCURAR_USUARIO_POR_ID, (x,))
            uma_pessoa = cursor.fetchall()
            uma_pessoa = list(*zip(*zip(*uma_pessoa)))
            amigos.append(uma_pessoa)
    
    cursor.execute(DB_LISTAR_USUARIOS)
    todaspessoas = cursor.fetchall()
    todaspessoas = [list(x) for x in todaspessoas]
   
    return render_template('amigos.html', amigos=amigos,todaspessoas=todaspessoas)


@app.route('/comentarios/<idpublicacao>', methods=['GET', 'POST'])
def page_comentarios(idpublicacao):
    """ Comentários de Cada Publicação """
    _, cursor = reload_conn()

    cursor.execute(DB_LISTAR_COMENTARIOS, (int(idpublicacao),))
    comentarios = cursor.fetchall()
    comentarios = [list(x) for x in comentarios]

    cursor.execute(DB_PROCURAR_PUBLICACAO, (int(idpublicacao),))
    publicacao = cursor.fetchall()
    publicacao = [list(x) for x in publicacao]

    return render_template('comentarios.html', comentarios=comentarios,publicacao=publicacao)

# MÉTODOS DE ESCRITA

@app.route('/adicionar_amigo<id_amigo>', methods=['POST'])
def web_adicionar_amigo(id_amigo):
    """ POST: Adicionar Amigo """
    if not session.get('logged_in'):
        abort(401)
    db, cursor = reload_conn()

    if session['userid'] == id_amigo: 
        abort(401)

    par_amigos = sorted((int(session['userid']), int(id_amigo)))
    cursor.execute(DB_ADICIONAR_AMIGO, (par_amigos[0],par_amigos[1]))
    db.commit()

    flash('Adicionado com Sucesso!')
    return redirect(url_for('perfil',idusuario=id_amigo))

@app.route('/remover_amigo<id_amigo>', methods=['POST'])
def web_remover_amigo(id_amigo):
    """ POST: Remover Amigos """
    if not session.get('logged_in'):
        abort(401)

    db, cursor = reload_conn()

    if session['userid'] == id_amigo: 
        abort(401)

    par_amigos = sorted((int(session['userid']), int(id_amigo)))
    cursor.execute(DB_REMOVER_AMIGO, (par_amigos[0],par_amigos[1]))
    db.commit()

    flash('Removido com Sucesso!')
    return redirect(url_for('perfil',idusuario=id_amigo))


@app.route('/bloquear_pessoa/<id_amigo>', methods=['POST'])
def web_bloquear_pessoa(id_amigo):
    """ POST: Bloquear Pessoa """
    if not session.get('logged_in'):
        abort(401)
    db, cursor = reload_conn()
    
    if session['userid'] == id_amigo: 
        abort(401)

    par_amigos = sorted((int(session['userid']), int(id_amigo)))
    cursor.execute(DB_BLOQUEAR_PESSOA, (par_amigos[0],par_amigos[1]))
    cursor.execute(DB_REMOVER_AMIGO, (par_amigos[0],par_amigos[1]))
    db.commit()
    

    flash('Bloqueado com Sucesso!')
    return redirect(url_for('perfil',idusuario=id_amigo))


@app.route('/desbloquear_pessoa/<id_amigo>', methods=['POST'])
def web_desbloquear_pessoa(id_amigo):
    """ POST: Desloquear Pessoa """
    if not session.get('logged_in'):
        abort(401)
    db, cursor = reload_conn()
    
    if session['userid'] == id_amigo: 
        abort(401)

    par_amigos = sorted((int(session['userid']), int(id_amigo)))
    cursor.execute(DB_DESBLOQUEAR_PESSOA, (par_amigos[0],par_amigos[1]))
    db.commit()
    

    flash('Desbloqueado com Sucesso!')
    return redirect(url_for('perfil',idusuario=id_amigo))





@app.context_processor
def utils():
    """ jinja2: funções para variaveis de processamento de paginas """
    def verificar_amizade(id_amigo):
        if not session.get('logged_in'):
            abort(401)
        _, cursor = reload_conn()
        test_a = cursor.execute(DB_VERIFICAR_AMIZADE,(session['userid'],id_amigo))
        test_b = cursor.execute(DB_VERIFICAR_AMIZADE,(id_amigo,session['userid']))
        return test_a or test_b
    def verificar_bloqueio(id_amigo):
        if not session.get('logged_in'):
            return None
        _, cursor = reload_conn()
        test_a = cursor.execute(DB_VERIFICAR_BLOQUEIO,(session['userid'],id_amigo) )
        test_b = cursor.execute(DB_VERIFICAR_BLOQUEIO,(id_amigo,session['userid']) )
        return test_a or test_b
    return dict(verificar_amizade=verificar_amizade,verificar_bloqueio=verificar_bloqueio)


