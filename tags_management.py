from GUI import MainWindow
from Session import Session


def select_tag():
    if MainWindow.tag_field.text() == "Виберіть тег":
        MainWindow.tag_field.setText("")
    Session.last_tag = MainWindow.tags_list.selectedItems()[0].text()


def add_tag():
    if Session.last_note is not None:
        if  MainWindow.tag_field.text() != "":
            key = Session.last_note
            tag = MainWindow.tag_field.text()

            if tag not in Session.notes[key]["Теги"]:
                Session.notes[key]["Теги"].append(tag)               
                MainWindow.tags_list.addItem(tag)
                MainWindow.tag_field.clear()
                Session.save_session()
            else:
                MainWindow.tag_field.setText("Такий тег вже існує")
        else:
            MainWindow.tag_field.setText("Вкажіть назву тегу")
    if Session.last_note is None:
        MainWindow.tag_field.setText("Виберіть нотатку")


def delete_tag():
    if MainWindow.notes_list.selectedItems():
        if Session.last_tag is not None:
            key = Session.last_note
            tag = Session.last_tag

            Session.notes[key]["Теги"].remove(tag)
            MainWindow.tags_list.clear()
            MainWindow.tags_list.addItems(Session.notes[key]["Теги"])
            Session.last_tag = None
            Session.save_session()
        else:
            MainWindow.tag_field.setText("Спочатку виберіть тег")


def rename_tag():
    if Session.last_tag is not None and Session.last_note is not None:
        old_name = Session.last_tag
        if MainWindow.tag_field.text() != "":
            new_name = MainWindow.tag_field.text()
            index=Session.notes[Session.last_note]["Теги"].index(old_name)
            Session.notes[Session.last_note]["Теги"][index] = new_name

            MainWindow.tags_list.clear()
            MainWindow.tags_list.addItems(Session.notes[Session.last_note]["Теги"])

            Session.last_tag = None
            MainWindow.tag_field.setText("")
            Session.save_session()
        else:
            MainWindow.tag_field.setText("Введіть нову назву тега")
    elif Session.last_note is None:
        MainWindow.tag_field.setText("Перше виберіть нотатку")
    else:
        MainWindow.tag_field.setText("Виберіть тег")