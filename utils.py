#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" utils.py - funções utilitarias usadas no código """

from random import shuffle, randint

# Geradores de texto aleatório
def mussum(tamanhotexto=5):
    mussumfala = ["Pra lá , depois divoltis porris, paradis. ", "Paisis, filhis, espiritis santis. ", "Mé faiz elementum girarzis, nisi eros vermeio. ", "Manduma pindureta quium dia nois paga. ", "Sapien in monti palavris qui num significa nadis i pareci latim. ", "Interessantiss quisso pudia ce receita de bolis, mais bolis eu num gostis.", "Suco de cevadiss, é um leite divinis, qui tem lupuliz, matis, aguis e fermentis. ", "Interagi no mé, cursus quis, vehicula ac nisi. ", "Casamentiss faiz malandris se pirulitá.", "Cevadis im ampola pa arma uma pindureta. ", "Atirei o pau no gatis, per gatis num morreus. ", "Viva Forevis aptent taciti sociosqu ad litora torquent. ", "Copo furadis é disculpa de bebadis, arcu quam euismod magna. ", "Delegadis gente finis, bibendum egestas augue arcu ut est. ", "In elementis mé pra quem é amistosis quis leo. ", "Não sou faixa preta cumpadi, sou preto inteiris, inteiris. ", "Mais vale um bebadis conhecidiss, que um alcoolatra anonimis. ", "Suco de cevadiss deixa as pessoas mais interessantis. ", "Tá deprimidis, eu conheço uma cachacis que pode alegrar sua vidis. ", "Todo mundo vê os porris que eu tomo, mas ninguém vê os tombis que eu levo! ", "Quem manda na minha terra sou euzis! ", "Si num tem leite então bota uma pinga aí cumpadi! ", "Diuretics paradis num copo é motivis de denguis. ", "Em pé sem cair, deitado sem dormir, sentado sem cochilar e fazendo pose. ", "A ordem dos tratores não altera o pão duris. ", "Quem num gosta di mim que vai caçá sua turmis! ", "Quem num gosta di mé, boa gentis num é. ", "Si u mundo tá muito paradis? Toma um mé que o mundo vai girarzis! ", "Per aumento de cachacis, eu reclamis. ", "Detraxit consequat et quo num tendi nada. ", "Admodum accumsan disputationi eu sit. Vide electram sadipscing et per. ", "Leite de capivaris, leite de mula manquis sem cabeça. ", "Aenean aliquam molestie leo, vitae iaculis nisl. ", "Praesent vel viverra nisi. Mauris aliquet nunc non turpis scelerisque, eget. ", "Posuere libero varius. Nullam a nisl ut ante blandit hendrerit. Aenean sit amet nisi. ", "Nec orci ornare consequat. Praesent lacinia ultrices consectetur. Sed non ipsum felis. ", "Praesent malesuada urna nisi, quis volutpat erat hendrerit non. Nam vulputate dapibus. ", "Nullam volutpat risus nec leo commodo, ut interdum diam laoreet. Sed non consequat odio. ", "Mauris nec dolor in eros commodo tempor. Aenean aliquam molestie leo, vitae iaculis nisl. ", "Vehicula non. Ut sed ex eros. Vivamus sit amet nibh non tellus tristique interdum. "]

    shuffle(mussumfala)
    mussumstring = []
    if tamanhotexto > 40: print("Deu errosis"); exit()
    for _ in range(tamanhotexto):
        mussumstring.append(mussumfala.pop())
    return ''.join(mussumstring)

def coxinha(paragrafos=1,linhas=4):
    paragrafos = randint(1,2)
    linhas = randint(1,5)
    tabela = [ \
    ['A miséria', 'A Greve dos Combustiveis', 'A Intervenção Militar','A inflação', 'O Golpe de 1964', 'A violência', 'A crise', 'O crime', 'O racismo', 'O machismo', 'O problema da fome', 'A corrupção'],\
    ['é uma invenção', 'é uma estratégia', 'é uma manobra', 'é um complô', 'é culpa', 'é uma criação', 'é uma conspiração', 'é uma forma orquestrada', 'é a doutrinação ideológica', 'é uma articulação'],\
    ['do PSDB', 'do Michel Temer', 'do Ancapistão', 'do capitalismo', 'dos reaças', 'do Serra', 'da "herança maldita"', 'dos religiosos', 'do homem branco hétero classe média', 'da direita', 'dos homofóbicos', 'da Raquel Sheherazade'],\
    ['para deslegitimar', 'para vandalizar', 'para demoralizar', 'para destruir', 'para regular', 'para ameaçar', 'para superar', 'para roubar', 'para aterrorizar', 'para transgredir'],\
    ['o PT', 'os nordestinos', 'a classe popular', 'a propriedade do estado', 'a Dilma', 'o Lula', 'o Temer', 'os direitos das minorias', 'a democracia', 'a liberdade', 'o ótimo trabalho do governo atual']\
    ]
    texto = []
    for _ in range(paragrafos):
        for _ in range(linhas):
            texto.append(tabela[0][randint(0,11)] + ' ')
            texto.append(tabela[1][randint(0,9)] + ' ') 
            texto.append(tabela[2][randint(0,11)] + ' ')   
            texto.append(tabela[3][randint(0,9)] + ' ')      
            texto.append(tabela[4][randint(0,9)] + '. ')
        texto.append("\n \n")

    return ''.join(texto)
    
