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


@app.route('/remover_comentario/<idcomentario>', methods=['POST'])
def remover_comentario(idcomentario):
    """ POST: Excluir Publicacao """

    if not session.get('logged_in'):
        abort(401)

    db, cursor = reload_conn()
    cursor.execute(DB_REMOVER_COMENTARIO, (idcomentario,))
    db.commit()

    flash('Removido com Sucesso!')
    return redirect(url_for('homepage'))


@app.route('/amigos', methods=['GET', 'POST'])
def page_amigos():
    """ Parte dos Requisitos: Pagina que lista amigos da rede social """
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
    

   
    return render_template('amigos.html', amigos=amigos)



@app.route('/pessoas', methods=['GET', 'POST'])
def page_pessoas():
    """ Parte dos Requisitos: Pagina que lista todas as pessoas rede social """
    _, cursor = reload_conn()
   
    cursor.execute(DB_LISTAR_USUARIOS)
    todaspessoas = cursor.fetchall()
    todaspessoas = [list(x) for x in todaspessoas]
   
    return render_template('pessoas.html', todaspessoas=todaspessoas)


@app.route('/solicitacoes', methods=['GET', 'POST'])
def page_solicitacoes_amizade():
    """ Parte dos Requisitos: Pagina que lista amigos da rede social """
    _, cursor = reload_conn()

    if session and session['logged_in']:
        cursor.execute(DB_LISTAR_PEDIDO_SOLICITADO, (session['userid'],))
        recebido = cursor.fetchall()
        cursor.execute(DB_LISTAR_PEDIDO_SOLICITANTE, (session['userid'],))
        enviado = cursor.fetchall()
    
    
    return render_template('a_solicitacoes.html', recebido=recebido, enviado=enviado)


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

@app.route('/adicionar_amigo/<id_amigo>', methods=['POST','GET'])
def web_adicionar_amigo(id_amigo):
    """ POST: Adicionar Amigo """
    if not session.get('logged_in'):
        abort(401)
    db, cursor = reload_conn()

    if session['userid'] == id_amigo: 
        abort(401)
    cursor.execute(DB_REMOVER_PEDIDO, (id_amigo,session['userid']))
    par_amigos = sorted((int(session['userid']), int(id_amigo)))
    cursor.execute(DB_ADICIONAR_AMIGO, (par_amigos[0],par_amigos[1]))
    db.commit()

    flash('Adicionado com Sucesso!')
    return redirect(url_for('perfil',idusuario=id_amigo))


@app.route('/solicitar_amigo/<id_amigo>', methods=['GET','POST'])
def web_solicitar_amigo(id_amigo):
    """ POST: Solicitar Amigo """
    if not session.get('logged_in'):
        abort(401)
    db, cursor = reload_conn()

    if session['userid'] == id_amigo: 
        abort(401)

    cursor.execute(DB_SOLICITAR_AMIGO, (session['userid'], int(id_amigo)))
    db.commit()

    flash('Pedido de Amizade Enviado!')
    return redirect(url_for('perfil',idusuario=id_amigo))

@app.route('/excluir_solicitacao_recebida/<id_amigo>', methods=['GET','POST'])
def web_excluir_solicitacao_recebida(id_amigo):
    """ POST: Excluir Solicitacao de Amizade """
    if not session.get('logged_in'):
        abort(401)
    db, cursor = reload_conn()

    if session['userid'] == id_amigo: 
        abort(401)

    cursor.execute(DB_REMOVER_PEDIDO, (int(id_amigo), session['userid']))
    db.commit()

    flash('Solicitacao Excluida!')
    return redirect(url_for('page_solicitacoes_amizade'))



@app.route('/excluir_solicitacao_enviada/<id_amigo>', methods=['GET','POST'])
def web_excluir_solicitacao_enviada(id_amigo):
    """ POST: Excluir Solicitacao de Amizade """
    if not session.get('logged_in'):
        abort(401)
    db, cursor = reload_conn()

    if session['userid'] == id_amigo: 
        abort(401)

    cursor.execute(DB_REMOVER_PEDIDO, (session['userid'], (id_amigo)))
    db.commit()

    flash('Solicitacao Excluida!')
    return redirect(url_for('page_solicitacoes_amizade'))



