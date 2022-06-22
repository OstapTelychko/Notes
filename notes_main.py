from ctypes import alignment
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon,QColor
from PyQt5.QtWidgets import (
        QApplication, QWidget, 
        QListWidget,QLineEdit, QFormLayout,
        QHBoxLayout, QVBoxLayout,   
        QPushButton, QLabel,QTextEdit,QInputDialog)
import json

def find_file(file):
    "Return path to file"
    Path = os.path.join(os.environ.get("_MEIPASS2",os.path.abspath(".")),file).replace("\\","/")
    return Path

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
button_note_save.setMinimumWidth(200)
button_note_rename = QPushButton("Переназвати замітку")
button_note_rename.setMinimumWidth(200)

field_tag = QLineEdit("")
field_tag.setPlaceholderText("Вкажіть назву тегу")
field_text = QTextEdit()
field_text.setTextColor(QColor(255,56,67))

button_tag_add = QPushButton("Додати тег до замітки")
button_tag_del = QPushButton("Відкріпити тег від замітки")
button_tag_search = QPushButton("Шукати замітки по тегу")
button_tag_search.setMinimumWidth(150)
button_tag_rename = QPushButton("Перназвати тег")
button_tag_rename.setMinimumWidth(150)

list_tag = QListWidget()
list_tag_label = QLabel("Список тегів")

add_note_or_rename = QLineEdit()
add_note_or_rename.setPlaceholderText("Введіть назву замітки")

layout_notes =QHBoxLayout()
col_1 = QVBoxLayout()
col_2 = QVBoxLayout()

col_1.addWidget(field_text)

col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
col_2.addWidget(add_note_or_rename)

row1 = QHBoxLayout()
row1.addWidget(button_note_create)
row1.addWidget(button_note_del)

col_2.addLayout(row1)
col_2.addWidget(button_note_rename,alignment=Qt.AlignHCenter)
col_2.addWidget(button_note_save,alignment=Qt.AlignHCenter)

col_2.addWidget(list_tag_label)
col_2.addWidget(list_tag)
col_2.addWidget(field_tag)

row2 = QHBoxLayout()
row2.addWidget(button_tag_add)
row2.addWidget(button_tag_del)

col_2.addLayout(row2)
col_2.addWidget(button_tag_rename,alignment=Qt.AlignHCenter)
col_2.addWidget(button_tag_search,alignment=Qt.AlignHCenter)

layout_notes.addLayout(col_1,stretch=2)
layout_notes.addLayout(col_2,stretch=1)

main_win.setLayout(layout_notes)

with open (find_file("note_data.json"),"r",encoding="UTF-8") as file:
    notes = json.load(file)
list_notes.addItems(notes)

def create_note():
    global last_note
    if last_note != None:
        save_note()
        list_tag.clear()
        last_note = None
    if add_note_or_rename.text() != "":
        save_note()
def save_note():
    if add_note_or_rename.text() != "" and last_note == None:
        if add_note_or_rename.text() not in notes:
            notes[add_note_or_rename.text()]= {"Текст":"","Теги":[]}
            list_tag.clear()
            field_text.setText("")
            list_notes.addItem(add_note_or_rename.text())
            add_note_or_rename.setText("")
            with open (find_file("note_data.json"),"w",encoding="UTF-8") as file:
                json.dump(notes,file,indent=4,ensure_ascii=False)
        else:
            add_note_or_rename.setText("Така нотатка вже існує")
    else:
        key = last_note
        notes[key]["Текст"]=field_text.toPlainText()
        with open(find_file("note_data.json"),"w",encoding="UTF-8") as file:
            json.dump(notes,file,indent=4,ensure_ascii=False)
def show_note():
    #gains the text from the note and displays it
    global last_note
    if last_note != None and notes[last_note]["Текст"] != field_text.toPlainText():
        save_note()
        key = list_notes.selectedItems()[0].text()
        field_text.setText(notes[key]["Текст"])
        list_tag.clear()
        list_tag.addItems(notes[key]["Теги"])
    else:
        key = list_notes.selectedItems()[0].text()
        field_text.setText(notes[key]["Текст"])
        list_tag.clear()
        list_tag.addItems(notes[key]["Теги"])
    last_note = key
def del_note():
    global last_note
    if list_notes.selectedItems():
        key = last_note
        del notes[key]
        list_notes.clear()
        list_tag.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open(find_file("note_data.json"),"w",encoding="UTF-8") as file:
            json.dump(notes,file,indent=4,ensure_ascii=False)
        last_note = None
def add_tag():
    if last_note !=None and field_tag.text() != "":
        key = last_note
        tag = field_tag.text()
        if tag not in notes[key]["Теги"]:
            notes[key]["Теги"].append(tag)               
            list_tag.addItem(tag)
            field_tag.clear()
            with open(find_file("note_data.json"),"w",encoding="UTF-8") as file:
                json.dump(notes,file,indent=4,ensure_ascii=False)
        else:
            field_tag.setText("Такий тег вже існує")
    if last_note is None:
        field_tag.setText("Виберіть нотатку")
    else:
        if field_tag.text() == "":
            field_tag.setText("Вкажіть назву тегу")
def del_tag():
    global last_tag
    if list_notes.selectedItems():
        if last_tag is not None:
            key = last_note
            tag = last_tag
            notes[key]["Теги"].remove(tag)
            list_tag.clear()
            list_tag.addItems(notes[key]["Теги"])
            with open(find_file("note_data.json"),"w",encoding="UTF-8") as file:
                json.dump(notes,file,indent=4,ensure_ascii=False)
            last_tag = None
        else:
            field_tag.setText("Перше виберіть тег")
def search_note():
    if field_tag.text() != "":
        tag = field_tag.text()
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
    else:
        field_tag.setText("Введіть назву шукаємого тега")
    if button_tag_search.text() == "Очистити пошук":
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
def select_tag():
    global last_tag
    last_tag = list_tag.selectedItems()[0].text()
def rename_note():
    global last_note,notes
    if last_note is not None:
        old_name = last_note
        if add_note_or_rename.text() != "":
            new_name = add_note_or_rename.text()
            new_notes = dict()
            for key,value in notes.items():
                new_notes[key.replace(old_name,new_name)] = value
            notes = new_notes
            list_notes.clear()
            list_notes.addItems(notes)
            with open(find_file("note_data.json"),"w",encoding="utf-8") as file:
                json.dump(notes,file,indent=4,ensure_ascii=False)
            add_note_or_rename.setText("")
            last_note = new_name
        else:
            add_note_or_rename.setText("Введіть нову назву")
    else:
        add_note_or_rename.setText("Виберіть нотатку")

def main():
    button_tag_search.clicked.connect(search_note)
    button_note_del.clicked.connect(del_note)
    button_tag_del.clicked.connect(del_tag)
    button_tag_add.clicked.connect(add_tag)
    button_note_create.clicked.connect(create_note)
    button_note_save.clicked.connect(save_note)
    button_note_rename.clicked.connect(rename_note)
    list_notes.itemClicked.connect(show_note)
    list_tag.itemClicked.connect(select_tag)
    main_win.show()
    app.exec()

if __name__ == "__main__":
    main()