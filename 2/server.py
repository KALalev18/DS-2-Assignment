from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xml.etree.ElementTree as ET
import threading
import requests
import datetime
import os

# XML File to store notes
XML_FILE = "notes.xml"

# Create XML structure if it does not exist or is empty
def init_xml():
    if not os.path.exists(XML_FILE) or os.stat(XML_FILE).st_size == 0:
        root = ET.Element("notes")
        tree = ET.ElementTree(root)
        tree.write(XML_FILE, xml_declaration=True, encoding='utf-8', method='xml')

init_xml()

class Server:

    # handle multiple requests at once

    def __init__(self):
        self.lock = threading.Lock()
    
    # Add a note to the XML database

    def add_note(self, topic, text):
        timestamp = datetime.datetime.now().isoformat()
        with self.lock:
            tree = ET.parse(XML_FILE)
            root = tree.getroot()
            
            # If the topic exists on the XML, the data will be appended to the structure

            topic_element = root.find(f".//topic[@name='{topic}']")
            if topic_element is None:
                topic_element = ET.SubElement(root, "topic", name=topic) # If not, a new XML entry will be made
            
            # Topic, Text, and timestamp for the note

            note = ET.SubElement(topic_element, "note")
            ET.SubElement(note, "text").text = text
            ET.SubElement(note, "timestamp").text = timestamp
            
            tree.write(XML_FILE, xml_declaration=True, encoding='utf-8', method='xml')
        return f"Note added to topic '{topic}'."
    
    # Get the contents of the XML database based on given topic
    # Data is saved on a xml file, acting as a database
    def get_notes(self, topic):
        with self.lock:
            try:
                tree = ET.parse(XML_FILE)
                root = tree.getroot()
                topic_element = root.find(f".//topic[@name='{topic}']")
                
                if topic_element is None:
                    return f"No notes found for topic '{topic}'."
                
                notes = []
                for note in topic_element.findall("note"):
                    text = note.find("text").text
                    timestamp = note.find("timestamp").text
                    notes.append(f"timestamp: {timestamp}, text: {text}")

                return "\n".join(notes)
            except ET.ParseError:
                return "Error: Unable to parse XML file. It may be corrupted."
    
    # Query wikipedia for user submitted articles - using GET protocol to parse API response and returns Wikipedia link for the first search result

    def fetch_wikipedia(self, topic):
        url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={topic}&limit=1&format=json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if len(data) > 1 and data[1]:
                link = data[3][0] if data[3] else "No link found."
                self.add_note(topic, f"Wikipedia link: {link}")
                return f"Wikipedia link: {link}"
        return "Failed to fetch Wikipedia data."


server = SimpleXMLRPCServer(("localhost", 8000), requestHandler=SimpleXMLRPCRequestHandler, allow_none=True)
server.register_instance(Server())
print("Notebook RPC Server running on port 8000...")
server.serve_forever()


