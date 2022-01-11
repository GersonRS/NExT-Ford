# Remova duplicatas de uma lista ordenada. Suponha que lhe seja fornecida uma lista encadeada armazenando números inteiros em ordem crescente. Sua tarefa é remover todos os elementos duplicados da lista. Por exemplo, dada a lista 
# [0 → 1 → 1 → 1 → 5 → 7 → 10 → 10 → None], seu programa deve retornar a lista 
# [0 → 1 → 5 → 7 → 10 → None].

from aula3 import ListaEncadeada

lista = ListaEncadeada()

lista.insere_no_inicio(10)
lista.insere_no_inicio(10)
lista.insere_no_inicio(7)
lista.insere_no_inicio(5)
lista.insere_no_inicio(1)
lista.insere_no_inicio(1)
lista.insere_no_inicio(1)
lista.insere_no_inicio(0)
print(lista)
lista.remove_duplicatas()
print(lista)