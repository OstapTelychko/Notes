from GUI import MainWindow
from Session import Session
   


def save_note():
    if MainWindow.add_or_rename_note.text() != "" and Session.last_note == None:
        if MainWindow.add_or_rename_note.text() not in Session.notes:
            Session.notes[MainWindow.add_or_rename_note.text()]= {"Текст":"","Теги":[]}
            MainWindow.tags_list.clear()
            MainWindow.text_field.setText("")

            MainWindow.notes_list.addItem(MainWindow.add_or_rename_note.text())
            MainWindow.add_or_rename_note.setText("")
            Session.save_session()
        else:
            MainWindow.add_or_rename_note.setText("Така нотатка вже існує")
    elif Session.last_note is not None:
        key = Session.last_note
        Session.notes[key]["Текст"]=MainWindow.text_field.toPlainText()
        Session.save_session()


def create_note():
    if Session.last_note != None:
        save_note()
        MainWindow.tags_list.clear()
        Session.last_note = None
    if MainWindow.add_or_rename_note.text() != "":
        save_note()
    else:
        MainWindow.add_or_rename_note.setText("Введіть назву нотатки")


def delete_note():
    if MainWindow.notes_list.selectedItems():
        key = Session.last_note
        del Session.notes[key]

        MainWindow.notes_list.clear()
        MainWindow.tags_list.clear()
        MainWindow.text_field.clear()
        MainWindow.notes_list.addItems(Session.notes)
        Session.last_note = None
        Session.save_session()
    else:
        MainWindow.add_or_rename_note.setText("Виберіть нотатку")


def show_note():
    if Session.last_note != None and Session.notes[Session.last_note]["Текст"] != MainWindow.text_field.toPlainText():
        save_note()
        key = MainWindow.notes_list.selectedItems()[0].text()
        MainWindow.text_field.setText(Session.notes[key]["Текст"])
        MainWindow.tags_list.clear()
        MainWindow.tags_list.addItems(Session.notes[key]["Теги"])
    else:
        key = MainWindow.notes_list.selectedItems()[0].text()
        MainWindow.text_field.setText(Session.notes[key]["Текст"])
        MainWindow.tags_list.clear()
        MainWindow.tags_list.addItems(Session.notes[key]["Теги"])
        MainWindow.tag_field.setText("")
        if MainWindow.add_or_rename_note.text() == "Виберіть нотатку":
            MainWindow.add_or_rename_note.setText("")
    Session.last_note = key


def rename_note():

    if Session.last_note is not None:
        old_name = Session.last_note
        if MainWindow.add_or_rename_note.text() != "":
            new_name = MainWindow.add_or_rename_note.text()
            dict_with_renamed_note = dict()
            for key,value in Session.notes.items():
                dict_with_renamed_note[key.replace(old_name,new_name)] = value
            Session.notes = dict_with_renamed_note

            MainWindow.notes_list.clear()
            MainWindow.notes_list.addItems(Session.notes)
            MainWindow.add_or_rename_note.setText("")
            Session.last_note = new_name
            Session.save_session()
        else:
            MainWindow.add_or_rename_note.setText("Введіть нову назву")
    else:
        MainWindow.add_or_rename_note.setText("Виберіть нотатку")


def search_note():
    if MainWindow.find_by_tag.text() == "Шукати нотатки по тегу" and MainWindow.tag_field.text() != "Введіть назву бажаного тега":
        if MainWindow.tag_field.text() != "":
            tag = MainWindow.tag_field.text()
            MainWindow.tag_field.clear()

            filtered_notes = []
            for note in Session.notes:
                for tags in Session.notes[note]["Теги"]:
                    if tag in tags:
                        filtered_notes.append(note)

            MainWindow.find_by_tag.setText("Очистити пошук")
            MainWindow.notes_list.clear()
            MainWindow.tags_list.clear()
            MainWindow.notes_list.addItems(filtered_notes)
        else:
            MainWindow.tag_field.setText("Введіть назву бажаного тега")
    else:
        if MainWindow.find_by_tag.text() == "Очистити пошук":
            filtered_notes = []
            MainWindow.notes_list.clear()
            MainWindow.notes_list.addItems(Session.notes)
            MainWindow.tags_list.clear()

            if Session.last_note != None:
                save_note()

            MainWindow.tag_field.clear()
            MainWindow.find_by_tag.setText("Шукати нотатки по тегу")