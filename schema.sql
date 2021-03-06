/* PADRÃO DE NOMENCLATURA
# ENTIDADE = 
# CHAVE PRIMÁRIA = id_qualquercoisa (minusculo)

*/

SET UNIQUE_CHECKS=0;
SET FOREIGN_KEY_CHECKS=0;

DROP DATABASE IF EXISTS social;
CREATE DATABASE social;
USE social;

/* Pessoas = Entidade */

DROP TABLE IF EXISTS pessoas;

CREATE TABLE pessoas(
	id_pessoa INT UNSIGNED NOT NULL AUTO_INCREMENT,
	nome VARCHAR(255) NOT NULL,
	sobrenome VARCHAR(255) NOT NULL,
  	email VARCHAR(255) NOT NULL,
 	senha VARCHAR(255) NOT NULL,
	genero ENUM('Masculino','Feminino','Outro'),
	bio TEXT,
	foto VARCHAR(255),
	data_entrada TIMESTAMP NOT NULL,
	PRIMARY KEY(id_pessoa),
	UNIQUE(email)
);

/* Amigos = Relacionamento ->  Pessoas <-> Pessoas */

DROP TABLE IF EXISTS p_amigos;

CREATE TABLE p_amigos(
	id_pessoa1 INT UNSIGNED NOT NULL,
	id_pessoa2 INT UNSIGNED NOT NULL,
	data_amizade TIMESTAMP NOT NULL,
	PRIMARY KEY(id_pessoa1,id_pessoa2),
	FOREIGN KEY(id_pessoa1) REFERENCES pessoas(id_pessoa) ON DELETE CASCADE, 
	FOREIGN KEY(id_pessoa2) REFERENCES pessoas(id_pessoa) ON DELETE CASCADE
);


DROP TABLE IF EXISTS p_pedido_amizade;

CREATE TABLE p_pedido_amizade(
	id_solicitante INT UNSIGNED NOT NULL,
	id_solicitado INT UNSIGNED NOT NULL,
	data_pedido TIMESTAMP NOT NULL,
	PRIMARY KEY(id_solicitante,id_solicitado),
	FOREIGN KEY(id_solicitante) REFERENCES pessoas(id_pessoa) ON DELETE CASCADE, 
	FOREIGN KEY(id_solicitado) REFERENCES pessoas(id_pessoa) ON DELETE CASCADE
);


DROP TABLE IF EXISTS p_bloqueio;

CREATE TABLE p_bloqueio(
	id_pessoa1 INT UNSIGNED NOT NULL,
	id_pessoa2 INT UNSIGNED NOT NULL,
	data_bloqueio TIMESTAMP NOT NULL,
	PRIMARY KEY(id_pessoa1,id_pessoa2),
	FOREIGN KEY(id_pessoa1) REFERENCES pessoas(id_pessoa) ON DELETE CASCADE, 
	FOREIGN KEY(id_pessoa2) REFERENCES pessoas(id_pessoa) ON DELETE CASCADE
);

/* PublicacoesPessoa = Entidade Fraca */

DROP TABLE IF EXISTS p_publicacoes;

CREATE TABLE p_publicacoes(
	id_publicacao INT UNSIGNED NOT NULL AUTO_INCREMENT,
	id_pessoa_mural INT UNSIGNED NOT NULL,
	id_pessoa_postador INT UNSIGNED NOT NULL,
	data_publicacao TIMESTAMP NOT NULL,
	texto_publicacao TEXT,
	tipo_publicacao ENUM('publico','amigos') NOT NULL,
	PRIMARY KEY(id_publicacao),
	FOREIGN KEY(id_pessoa_mural) REFERENCES pessoas(id_pessoa) ON DELETE CASCADE,
	FOREIGN KEY(id_pessoa_postador) REFERENCES pessoas(id_pessoa) ON DELETE CASCADE
);


CREATE TABLE p_comentarios(
	id_comentario INT UNSIGNED NOT NULL AUTO_INCREMENT,
	id_publicacao INT UNSIGNED NOT NULL,
	id_pessoa_comentario INT UNSIGNED NOT NULL,
	data_publicacao TIMESTAMP NOT NULL,
	texto_publicacao TEXT,
	PRIMARY KEY(id_comentario),
	FOREIGN KEY(id_publicacao) REFERENCES p_publicacoes(id_publicacao) ON DELETE CASCADE,
	FOREIGN KEY(id_pessoa_comentario) REFERENCES pessoas(id_pessoa) ON DELETE CASCADE
);


/* Grupos = Entidade */

DROP TABLE IF EXISTS grupos;

CREATE TABLE grupos(
	id_grupo INT UNSIGNED NOT NULL AUTO_INCREMENT, 
	nome_grupo VARCHAR(255),
	descricao_grupo TEXT,
	PRIMARY KEY(id_grupo),
	UNIQUE(nome_grupo)
);

/* Membro = RELACIONAMENTO Grupo -> Membro # */

DROP TABLE IF EXISTS g_membros;

CREATE TABLE g_membros(
	id_grupo INT UNSIGNED NOT NULL, 
	id_pessoa INT UNSIGNED NOT NULL,
	tipo_membro ENUM('Administrador','Comum','Bloqueado','Solicitado') NOT NULL,
	PRIMARY KEY(id_pessoa, id_grupo), 
	FOREIGN KEY(id_pessoa) REFERENCES pessoas(id_pessoa) ON DELETE CASCADE, 
	FOREIGN KEY(id_grupo) REFERENCES grupos(id_grupo)
);

/* PublicacoesGrupo */

DROP TABLE IF EXISTS g_publicacoes;

CREATE TABLE g_publicacoes(
	id_publicacao INT UNSIGNED NOT NULL AUTO_INCREMENT, 
	id_pessoa INT UNSIGNED NOT NULL, 
	id_grupo INT UNSIGNED NOT NULL, 
	data_publicacao_grupo TIMESTAMP NOT NULL,
	texto TEXT, 
	PRIMARY KEY(id_publicacao), 
	FOREIGN KEY(id_pessoa) REFERENCES pessoas(id_pessoa) ON DELETE CASCADE,
	FOREIGN KEY(id_grupo) REFERENCES grupos(id_grupo)
);


CREATE TABLE g_comentarios(
	id_comentario INT UNSIGNED NOT NULL AUTO_INCREMENT,
	id_publicacao INT UNSIGNED NOT NULL,
	id_pessoa_comentario INT UNSIGNED NOT NULL,
	data_publicacao TIMESTAMP NOT NULL,
	texto_publicacao TEXT,
	PRIMARY KEY(id_comentario),
	FOREIGN KEY(id_publicacao) REFERENCES g_publicacoes(id_publicacao) ON DELETE CASCADE,
	FOREIGN KEY(id_pessoa_comentario) REFERENCES pessoas(id_pessoa) ON DELETE CASCADE
);



SET FOREIGN_KEY_CHECKS=1;
SET UNIQUE_CHECKS=1;
