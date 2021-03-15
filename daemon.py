import pymongo 
import time
from FormatAllData import FormatAllData

client = pymongo.MongoClient("localhost", 27017)
db = client["legume-choice"]
# Extracting the projects data
cursorCollection =  db["cursors"]

cursor = cursorCollection.find(cursor_type = pymongo.CursorType.TAILABLE_AWAIT)
while cursor.alive:
    try:
        doc = cursor.next()
        print(doc)
        print("New entry added")
        FormatAllData()
    except StopIteration:
        time.sleep(1)

