from multiprocessing import Queue

import networkx as nx
import itertools

import matplotlib.pyplot as plt

def generate_graph(q: Queue, parole: dict, rules: list, w1: str, w2: str):
  graph = nx.Graph()
  global wordset , anagrams
  anagrams = {}
  wordset = set(parole.keys())
  for word in parole.keys():
      graph.add_node(word)
      anagrams.setdefault(''.join(sorted(word)), []).append(word)

  add_selected_word(graph, w1, wordset)
  add_selected_word(graph, w2, wordset)
  build_edges(graph, rules)

  if not nx.has_path(graph, w1, w2):
    q.put_nowait(False)
    return
  q.put_nowait(True)

  path = nx.shortest_path(graph, source=w1, target=w2)
  path_graph = nx.Graph()
  path_graph.add_nodes_from(path)
  for i in range(len(path) - 1):
    path_graph.add_edge(path[i], path[i + 1])

  # Disegna il grafo
  nx.draw(path_graph, with_labels=True, node_color='lightblue', edge_color='gray')
  # Visualizza il grafico in una finestra separata
  plt.show()

def add_selected_word(graph: nx.Graph, word: str, wordset:set):
  word = word.strip().lower()
  if word not in graph.nodes():
    graph.add_node(word)
    wordset.add(word)
    anagrams.setdefault(''.join(sorted(word)), []).append(word)

def build_edges(graph: nx.Graph, rules:list[bool]):
  if rules[0]: #Anagram
    for anagram_group in anagrams.values():
      for word1, word2 in itertools.combinations(anagram_group, 2):
        graph.add_edge(word1, word2, weight=1)

  for word in wordset:
    word_variations = all_combination(word, rules)
    words_on_dictionary = filter_by_dictionary(word_variations, word)
    for w, weight in words_on_dictionary:
      graph.add_edge(word, w, weight=weight)
      #graph.add_edges_from([(word, w, {'weight': weight}) for w, weight in words_on_dictionary])

def filter_by_dictionary(word_variations: set, word:str):
  return set((w, val)
              for w, val in word_variations
                    if w in wordset and w != word)

# Generate all word variation from rules
def all_combination(word: str, rules: list[bool]) -> set:
  word_variations = set()

  letters = "abcdefghijklmnopqrstuvwxyz"

  #   0              1              2              3              4              5          len == 5
  #[('', 'hello'), ('h', 'ello'), ('he', 'llo'), ('hel', 'lo'), ('hell', 'o'), ('hello', '')]
  word_splitted = [(word[:i], word[i:]) for i in range(len(word) + 1)]
  if rules[1]: # Begin
    insert_begin = [(c + word_splitted[0][1], 2) for c in letters]
    word_variations.update(insert_begin)
  if rules[2]:  # End
    insert_end = [(word_splitted[len(word_splitted) - 1][0] + c, 2) for c in letters]
    word_variations.update(insert_end)
  if rules[3]: # between
    inserts_inbetween = [(L + c + R, 3) for L, R in word_splitted[1:len(word_splitted) - 1] for c in letters]
    word_variations.update(inserts_inbetween)
  if rules[4]: # replace
    replaces = [(L + c + R[1:], 3) for L, R in word_splitted[1:len(word_splitted) - 1] for c in letters]
    word_variations.update(replaces)
  return word_variations