@app.route('/remover_amigo/<id_amigo>', methods=['GET','POST'])
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


@app.route('/bloquear_pessoa/<id_amigo>', methods=['GET','POST'])
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


@app.route('/grupos', methods=['GET', 'POST'])
def page_grupos():
    """ Pagina que lista os grupos da rede social """
    _, cursor = reload_conn()
    grupos_participados, todos_grupos = [], []

    if session and session['logged_in']:
        cursor.execute(DB_LISTAR_GRUPOS_PARTICIPADOS, (session['userid'],))
        grupos_participados = cursor.fetchall()
        grupos_participados = [list(x) for x in grupos_participados]

        cursor.execute(DB_LISTAR_GRUPOS_LOGADO, (session['userid'],))
        todos_grupos = cursor.fetchall()
        todos_grupos = [list(x) for x in todos_grupos] # desempacota a tupla de tuplas
    else:
        cursor.execute(DB_LISTAR_GRUPOS)
        todos_grupos = cursor.fetchall()
        todos_grupos = [list(x) for x in todos_grupos] # desempacota a tupla de tuplas
        
    return render_template('grupos.html', todos_grupos=todos_grupos,grupos_participados=grupos_participados)


@app.route('/grupos/criar_grupo', methods=['GET', 'POST'])
def page_criar_grupo():
    """ Criar Grupos """
    error = None
    db, cursor = reload_conn()

    if request.method == 'POST':
        grup = cursor.execute(DB_GRUPO_PROCURAR_GRUPO_POR_NOME, (request.form['grupo'],))
        
        if grup:
            error = 'grupo já existe'
        else:
            cursor.execute(DB_CRIAR_GRUPO, (request.form['grupo'], request.form['descricao']))
            cursor.execute(DB_GRUPO_PROCURAR_GRUPO_POR_NOME, (request.form['grupo'],))
            id_grupo = cursor.fetchall()
            cursor.execute(DB_GRUPO_ADICIONAR_MEMBRO, (id_grupo[0][1], session['userid'], 'Administrador'))
            db.commit()
            flash("grupo criado com sucesso")
            return redirect(url_for('page_grupos'))

    return render_template('criargrupo.html', error=error)


@app.route('/grupo/<id_grupo>/adicionar_membro/<id_pessoa>/<tipo_membro>', methods=['POST','GET'])
def grupo_adicionar_amigo(id_grupo, id_pessoa, tipo_membro):
    if not session.get('logged_in'):
        abort(401)
    db, cursor = reload_conn()

    cursor.execute(DB_GRUPO_ADICIONAR_MEMBRO, (id_grupo,id_pessoa,tipo_membro))
    db.commit()

    flash('Adicionado com Sucesso!')
    return redirect(url_for('web_grupo',id_grupo=id_grupo))

@app.route('/grupo/<id_grupo>/remover_membro/<id_pessoa>/', methods=['POST','GET'])
def grupo_remover_amigo(id_grupo,id_pessoa):
    if not session.get('logged_in'):
        abort(401)
    db, cursor = reload_conn()

    cursor.execute(DB_GRUPO_REMOVER_MEMBRO, (id_grupo, id_pessoa))
    db.commit()

    flash('Removido com Sucesso!')
    return redirect(url_for('web_grupo',id_grupo=id_grupo))

@app.route('/grupos/<id_grupo>', methods=['GET', 'POST'])
def web_grupo(id_grupo):
    """ Carrega detalhes, membros e postagens do grupo """
    _, cursor = reload_conn()
    
    cursor.execute(DB_GRUPO_PROCURAR_GRUPO_POR_ID,(id_grupo,))
    detalhes_grupo = cursor.fetchall()
    detalhes_grupo = [list(x) for x in detalhes_grupo]

    postagens_grupo = []
    membros_grupo = []


    if session and session['logged_in']:
        check = cursor.execute(DB_GRUPO_PROCURAR_MEMBRO_POR_ID,(session['userid'],id_grupo))
        if check:    
            cursor.execute(DB_GRUPO_LISTAR_PUBLICACOES, (id_grupo,))
            postagens_grupo = cursor.fetchall()
            postagens_grupo = [list(x) for x in postagens_grupo]
            
            cursor.execute(DB_GRUPO_LISTAR_MEMBROS, (id_grupo,))
            membros_grupo = cursor.fetchall()
            membros_grupo = [list(x) for x in membros_grupo]

    return render_template('gperfil.html', postagens_grupo=postagens_grupo, membros_grupo=membros_grupo, detalhes_grupo=detalhes_grupo, id_grupo=id_grupo)

