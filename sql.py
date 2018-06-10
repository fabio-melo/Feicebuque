#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" SQL Queries - Definições de todas as queries que fazemos ao banco de dados """

# Minhas Queries
# (pessoas)
DB_CRIAR_USUARIO = "INSERT INTO pessoas(nome, sobrenome, email, genero, senha, bio) VALUES (%s,%s,%s,%s,%s,%s);"
DB_EXCLUIR_USUARIO = "DELETE FROM pessoas WHERE id_pessoa = %s;"
DB_PROCURAR_USUARIO = "SELECT * FROM pessoas WHERE email = %s;"
DB_PROCURAR_USUARIO_POR_ID = "SELECT * FROM pessoas WHERE id_pessoa = %s;"
DB_LISTAR_USUARIOS = "SELECT id_pessoa,nome,sobrenome FROM pessoas;"

# (p_pedido_amizade)
DB_SOLICITAR_AMIGO  = "INSERT INTO p_pedido_amizade(id_solicitante,id_solicitado) VALUES (%s,%s);"
DB_REMOVER_PEDIDO = "DELETE FROM p_pedido_amizade WHERE id_pessoa1 = %s AND id_pessoa2 = %s;"
DB_LISTAR_PEDIDO = "SELECT * FROM p_pedido_amizade WHERE (id_solicitante LIKE %s OR id_solicitadol LIKE %s);"

# (p_amigos)
DB_ADICIONAR_AMIGO  = "INSERT INTO p_amigos(id_pessoa1,id_pessoa2) VALUES (%s,%s);"
DB_REMOVER_AMIGO = "DELETE FROM p_amigos WHERE id_pessoa1 = %s AND id_pessoa2 = %s;"
DB_LISTAR_AMIGOS = "SELECT id_pessoa1 FROM p_amigos WHERE id_pessoa2 LIKE %s \
                      UNION SELECT id_pessoa2 FROM p_amigos WHERE id_pessoa1 LIKE %s;"

DB_VERIFICAR_AMIZADE = "SELECT * FROM p_amigos WHERE (id_pessoa1 LIKE %s AND id_pessoa2 LIKE %s);"

# (p_bloqueio)
DB_BLOQUEAR_PESSOA = "INSERT INTO p_bloqueio(id_pessoa1,id_pessoa2) VALUES (%s,%s);"
DB_DESBLOQUEAR_PESSOA = "DELETE FROM p_bloqueio WHERE id_pessoa1 = %s AND id_pessoa2 = %s;"
DB_LISTAR_BLOQUEIOS = "SELECT id_pessoa1 FROM p_bloqueio WHERE id_pessoa2 LIKE %s \
                      UNION SELECT id_pessoa2 FROM p_bloqueio WHERE id_pessoa1 LIKE %s;"



DB_VERIFICAR_BLOQUEIO = "SELECT * FROM p_bloqueio WHERE (id_pessoa1 LIKE %s AND id_pessoa2 LIKE %s);"

# (p_publicacoes)
DB_ESCREVER_PUBLICACAO = "INSERT INTO p_publicacoes(id_pessoa_mural, id_pessoa_postador, texto_publicacao, tipo_publicacao) VALUES (%s,%s,%s,%s);"
DB_REMOVER_PUBLICACAO = "DELETE FROM p_publicacoes WHERE id_publicacao = %s;"

DB_LISTAR_PUBLICACOES_PUBLICAS = \
    "SELECT p_publicacoes.id_publicacao, mural.nome, mural.sobrenome, postador.nome, postador.sobrenome, p_publicacoes.texto_publicacao, p_publicacoes.data_publicacao, p_publicacoes.id_pessoa_mural, p_publicacoes.id_pessoa_postador \
    FROM p_publicacoes \
    INNER JOIN pessoas mural ON mural.id_pessoa = p_publicacoes.id_pessoa_mural \
    INNER JOIN pessoas postador ON postador.id_pessoa = p_publicacoes.id_pessoa_postador \
    WHERE (p_publicacoes.tipo_publicacao LIKE 'publico')\
    ORDER BY p_publicacoes.data_publicacao DESC;"

DB_LISTAR_PUBLICACOES_MURAL = \
    "SELECT p_publicacoes.id_publicacao, mural.nome, mural.sobrenome, postador.nome, postador.sobrenome, p_publicacoes.texto_publicacao, p_publicacoes.data_publicacao, p_publicacoes.id_pessoa_mural, p_publicacoes.id_pessoa_postador \
    FROM p_publicacoes \
    INNER JOIN pessoas mural ON mural.id_pessoa = p_publicacoes.id_pessoa_mural \
    INNER JOIN pessoas postador ON postador.id_pessoa = p_publicacoes.id_pessoa_postador \
    WHERE (p_publicacoes.id_pessoa_mural LIKE %s)\
    ORDER BY p_publicacoes.data_publicacao DESC;"

DB_LISTAR_PUBLICACOES_LINHA_DO_TEMPO = \
    "SELECT p_publicacoes.id_publicacao, mural.nome, mural.sobrenome, postador.nome, postador.sobrenome, p_publicacoes.texto_publicacao, p_publicacoes.data_publicacao \
    FROM p_publicacoes \
    INNER JOIN pessoas mural ON mural.id_pessoa = p_publicacoes.id_pessoa_mural \
    INNER JOIN pessoas postador ON postador.id_pessoa = p_publicacoes.id_pessoa_postador \
    WHERE (p_publicacoes.id_pessoa_mural LIKE %s)\
    ORDER BY p_publicacoes.data_publicacao DESC;"