def lerolero():

    tabela = [ [
			"Caros amigos, ",
			"Por outro lado, ",
			"Assim mesmo, ",
			"No entanto, não podemos esquecer que ",
			"Do mesmo modo, ",
			"A prática cotidiana prova que ",
			"Nunca é demais lembrar o peso e o significado destes problemas, uma vez que ",
			"As experiências acumuladas demonstram que ",
			"Acima de tudo, é fundamental ressaltar que ",
			"O incentivo ao avanço tecnológico, assim como ",
			"Não obstante, ",
			"Todas estas questões, devidamente ponderadas, levantam dúvidas sobre se ",
			"Pensando mais a longo prazo, ",
			"O que temos que ter sempre em mente é que ",
			"Ainda assim, existem dúvidas a respeito de como ",
			"Gostaria de enfatizar que ",
			"Todavia, ",
			"A nível organizacional, ",
			"O empenho em analisar ",
			"Percebemos, cada vez mais, que ",
			"No mundo atual, ",
			"É importante questionar o quanto ",
			"Neste sentido, ",
			"Evidentemente, ",
			"Por conseguinte, ",
			"É claro que ",
			"Podemos já vislumbrar o modo pelo qual ",
			"Desta maneira, ",
			"O cuidado em identificar pontos críticos n",
			"A certificação de metodologias que nos auxiliam a lidar com "
		],[
			"a execução dos pontos do programa ",
			"a complexidade dos estudos efetuados ",
			"a contínua expansão de nossa atividade ",
			"a estrutura atual da organização ",
			"o novo modelo estrutural aqui preconizado ",
			"o desenvolvimento contínuo de distintas formas de atuação ",
			"a constante divulgação das informações ",
			"a consolidação das estruturas ",
			"a consulta aos diversos militantes ",
			"o início da atividade geral de formação de atitudes ",
			"o desafiador cenário globalizado ",
			"a mobilidade dos capitais internacionais ",
			"o fenômeno da Internet ",
			"a hegemonia do ambiente político ",
			"a expansão dos mercados mundiais ",
			"o aumento do diálogo entre os diferentes setores produtivos ",
			"a crescente influência da mídia ",
			"a necessidade de renovação processual ",
			"a competitividade nas transações comerciais ",
			"o surgimento do comércio virtual ",
			"a revolução dos costumes ",
			"o acompanhamento das preferências de consumo ",
			"o comprometimento entre as equipes ",
			"a determinação clara de objetivos ",
			"a adoção de políticas descentralizadoras ",
			"a valorização de fatores subjetivos ",
			"a percepção das dificuldades ",
			"o entendimento das metas propostas ",
			"o consenso sobre a necessidade de qualificação ",
			"o julgamento imparcial das eventualidades "
		],[
			"nos obriga à análise ",
			"cumpre um papel essencial na formulação ",
			"exige a precisão e a definição ",
			"auxilia a preparação e a composição ",
			"garante a contribuição de um grupo importante na determinação ",
			"assume importantes posições no estabelecimento ",
			"facilita a criação ",
			"obstaculiza a apreciação da importância ",
			"oferece uma interessante oportunidade para verificação ",
			"acarreta um processo de reformulação e modernização ",
			"pode nos levar a considerar a reestruturação ",
			"representa uma abertura para a melhoria ",
			"ainda não demonstrou convincentemente que vai participar na mudança ",
			"talvez venha a ressaltar a relatividade ",
			"prepara-nos para enfrentar situações atípicas decorrentes ",
			"maximiza as possibilidades por conta ",
			"desafia a capacidade de equalização ",
			"agrega valor ao estabelecimento ",
			"é uma das consequências ",
			"promove a alavancagem ",
			"não pode mais se dissociar ",
			"possibilita uma melhor visão global ",
			"estimula a padronização ",
			"aponta para a melhoria ",
			"faz parte de um processo de gerenciamento ",
			"causa impacto indireto na reavaliação ",
			"apresenta tendências no sentido de aprovar a manutenção ",
			"estende o alcance e a importância ",
			"deve passar por modificações independentemente ",
			"afeta positivamente a correta previsão "
        ],[
			"das condições financeiras e administrativas exigidas.",
			"das diretrizes de desenvolvimento para o futuro.",
			"do sistema de participação geral.",
			"das posturas dos órgãos dirigentes com relação às suas atribuições.",
			"das novas proposições.",
			"das direções preferenciais no sentido do progresso.",
			"do sistema de formação de quadros que corresponde às necessidades.",
			"das condições inegavelmente apropriadas.",
			"dos índices pretendidos.",
			"das formas de ação.",
			"dos paradigmas corporativos.",
			"dos relacionamentos verticais entre as hierarquias.",
			"do processo de comunicação como um todo.",
			"dos métodos utilizados na avaliação de resultados.",
			"de todos os recursos funcionais envolvidos.",
			"dos níveis de motivação departamental.",
			"da gestão inovadora da qual fazemos parte.",
			"dos modos de operação convencionais.",
			"de alternativas às soluções ortodoxas.",
			"dos procedimentos normalmente adotados.",
			"dos conhecimentos estratégicos para atingir a excelência.",
			"do fluxo de informações.",
			"do levantamento das variáveis envolvidas.",
			"das diversas correntes de pensamento.",
			"do impacto na agilidade decisória.",
			"das regras de conduta normativas.",
			"do orçamento setorial.",
			"do retorno esperado a longo prazo.",
			"do investimento em reciclagem técnica.",
			"do remanejamento dos quadros funcionais."
        ] ]
    paragrafos = randint(1,3)
    linhas = randint(1,3)
    texto = []
    for _ in range(paragrafos):
        for _ in range(linhas):
            texto.append(tabela[0][randint(0,len(tabela[0])-1)])
            texto.append(tabela[1][randint(0,len(tabela[1])-1)]) 
            texto.append(tabela[2][randint(0,len(tabela[2])-1)])
            texto.append(tabela[3][randint(0,len(tabela[3])-1)]) 
        texto.append("<br>")

    return ''.join(texto)
    