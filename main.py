from GUI import *
from Session import Session
from notes_management import save_note, create_note, delete_note, show_note, rename_note, search_note
from tags_management import add_tag, delete_tag, select_tag, rename_tag

import json



def change_theme():
    # with open(f"{ROOT_DIRECTORY}/theme.json","r",encoding="utf-8") as file:
    #     Session.theme = json.load(file)

    if Session.theme["theme"] == "white":
        MainWindow.change_theme.setIcon(DARK_THEME_ICON)
        MainWindow.window.setStyleSheet(DARK_THEME)
        Session.theme["theme"] = "black"
    else:
        MainWindow.change_theme.setIcon(LIGHT_THEME_ICON)
        Session.theme["theme"] = "white"
        MainWindow.window.setStyleSheet(LIGHT_THEME)

    with open(f"{ROOT_DIRECTORY}/theme.json","w",encoding="utf-8") as file:
        json.dump(Session.theme, file, indent=4, ensure_ascii=False)


def main():
    #Load user configuration
    with open(f"{ROOT_DIRECTORY}/theme.json","r",encoding="utf-8") as file:
        Session.theme = json.load(file)

    #Load theme
    if Session.theme["theme"] == "black":
        MainWindow.window.setStyleSheet(DARK_THEME)
        MainWindow.change_theme.setIcon(DARK_THEME_ICON)
    else:
        MainWindow.window.setStyleSheet(LIGHT_THEME)
        MainWindow.change_theme.setIcon(LIGHT_THEME_ICON)

    #Change theme
    MainWindow.change_theme.clicked.connect(change_theme)

    #Load notes
    with open (f"{ROOT_DIRECTORY}/note_data.json","r",encoding="UTF-8") as file:
        Session.notes = json.load(file)
    MainWindow.notes_list.addItems(Session.notes)

    #Notes management
    MainWindow.delete_note.clicked.connect(delete_note)
    MainWindow.create_note.clicked.connect(create_note)
    MainWindow.save_note.clicked.connect(save_note)
    MainWindow.rename_note.clicked.connect(rename_note)
    MainWindow.notes_list.itemClicked.connect(show_note)

    #Tags management
    MainWindow.find_by_tag.clicked.connect(search_note)
    MainWindow.delete_tag.clicked.connect(delete_tag)
    MainWindow.add_tag.clicked.connect(add_tag)
    MainWindow.rename_tag.clicked.connect(rename_tag)
    MainWindow.tags_list.itemClicked.connect(select_tag)

    MainWindow.window.show()
    app.exec()

if __name__ == "__main__":
    main()