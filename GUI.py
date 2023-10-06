from PyQt6.QtCore import Qt,QSize, QCoreApplication
from PyQt6.QtGui import QIcon,QColor
from PyQt6.QtWidgets import QApplication, QWidget,QListWidget,QLineEdit,QHBoxLayout, QVBoxLayout,QPushButton, QLabel,QTextEdit,QToolButton
from qdarktheme._style_loader import load_stylesheet, load_palette #pip install pyqtdarktheme
from qdarktheme import setup_theme
from project_configuration import ROOT_DIRECTORY


app = QApplication([])
#app icon
APP_ICON = QIcon(f"{ROOT_DIRECTORY}/Images/Notes.ico")

LIGHT_THEME_ICON = QIcon(f"{ROOT_DIRECTORY}/Images/Light theme.png")
LIGHT_THEME = load_stylesheet(theme="light", custom_colors={"background":"#ebeef0","foreground":"#191a1b"})
LIGHT_THEME +="QPushButton[class=button]{background:rgb(230,230,230)}QPushButton[class=button]:hover{background:rgb(210, 210, 210)}"

DARK_THEME_ICON = QIcon(f"{ROOT_DIRECTORY}/Images/Dark theme.png")
DARK_THEME = load_stylesheet(theme="dark")

HCENTER = Qt.AlignmentFlag.AlignHCenter
VCENTER = Qt.AlignmentFlag.AlignVCenter


def create_button(text:str) -> QPushButton:
    button = QPushButton(text=text)
    button.setProperty("class", "button")
    return button


class MainWindow():
    #interface
    window = QWidget()
    window.setWindowTitle("Розумні нотатки")
    window.resize(900, 600)
    window.setWindowIcon(APP_ICON)

    notes_list = QListWidget()
    notes_list.setMinimumHeight(400)
    list_notes_label = QLabel("Список нотаток")

    create_note = create_button("Створити нотатку")
    delete_note = create_button("Видалити нотатку")
    save_note = create_button("Зберегти нотатку")
    save_note.setMinimumWidth(200)
    rename_note = create_button("Переназвати нотатку")
    rename_note.setMinimumWidth(200)

    tag_field = QLineEdit("")
    tag_field.setPlaceholderText("Вкажіть назву тегу")
    text_field = QTextEdit()

    add_tag = create_button("Додати тег до нотатки")
    delete_tag = create_button("Відкріпити тег від нотатки")
    find_by_tag = create_button("Шукати нотатки по тегу")
    find_by_tag.setMinimumWidth(150)
    rename_tag = create_button("Перназвати тег")
    rename_tag.setMinimumWidth(150)

    tags_list = QListWidget()
    tags_list_label = QLabel("Список тегів")

    add_or_rename_note = QLineEdit()
    add_or_rename_note.setPlaceholderText("Введіть назву нотатки")

    change_theme = QToolButton()
    change_theme.setIconSize(QSize(30,30))


    note_text_area = QVBoxLayout()
    note_text_area.addWidget(text_field)

    notes_management = QVBoxLayout()
    notes_management.addWidget(change_theme, alignment=Qt.AlignmentFlag.AlignRight |Qt.AlignmentFlag.AlignTop)
    notes_management.addWidget(list_notes_label)
    notes_management.addWidget(notes_list)
    notes_management.addWidget(add_or_rename_note)

    row1 = QHBoxLayout()
    row1.addWidget(create_note)
    row1.addWidget(delete_note)

    notes_management.addLayout(row1)
    notes_management.addWidget(rename_note, alignment=HCENTER)
    notes_management.addWidget(save_note, alignment=HCENTER)

    notes_management.addWidget(tags_list_label)
    notes_management.addWidget(tags_list)
    notes_management.addWidget(tag_field)

    row2 = QHBoxLayout()
    row2.addWidget(add_tag)
    row2.addWidget(delete_tag)

    notes_management.addLayout(row2)
    notes_management.addWidget(rename_tag, alignment=HCENTER)
    notes_management.addWidget(find_by_tag, alignment=HCENTER)


    main_layout =QHBoxLayout()
    main_layout.addLayout(note_text_area,stretch=2)
    main_layout.addSpacing(15)
    main_layout.addLayout(notes_management,stretch=1)

    window.setLayout(main_layout)