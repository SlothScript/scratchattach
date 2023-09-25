# Imports
import scratchattach as scratch3
from json import dumps
from time import sleep

f = open("Save Data.json", "r")
# Import data from json table
saveData = f.read()
try:
    saveData = eval(saveData)
except Exception as e:
    saveData = {}
    print(e)
f.close()

def Encode(string):
    encoded = ""
    for i in string.lower():
        if i == " ":
            encoded += "9"
        elif i == "a":
            encoded += "1"
        elif i == "b":
            encoded += "2"
        elif i == "c":
            encoded += "3"
        elif i == "d":
            encoded += "4"
        elif i == "e":
            encoded += "5"
        elif i == "f":
            encoded += "6"
        elif i == "g":
            encoded += "7"
        elif i == "h":
            encoded += "81"
        elif i == "i":
            encoded += "82"
        elif i == "j":
            encoded += "83"
        elif i == "k":
            encoded += "84"
        elif i == "l":
            encoded += "85"
        elif i == "m":
            encoded += "86"
        elif i == "n":
            encoded += "87"
        elif i == "o":
            encoded += "881"
        elif i == "p":
            encoded += "882"
        elif i == "q":
            encoded += "883"
        elif i == "r":
            encoded += "884"
        elif i == "s":
            encoded += "885"
        elif i == "t":
            encoded += "886"
        elif i == "u":
            encoded += "887"
        elif i == "v":
            encoded += "8881"
        elif i == "w":
            encoded += "8882"
        elif i == "x":
            encoded += "8883"
        elif i == "y":
            encoded += "8884"
        elif i == "z":
            encoded += "8885"
    return encoded

def Decode(string):
    decoded = ""
    i = 0
    while i != len(string):
        c = string[i]
        if c == "9":
            decoded += " "
        elif c == "1":
            decoded += "a"
        elif c == "2":
            decoded += "b"
        elif c == "3":
            decoded += "c"
        elif c == "4":
            decoded += "d"
        elif c == "5":
            decoded += "e"
        elif c == "6":
            decoded += "f"
        elif c == "7":
            decoded += "g"
        elif c == "8":
            c = string[i + 1]
            if c == "1":
                decoded += "h"
            elif c == "2":
                decoded += "i"
            elif c == "3":
                decoded += "j"
            elif c == "4":
                decoded += "k"
            elif c == "5":
                decoded += "l"
            elif c == "6":
                decoded += "m"
            elif c == "7":
                decoded += "n"
            elif c == "8":
                c = string[i + 2]
                if c == "1":
                    decoded += "o"
                elif c == "2":
                    decoded += "p"
                elif c == "3":
                    decoded += "q"
                elif c == "4":
                    decoded += "r"
                elif c == "5":
                    decoded += "s"
                elif c == "6":
                    decoded += "t"
                elif c == "7":
                    decoded += "u"
                elif c == "8":
                    c = string[i + 3]
                    if c == "1":
                        decoded += "v"
                    elif c == "2":
                        decoded += "w"
                    elif c == "3":
                        decoded += "x"
                    elif c == "4":
                        decoded += "y"
                    elif c == "5":
                        decoded += "z"
                    i += 1
                i += 1
            i += 1
        i += 1
    return decoded

def exclude(string, amount):
    returnValue = ""
    for i in range(len(string)):
        if i >= amount:
            returnValue += string[i]
    return returnValue

def toBinCSV(obj_list):
    final = ""
    try:
        for item in obj_list:
            final += exclude(str(bin(int(item))), 2) + "8"
    except:
        pass
    return final

def fromBinCSV(CSVBinString):
    final = []
    iteration = 0
    toAdd = ""
    for chara in CSVBinString:
        if chara == "8":
            final.append(int(toAdd, 2))
            toAdd = ""
        else:
            toAdd += chara
    return final

def toCSV(obj_list):
    final = ""
    try:
        for item in obj_list:
            print(item)
            final += item + "|"
    except:
        pass
    return final

def fromCSV(CSVString):
    final = []
    iteration = 0
    toAdd = ""
    for chara in CSVString:
        if chara == "|":
            final.append(toAdd)
            toAdd = ""
        else:
            toAdd += chara
    return final

def main():
    # Online cloud game
    PID = "810110876"
    session = scratch3.login("slothdoodles","Enter Password")
    conn = session.connect_cloud(PID)
    events = scratch3.CloudEvents(PID)
    @events.event
    def on_set(event): # When variable set. Uses: event.user (the user); event.var (the variable set); event.value (what it was set to); event.timestamp (when it happened);
        #print(f"{event.user} set the variable {event.var} to the value {event.value} at {event.timestamp}")
        print("Var set: " + event.var + ". Value set to: " + event.value)
        if event.var == "ACTION" and event.value == "1":
            # Save
            conn.set_var("ACTION", "-1")
            print("Save BINLIST: " + str(fromBinCSV(scratch3.get_var(PID, "CSV Save"))))
            saveData[event.user] = fromBinCSV(scratch3.get_var(PID, "CSV Save")) # ["412","72"]
            print(f"SaveData for {event.user}: " + str(saveData[event.user]))
            conn.set_var("Process Finished", "1")
            print(f"Action: SAVE. From: {event.user}")
        if event.var == "ACTION" and event.value == "2":
            # Load
            try:
                SaveList = []
                saveList = saveData.get(event.user)
                for i in saveList:
                    SaveList.append(i)
                conn.set_var("ACTION", "-1")
                conn.set_var("CSV Save",toBinCSV(SaveList))
            except:
                pass
            sleep(0.01)
            conn.set_var("Process Finished", "1")
            print(f"Action: LOAD. From: {event.user}. Process must be finished to start the loading.")
            sleep(5)
        if event.var == "ACTION" and event.value == "3":
            # Save to JSON (Every time someone clicks the internal save button. AKA: nobody but paranoid people. And me. Should be quick)
            conn.set_var("ACTION", "-1")
            with open("Save Data.json", "w") as f:
                f.write(dumps(saveData))
            conn.set_var("Process Finished", "1")
            print(f"Action: INTERNAL SAVE. From: {event.user}")
    
    events.start()
if __name__ == "__main__":
    main()