DB_PROCURAR_PUBLICACAO = \
    "SELECT p_publicacoes.id_publicacao, mural.nome, mural.sobrenome, postador.nome, postador.sobrenome, p_publicacoes.texto_publicacao, p_publicacoes.data_publicacao \
    FROM p_publicacoes \
    INNER JOIN pessoas mural ON mural.id_pessoa = p_publicacoes.id_pessoa_mural \
    INNER JOIN pessoas postador ON postador.id_pessoa = p_publicacoes.id_pessoa_postador \
    WHERE (p_publicacoes.id_publicacao LIKE %s)\
    ORDER BY p_publicacoes.data_publicacao DESC;"


# (p_comentarios)
DB_ESCREVER_COMENTARIO = "INSERT INTO p_comentarios(id_publicacao, id_pessoa_comentario, texto_publicacao) VALUES (%s,%s,%s);"
DB_REMOVER_COMENTARIO = "DELETE FROM p_comentarios WHERE id_comentario = %s;"
DB_LISTAR_COMENTARIOS = \
    "SELECT id_pessoa_comentario, postador.nome, postador.sobrenome, data_publicacao, texto_publicacao \
    FROM p_comentarios \
    INNER JOIN pessoas postador ON postador.id_pessoa = p_comentarios.id_pessoa_comentario \
    WHERE (p_comentarios.id_publicacao LIKE %s)\
    ORDER BY p_comentarios.data_publicacao DESC;"

# (grupos)
DB_CRIAR_GRUPO = "INSERT INTO grupos(nome_grupo,descricao_grupo) \
                  VALUES (%s, %s);"

DB_LISTAR_GRUPOS_LOGADO = 'grupos.id_grupo, grupos.nome_grupo, grupos.descricao_grupo\
                           INNER JOIN g_membros g ON g.id_grupo = grupos.id_grupo \
                                  WHERE g.id_pessoa = %s AND g.tipo_membro != "Bloqueado";'

DB_LISTAR_GRUPOS_PARTICIPADOS = 'SELECT grupos.id_grupo, grupos.nome_grupo, grupos.descricao_grupo FROM grupos\
                                  INNER JOIN g_membros g ON g.id_grupo = grupos.id_grupo \
                                  WHERE g.id_pessoa = %s AND g.tipo_membro != "Bloqueado";'

# (g_membros)
DB_GRUPO_ADICIONAR_MEMBRO = "INSERT INTO g_membros(id_grupo,id_pessoa,tipo_membro) \
                         VALUES (%s,%s,%s);"

DB_GRUPO_REMOVER_MEMBRO = "DELETE FROM g_membros WHERE id_grupo = %s and id_pessoa = %s;"

DB_GRUPO_LISTAR_MEMBROS = 'SELECT grupos.id_grupo, grupos.nome_grupo, g.tipo_membro, g.id_pessoa, p.nome, p.sobrenome FROM grupos \
                           INNER JOIN g_membros g ON g.id_grupo = grupos.id_grupo \
                           INNER JOIN pessoas p ON p.id_pessoa = g.id_pessoa \
                                  WHERE g.id_grupo = %s and g.tipo_membro != "Bloqueado";'

DB_GRUPO_LISTAR_SOLICITACOES = 'SELECT grupos.id_grupo, grupos.nome_grupo, g.tipo_membro, g.id_pessoa, p.nome, p.sobrenome FROM grupos \
                                INNER JOIN g_membros g ON g.id_grupo = grupos.id_grupo \
                                INNER JOIN pessoas p ON p.id_pessoa = g.id_pessoa \
                                WHERE g.id_grupo = %s and g.tipo_membro = "Solicitado";'


# tornar ou remover admin, e bloquear
DB_GRUPO_MODIFICAR_PRIVILEGIOS = "UPDATE g_membros \
                              SET tipo_membro = %s \
                              WHERE id_grupo = %s AND id_pessoa = %s;"

# (g_publicacoes)
DB_GRUPO_ESCREVER_PUBLICACAO = "INSERT INTO g_publicacoes(id_grupo, id_pessoa, texto) VALUES (%s,%s,%s);"
DB_GRUPO_REMOVER_PUBLICACAO = "DELETE FROM g_publicacoes WHERE id_publicacao = %s;"


DB_GRUPO_LISTAR_PUBLICACOES = \
    "SELECT g_publicacoes.id_publicacao, g_publicacoes.id_pessoa, g_publicacoes.id_grupo, m.nome, m.sobrenome, g_publicacoes.texto, g.nome_grupo, g_publicacoes.data_publicacao_grupo \
    FROM g_publicacoes \
    INNER JOIN pessoas m ON m.id_pessoa = g_publicacoes.id_pessoa \
    INNER JOIN grupos g ON g.id_grupo = g_publicacoes.id_grupo \
    WHERE (g_publicacoes.id_grupo LIKE %s)\
    ORDER BY g_publicacoes.data_publicacao_grupo DESC;"


DB_GRUPO_PROCURAR_PUBLICACAO = \
    "SELECT g_publicacoes.id_publicacao, g_publicacoes.id_pessoa, g_publicacoes.id_grupo, m.nome, m.sobrenome, g_publicacoes.texto, g.nome_grupo, g_publicacoes.data_publicacao_grupo \
    FROM g_publicacoes \
    INNER JOIN pessoas m ON m.id_pessoa = g_publicacoes.id_pessoa \
    INNER JOIN grupos g ON g.id_grupo = g_publicacoes.id_grupo \
    WHERE (g_publicacoes.id_publicacao LIKE %s)\
    ORDER BY g_publicacoes.data_publicacao_grupo DESC;"
