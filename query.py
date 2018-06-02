# Minhas Queries
# (pessoas)
DB_CRIAR_USUARIO = "INSERT INTO pessoas(nome, sobrenome, email, genero, senha, bio) VALUES (%s,%s,%s,%s,%s,%s);"
DB_EXCLUIR_USUARIO = "DELETE FROM pessoas WHERE id_pessoa = %s;"

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
DB_ESCREVER_PUBLICACAO = "INSERT INTO p_publicacoes(id_pessoa, texto_publicacao) VALUES (%s,%s);"
DB_REMOVER_PUBLICACAO = "DELETE FROM p_publicacoes WHERE id_publicacao = %s;"

