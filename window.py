from tkinter import Button, Label, Entry, Frame, Tk, Text, WORD, W, NO, END
import tkinter.ttk as ttk

from nlp import parser
import numpy as np

class MainWindow:
    def __init__(self):
        self.root = Tk()
        vocabulary = []
        self.rows = 0

        space0 = Label(self.root)
        inputFrame = Frame(self.root, bd=2)
        self.inputText = Text(inputFrame, height=10, width=130, wrap=WORD)
        createVocabularyButton = Button(inputFrame, text='Создать словарь по тексту', width=55, height=2, bg='grey')

        space1 = Label(self.root)
        vocabularyFrame = Frame(self.root, bd=2)
        self.vocabularyTree = ttk.Treeview(vocabularyFrame, columns=("Лексема", "Форма слова", "Информация"),
                                           selectmode='browse',
                                           height=11)
        self.vocabularyTree.heading('Лексема', text="Лексема", anchor=W)
        self.vocabularyTree.heading('Форма слова', text="Форма слова", anchor=W)
        self.vocabularyTree.heading('Информация', text="Информация", anchor=W)
        self.vocabularyTree.column('#0', stretch=NO, minwidth=0, width=0)
        self.vocabularyTree.column('#1', stretch=NO, minwidth=347, width=347)
        self.vocabularyTree.column('#2', stretch=NO, minwidth=347, width=347)
        self.vocabularyTree.column('#3', stretch=NO, minwidth=347, width=347)

        space2 = Label(self.root, text='\n')
        addingFrame = Frame(self.root, bg='grey', bd=5)
        self.posAddingLabel = Label(addingFrame, text=' Словаформа: ', width=14, height=2, bg='grey', fg='white')
        self.formAddingEntry = Entry(addingFrame, width=23)
        endingsAddingLabel = Label(addingFrame, text=' Тэги: ', width=10, height=2, bg='grey', fg='white')
        self.tagAddingEntry = Entry(addingFrame, width=50)
        space21 = Label(addingFrame, text='          ', bg='grey')
        addButton = Button(addingFrame, text='Добавить', width=8, height=2, bg='grey')

        createVocabularyButton.config(command=self.create_vocabulary)
        addButton.config(command=self.add_vocabulary)

        space0.pack()
        inputFrame.pack()
        self.inputText.pack()
        createVocabularyButton.pack(side='left')
        space1.pack()
        vocabularyFrame.pack()
        self.vocabularyTree.pack()
        space2.pack()
        addingFrame.pack()

        self.posAddingLabel.pack(side='left')
        self.posAddingLabel.pack(side='left')
        self.formAddingEntry.pack(side='left')
        endingsAddingLabel.pack(side='left')
        self.tagAddingEntry.pack(side='left')

        space21.pack(side='left')
        addButton.pack(side='left')

        self.lexemes = []
        self.forms = []
        self.count = []
        self.infos = []

    def clear_vocabulary(self):
        self.lexemes = []
        self.forms = []
        self.infos = []
        self.count = []


    def clear_table(self):
        self.vocabularyTree.delete(*self.vocabularyTree.get_children())

    def create_vocabulary(self):
        self.clear_vocabulary()
        self.clear_table()

        self.update_vocabulary()
        self.update_table()

    def add_vocabulary(self):
        if self.formAddingEntry.get() != "" and self.tagAddingEntry.get() != "":
            index = np.where(np.array(self.forms) == self.formAddingEntry.get())[0]
            if len(index) != 0:
                index = index.item()
                self.infos[index] = self.tagAddingEntry.get()

        self.clear_table()
        self.update_table()

    def update_vocabulary(self):
        text = self.inputText.get(1.0, END).replace('\n', '')
        self.vocabularyTree.delete(*self.vocabularyTree.get_children())
        for lexeme in parser(text):
            # Increase number
            count = lexeme[1]['count']
            if lexeme[0] in self.lexemes:
                unique, counts = np.unique(self.lexemes, return_counts=True)
                occ_dict = dict(zip(unique, counts))
                count = int(occ_dict[lexeme[0]]) + 1

            elif lexeme[0] in self.forms:
                unique, counts = np.unique(self.forms, return_counts=True)
                occ_dict = dict(zip(unique, counts))
                count = int(occ_dict[lexeme[0]]) + 1

            self.lexemes.append(lexeme[0])
            self.forms.append(lexeme[1]['word_form'])
            self.infos.append(lexeme[1]['tag'])
            self.count.append(count)



    def update_table(self):
        rows = len(self.vocabularyTree.get_children())
        for i in range(len(self.lexemes)):
            self.vocabularyTree.insert('', 'end', values=(self.lexemes[i], self.forms[i] + ' ' + str(self.count[i]), self.infos[i]), iid=rows)
            rows += 1

    def start(self):
        self.root.mainloop()


if __name__ == '__main__':
    window = MainWindow()
    window.start()