@app.route('/grupos/<id_grupo>/add_postagem/', methods=['GET', 'POST'])
def grupo_add_postagem(id_grupo):
    if not session.get('logged_in'):
        abort(401)
    db, cursor = reload_conn()
    cursor.execute(DB_GRUPO_ESCREVER_PUBLICACAO, (id_grupo, session['userid'], \
                                            request.form['text']))
    db.commit()

    flash('Postado com Sucesso!')
    return redirect(url_for('web_grupo',id_grupo=id_grupo))

@app.route('/grupo_remover_postagem/<id_postagem>', methods=['GET', 'POST'])
def grupo_remover_postagem(id_postagem):
    """ POST: Excluir Publicacao """

    if not session.get('logged_in'):
        abort(401)

    db, cursor = reload_conn()
    cursor.execute(DB_GRUPO_REMOVER_PUBLICACAO, (id_postagem,))
    db.commit()
    return redirect(url_for('grupo_remover_postagem'))


@app.route('/grupo_add_comentario/<id_comentario>', methods=['GET', 'POST'])
def grupo_add_comentario(id_comentario):
    if not session.get('logged_in'):
        abort(401)
    db, cursor = reload_conn()
    cursor.execute(DB_GRUPO_ESCREVER_COMENTARIO, (id_comentario, session['userid'],\
                                            request.form['text']))
    db.commit()
    flash('Postado com Sucesso!')
    return redirect(url_for('grupo_add_comentario'))

@app.route('/grupo_remover_comentario/<id_comentario>', methods=['GET', 'POST'])
def grupo_remover_comentario(id_comentario):
    if not session.get('logged_in'):
        abort(401)

    db, cursor = reload_conn()
    cursor.execute(DB_GRUPO_REMOVER_COMENTARIO, (id_comentario,))
    db.commit()

    flash('Removido com Sucesso!')
    return redirect(url_for('homepage'))

@app.route('/grupo/<id_grupo>/comentarios/<id_publicacao>', methods=['GET', 'POST'])
def page_grupo_comentarios(idpublicacao):
    """ Comentários de Cada Publicação """
    _, cursor = reload_conn()

    cursor.execute(DB_GRUPO_LISTAR_COMENTARIOS, (int(idpublicacao),))
    comentarios = cursor.fetchall()
    comentarios = [list(x) for x in comentarios]

    cursor.execute(DB_GRUPO_PROCURAR_PUBLICACAO, (int(idpublicacao),))
    publicacao = cursor.fetchall()
    publicacao = [list(x) for x in publicacao]

    return render_template('comentarios.html', comentarios=comentarios,publicacao=publicacao)


@app.route('/grupo/<id_grupo>/solicitacoes', methods=['GET', 'POST'])
def page_solicitacoes_grupo(id_grupo):
    """ Parte dos Requisitos: Pagina que lista amigos da rede social """
    _, cursor = reload_conn()

    if session and session['logged_in']:
        cursor.execute(DB_GRUPO_LISTAR_SOLICITACOES, (id_grupo,))
        recebido = cursor.fetchall()
        cursor.execute(DB_GRUPO_LISTAR_MEMBROS, (id_grupo,))
        enviado = cursor.fetchall()
    
    
    return render_template('g_solicitacoes.html', recebido=recebido, enviado=enviado)


@app.route('/sobre', methods=['GET', 'POST'])
def sobre():
    
    return render_template('sobre.html')


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

    def verificar_status_grupo(id_grupo):
        if not session.get('logged_in'):
            return None
        _, cursor = reload_conn()

        test = cursor.execute(DB_GRUPO_VERIFICAR_PRIVILEGIOS,(id_grupo, session['userid']) )
        test = cursor.fetchall()
        if test:
            return test[0][0]
        else:
            return None
    return dict(verificar_amizade=verificar_amizade,verificar_bloqueio=verificar_bloqueio, verificar_status_grupo=verificar_status_grupo)


