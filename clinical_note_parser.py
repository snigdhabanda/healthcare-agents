import xml.etree.ElementTree as ET

class ClinicalNoteParser:
    
    """
    Reads an xml file of notes for a single patient. 
    Returns a list of medical notes for that patient in plain text. 
    """
    def parse(self, note):

        # parse the xml file
        tree = ET.parse(note)
        data = tree.getroot().find("TEXT").text

        # split the notes for a single patient 
        delimiter = "".join(["*"] * 100)
        filtered_data = data.split(delimiter)

        #drop last part of note
        return filtered_data[:-1]
    

