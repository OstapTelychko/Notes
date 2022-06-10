from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
        QApplication, QWidget, 
        QListWidget,QLineEdit, QFormLayout,
        QHBoxLayout, QVBoxLayout,   
        QPushButton, QLabel,QTextEdit,QInputDialog)
import json


#variables for auto-save
last_note = None
last_tag = None


app = QApplication([])

#app icon
icon = QIcon("Notes.ico")

#interface
main_win = QWidget()
main_win.setWindowTitle("Розумні замітки")
main_win.resize(900, 600)
main_win.setWindowIcon(icon)

list_notes = QListWidget()
list_notes_label = QLabel("Список заміток")

button_note_create = QPushButton("Створити замітку")
button_note_del = QPushButton("Видалити замітку")
button_note_save = QPushButton("Зберегти замітку")

field_tag = QLineEdit("")
field_tag.setPlaceholderText("Введіть текст")
field_text = QTextEdit()

button_tag_add = QPushButton("Додати тег до замітки")
button_tag_del = QPushButton("Відкріпити тег від замітки")
button_tag_search = QPushButton("Шукати замітки по тегу")

list_tag = QListWidget()
list_tag_label = QLabel("Список тегів")

add_note = QLineEdit()

layout_notes =QHBoxLayout()
col_1 = QVBoxLayout()
col_2 = QVBoxLayout()

col_1.addWidget(field_text)

col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)

col_2.addWidget(add_note)

row1 = QHBoxLayout()
row1.addWidget(button_note_create)
row1.addWidget(button_note_del)
row2 = QHBoxLayout()
row2.addWidget(button_note_save)

col_2.addLayout(row1)
col_2.addLayout(row2)

col_2.addWidget(list_tag_label)
col_2.addWidget(list_tag)
col_2.addWidget(field_tag)

row3 = QHBoxLayout()
row3.addWidget(button_tag_add)
row3.addWidget(button_tag_del)
row4 = QHBoxLayout()
row4.addWidget(button_tag_search)

col_2.addLayout(row3)
col_2.addLayout(row4)

layout_notes.addLayout(col_1,stretch=2)
layout_notes.addLayout(col_2,stretch=1)

main_win.setLayout(layout_notes)

with open ("Notes/note_data.json","r",encoding="UTF-8") as file:
    notes = json.load(file)
list_notes.addItems(notes)

def create_note():
    global last_note
    if last_note != None:
        save_note()
        add_note.setPlaceholderText("Введіть назву замітки")
        list_tag.clear()
        last_note = None
    else:
        add_note.setPlaceholderText("Введіть назву замітки і збережіть")
        add_note.setText("")
def save_note():
    if add_note.text() != "" and  last_note == None:
        notes[add_note.text()]= {"Текст":"","Теги":[]}
        list_tag.clear()
        field_text.setText("")
        list_notes.addItem(add_note.text())
        add_note.setText("")
        with open ("note_data.json","w",encoding="UTF-8") as file:
            json.dump(notes,file)
    else:
        key = last_note
        notes[key]["Текст"]=field_text.toPlainText()
        with open("Notes/note_data.json","w",encoding="UTF-8") as file:
            json.dump(notes,file)


def show_note():
    #gains the text from the note and displays it
    global last_note
    if last_note != None and notes[last_note]["Текст"] != field_text.toPlainText():
        save_note()
        key = list_notes.selectedItems()[0].text()
        field_text.setText(notes[key]["Текст"])
        list_tag.clear()
        list_tag.addItems(notes[key]["Теги"])
        last_note = key
    else:
        key = list_notes.selectedItems()[0].text()
        field_text.setText(notes[key]["Текст"])
        list_tag.clear()
        list_tag.addItems(notes[key]["Теги"])
        last_note = key

def del_note():
    if list_notes.selectedItems():
        key = last_note
        del notes[key]
        list_notes.clear()
        list_tag.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open("note_data.json","w",encoding="UTF-8") as file:
            json.dump(notes,file)
        last_note = None

def add_tag():
    if last_note !=None and field_tag.text() != "":
        key = last_note
        tag = field_tag.text()
        field_tag.setPlaceholderText("")
        if tag not in notes[key]["Теги"]:
            notes[key]["Теги"].append(tag)               
            list_tag.addItem(tag)
            field_tag.clear()
        with open("note_data.json","w",encoding="UTF-8") as file:
            json.dump(notes,file)
    if field_tag.text() == "":
        field_tag.setPlaceholderText("Вкажіть назву тегу")


def del_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tag.selectedItems()[0].text()
        notes[key]["Теги"].remove(tag)
        list_tag.clear()
        list_tag.addItems(notes[key]["Теги"])
        with open("note_data.json","w",encoding="UTF-8") as file:
            json.dump(notes,file)
        last_tag = None

def search_note():
    tag = field_tag.text()
    field_tag.setPlaceholderText("Введіть текст")
    if button_tag_search.text() == "Шукати замітки по тегу" and tag != "":
        notes_filtered = []
        for note in notes:
            for tags in notes[note]["Теги"]:
                if tag in tags:
                    notes_filtered.append(note)
        button_tag_search.setText("Очистити пошук")
        list_notes.clear()
        list_tag.clear()
        list_notes.addItems(notes_filtered)
    elif button_tag_search.text() == "Очистити пошук":
        notes_filtered = []
        list_notes.clear()
        list_notes.addItems(notes)
        list_tag.clear()
        if last_note != None:
            save_note()
        field_tag.clear()
        button_tag_search.setText("Шукати замітки по тегу")
    else:
        if tag == "":
            field_tag.setPlaceholderText("Вкажіть назву тегу для пошуку")

def last_tag():
    global last_tag
    last_tag = list_tag.selectedItems()[0].text()

def main():
    button_tag_search.clicked.connect(search_note)
    button_note_del.clicked.connect(del_note)
    button_tag_del.clicked.connect(del_tag)
    button_tag_add.clicked.connect(add_tag)
    button_note_create.clicked.connect(create_note)
    button_note_save.clicked.connect(save_note)
    list_notes.itemClicked.connect(show_note)
    list_tag.itemClicked.connect(last_tag)
    main_win.show()
    app.exec()

if __name__ == "__main__":
    main()