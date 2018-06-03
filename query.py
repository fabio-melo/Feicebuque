# -*- coding: utf-8 -*-

# Minhas Queries
# (pessoas)
DB_CRIAR_USUARIO = "INSERT INTO pessoas(nome, sobrenome, email, genero, senha, bio) VALUES (%s,%s,%s,%s,%s,%s);"
DB_EXCLUIR_USUARIO = "DELETE FROM pessoas WHERE id_pessoa = %s;"
DB_PROCURAR_USUARIO = "SELECT * FROM pessoas WHERE email = %s;"
# (p_pedido_amizade)
DB_SOLICITAR_AMIGO  = "INSERT INTO p_pedido_amizade(id_solicitante,id_solicitado) VALUES (%s,%s);"
DB_REMOVER_PEDIDO = "DELETE FROM p_pedido_amizade WHERE id_pessoa1 = %s AND id_pessoa2 = %s;"
DB_LISTAR_PEDIDO = "SELECT * FROM p_pedido_amizade WHERE (id_solicitante LIKE %s OR id_solicitadol LIKE %s);"

# (p_amigos)
DB_ADICIONAR_AMIGO  = "INSERT INTO p_amigos(id_pessoa1,id_pessoa2) VALUES (%s,%s);"
DB_REMOVER_AMIGO = "DELETE FROM p_amigos WHERE id_pessoa1 = %s AND id_pessoa2 = %s;"
DB_LISTAR_AMIGOS = "SELECT * FROM p_amigos WHERE (id_pessoa1 LIKE %s OR id_pessoa2 LIKE %s);"

# (p_bloqueio)
DB_BLOQUEAR_PESSOA = "INSERT INTO p_bloqueio(id_pessoa1,id_pessoa2) VALUES (%s,%s);"
DB_DESBLOQUEAR_PESSOA = "DELETE FROM p_bloqueio WHERE id_pessoa1 = %s AND id_pessoa2 = %s;"
DB_LISTAR_BLOQUEIOS = "SELECT * FROM p_bloqueio WHERE (id_pessoa1 LIKE %s OR id_pessoa2 LIKE %s);"

# (p_publicacoes)
DB_ESCREVER_PUBLICACAO = "INSERT INTO p_publicacoes(id_pessoa_mural, id_pessoa_postador, texto_publicacao, tipo_publicacao) VALUES (%s,%s,%s,%s);"
DB_REMOVER_PUBLICACAO = "DELETE FROM p_publicacoes WHERE id_publicacao = %s;"

DB_LISTAR_PUBLICACOES_PUBLICAS = \
    "SELECT p_publicacoes.id_publicacao, mural.nome, mural.sobrenome, postador.nome, postador.sobrenome, p_publicacoes.texto_publicacao, p_publicacoes.data_publicacao \
    FROM p_publicacoes \
    INNER JOIN pessoas mural ON mural.id_pessoa = p_publicacoes.id_pessoa_mural \
    INNER JOIN pessoas postador ON postador.id_pessoa = p_publicacoes.id_pessoa_postador \
    WHERE (p_publicacoes.tipo_publicacao LIKE 'publico')\
    ORDER BY p_publicacoes.data_publicacao DESC;"

DB_LISTAR_PUBLICACOES_MURAL = \
    "SELECT p_publicacoes.id_publicacao, mural.nome, mural.sobrenome, postador.nome, postador.sobrenome, p_publicacoes.texto_publicacao, p_publicacoes.data_publicacao \
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
