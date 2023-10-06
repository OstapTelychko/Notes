import json
from project_configuration import ROOT_DIRECTORY

class Session:
    notes = None
    theme = None
    
    #variables for auto-save
    last_note = None
    last_tag = None

    def save_session():
        with open(f"{ROOT_DIRECTORY}/note_data.json", "w", encoding="UTF-8") as file:
            json.dump(Session.notes, file, indent=4, ensure_ascii=False)