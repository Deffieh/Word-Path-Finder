
from multiprocessing import Queue, Process

from tkinter import filedialog as fd
import customtkinter as ctk

from graph.graph_handler import generate_graph

class FinestraGrafica(ctk.CTk):
  WIDTH = 635
  HEIGHT = 450

  def __init__(self):
    super().__init__()
    self.parole = {}

    self.title("Progetto 2")
    self.geometry(f"{FinestraGrafica.WIDTH}x{FinestraGrafica.HEIGHT}")
    self.resizable(False, False)  # Imposta la dimensione non ridimensionabile

    self.frame = self.build_frame(self)
    self.frame.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)

    self.label_title = ctk.CTkLabel(master=self.frame, text="Progetto IUM", font=("Calibri", -30, "bold"))
    self.label_title.grid(row=0, column=0, pady=10, padx=5, sticky="nw")
    self.label_info = ctk.CTkLabel(master=self.frame, text="", font=("Calibri", -20, "bold"), text_color=("red"))
    self.label_info.grid(row=5, column=0, columnspan=5, sticky="n", padx=10, pady=10)

    self.create_dictionary_section()
    self.create_rules_section()
    self.create_words_section()

    self.progressbar = ctk.CTkProgressBar(master=self.frame, mode="indeterminate")
    self.progressbar.grid(row=6, column=0, columnspan=13, sticky="ew", padx=2, pady=15)

  @staticmethod
  def build_frame(master, **kwargs):
    frame = ctk.CTkFrame(master=master, **kwargs)
    frame.grid_columnconfigure(0 , weight=1)
    frame.grid_rowconfigure(1 , weight=1)
    return frame

  def create_dictionary_section(self):
    self.dictionary_frame = ctk.CTkFrame(master=self.frame)
    self.dictionary_frame.grid(row=1, column=0, pady=0, padx=10, sticky="nsw")

    self.dictionary_label = ctk.CTkLabel(master=self.dictionary_frame, text="Dictionary: ", font=("Calibri", -20, "bold"))
    self.dictionary_label.grid(row=0, column=0, pady=10, padx=5, sticky="nw")

    self.number_word_label = ctk.CTkLabel(master=self.dictionary_frame, text="words: 0")
    self.number_word_label.grid(row=1, column=0, pady=10, padx=20, sticky="nw")

    self.dictionary_botton = ctk.CTkButton(master=self.dictionary_frame, text="Select dictionary", command=self.file_picker)
    self.dictionary_botton.grid(row=3, column=0, pady=5, padx=20, sticky="sw")

  def create_words_section(self):
    self.words_frame = ctk.CTkFrame(master=self.frame)
    self.words_frame.grid(row=1, column=2, pady=0, padx=10, sticky="nsw")

    self.label_words = ctk.CTkLabel(master=self.words_frame, text="Words:", font=("Calibri", -20, "bold"))
    self.label_words.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="nw")

    self.first_word = ctk.CTkEntry(master=self.words_frame, width=150, placeholder_text="Enter word 1")
    self.first_word.grid(row=1, column=0, columnspan=5, pady=10, padx=5)

    self.second_word = ctk.CTkEntry(master=self.words_frame, width=150, placeholder_text="Enter word 2")
    self.second_word.grid(row=2, column=0, columnspan=5, pady=10, padx=5)

    self.confirm_button = ctk.CTkButton(master=self.words_frame, width=150, text="Confirm", command=self.on_confirm)
    self.confirm_button.grid(row=3, column=0, columnspan=2, pady=10, padx=20)

  def create_rules_section(self):
    self.rules_frame = ctk.CTkFrame(master=self.frame)
    self.rules_frame.grid(row=1, column=4, rowspan=4, pady=0, padx=20, sticky="nsew")

    self.rule_label = ctk.CTkLabel(master=self.rules_frame, text="Rules: ", font=("Calibri", -20, "bold"))
    self.rule_label.grid(row=0, column=0, pady=10, padx=10, sticky="nw")

    rules = [ "Anagram", "Char at the begin", "Char at the end", "Char in between", "Char replace"]
    self.rule_checkbox = {}
    for i, rule_text in enumerate(rules, start=1):
      self.rule_checkbox[i] = ctk.CTkCheckBox(master=self.rules_frame, text=rule_text)
      self.rule_checkbox[i].grid(row=i, column=0 , pady=10, padx=20, sticky="w")

  def file_picker(self):
    self.file_path = fd.askopenfilename(title="Select file", filetypes=[("Text files", "*.txt")])
    self.parole.clear();
    try:
      with open(self.file_path, "r") as file:
        for linea in file:
          parola = linea.strip().lower()
          if parola.strip():
            self.parole[parola] = True
        self.number_word_label.configure(text=f"words: {len(self.parole)}")
    except FileNotFoundError:
      self.number_word_label.configure(text="Retry")
    except IOError:
      self.number_word_label.configure(text="Retry pls")

  def get_rules(self):
    rules = []
    for i in range(1, 6):
      if self.rule_checkbox[i].get():
        rules.append(True)
      else:
        rules.append(False)
    return  rules

  def check_all_compiled(self, rules: list, w1: str, w2:str) -> bool:
    self.label_info.configure(text="",text_color=("red"))
    if len(self.parole) == 0:
      self.label_info.configure(text="Error: No dictionary selected or no words on dictionary")
      return False
    elif w1=="" or w2=="":
      self.label_info.configure(text="Error: One or more words are empty")
      return False
    elif w1 == w2:
      self.label_info.configure(text="Error: Words are the same")
      return False
    elif all(x == False for x in rules):
      self.label_info.configure(text="Error: No rules selected")
      return False
    return True

  def on_confirm(self):
    rules = self.get_rules()
    word1 = self.first_word.get().strip().lower()
    word2 = self.second_word.get().strip().lower()
    parole = self.parole.copy()

    if not self.check_all_compiled(rules, word1, word2):
      return

    self.progressbar.start()
    queue = Queue()
    self.p = Process(target=generate_graph, args=(queue, parole, rules, word1, word2))
    self.p.start()

    while queue.empty():
      self.update()
    self.progressbar.stop()

    finded:bool = queue.get()
    if finded:
      self.label_info.configure(text="Drawing graph..",text_color=("green"))
    else:
      self.label_info.configure(text="No path found..")
