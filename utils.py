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
    