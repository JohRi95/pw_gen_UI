import random
import os
import json
import tkinter
import pyperclip
import verschlüsselungsmodul
from tkinter.simpledialog import askstring
from tkinter import ttk, messagebox, filedialog

PW_DICTIONARY_PATH = "password_dict.json"

def check_init():

    if os.path.exists(PW_DICTIONARY_PATH) == True:
        # fragt nach passwort, wenn .json existiert
        pass_from_user = askstring("Enter Password", "Please Enter Password")

        while verschlüsselungsmodul.validate_password(pass_from_user)[0] == False:
            pass_from_user = askstring("Enter Password", "Please Enter Password")

        return verschlüsselungsmodul.validate_password(pass_from_user)[1], pass_from_user

    elif os.path.exists(PW_DICTIONARY_PATH) == False:

        print(False)

        pass_from_user = askstring("Enter Password", "Please Enter Password")
        validation = False

        while validation == False:
            if pass_from_user == askstring("Confirm Password", "Confirm Password"):
                break
            else:
                pass_from_user = askstring("Enter Password", "Please Enter Password")

        with open(PW_DICTIONARY_PATH, "w") as file:
            pw_dictionary = {}
            file.write(json.dumps(pw_dictionary))

        verschlüsselungsmodul.encode_file(pass_from_user)
        verschlüsselungsmodul.validate_password(pass_from_user)

        return verschlüsselungsmodul.validate_password(pass_from_user)[1], pass_from_user

def update_dictionary(pw_dictionary, dict_json="password_dict.json"):

    print(passwort)

    with open(PW_DICTIONARY_PATH, "w") as file:
        file.write(json.dumps(pw_dictionary))

    verschlüsselungsmodul.encode_file(passwort)
    verschlüsselungsmodul.validate_password(passwort)

def item_selected(event):
    for selected_item in password_treeview.selection():
        item = password_treeview.item(selected_item)
        # show a message
        global treeview_item
        treeview_item= item["values"]
        return item['values']

def update_treeview():
    password_treeview.delete(*password_treeview.get_children())
    with open(PW_DICTIONARY_PATH, "r") as file:
        pw_dictionary = verschlüsselungsmodul.validate_password(passwort)[1]
        for key in pw_dictionary:
            password_treeview.insert('', tkinter.END, values=(key, pw_dictionary[key]))

def delete():
    item = str(treeview_item[0])
    if tkinter.messagebox.askyesno("Info", message="Passwort wirklich löschen?") == True:
        pw_dictionary.pop(item)
        update_dictionary(pw_dictionary)
        update_treeview()
        tkinter.messagebox.showinfo("Info", message = f"{item} Passwort gelöscht.")
    else:
        return

def export():
    path = tkinter.filedialog.askdirectory()
    path = f"{path}"
    file_extension = 0
    file_extension_string = ""
    file_name = f"{path}/passwortliste_export{file_extension_string}.txt"

    while os.path.exists(file_name):
        file_extension += 1
        file_extension_string = f" ({file_extension})"
        file_name = f"{path}/passwortliste_export{file_extension_string}.txt"

    with open(PW_DICTIONARY_PATH, "r"):
        pw_dictionary = verschlüsselungsmodul.validate_password(passwort)[1]
        with open(file_name, "a") as export_file:
            for key in pw_dictionary:
                export_file.write(f"{key} : {pw_dictionary[key]}\n")


    tkinter.messagebox.showinfo("Info", message = f"Passwortliste als .txt exportiert:\n"
                                                  f"{file_name}")

def copy():
    item = treeview_item[1]
    pyperclip.copy(item)
    tkinter.messagebox.showinfo("Info", message = f"{treeview_item[0].card_title()} Passwort in Zwischenablage kopiert.")

class spinbox():

    def set_value(self):
        current_val = self.value.get()
        input_dictionary[self.name] = current_val


    def __init__(self, frame, name, row):
        pad = 2
        input_dictionary[name] = 0
        self.name = name
        self.value = tkinter.IntVar()
        self.value.set(input_dictionary[name])
        self.regler = ttk.Spinbox(frame, from_ = 0, to = 100.0, textvariable = self.value, command = self.set_value, state = "readonly")
        self.regler.grid(padx = pad, pady = pad, row = row, column = 1, sticky = "E")
        self.label = tkinter.Label(frame, text = name)
        self.label.grid(padx = pad, pady = pad, row = row, column = 0, sticky = "W")

class button():

    def button_command(self):

        if self.name == "Generate":
            checksum = 0

            # Abfrage der Anzahl an Kleinbuchstaben
            count_lower = input_dictionary["Kleinbuchstaben"]
            checksum += count_lower

            # Abfrage der Anzahl an Großbuchstaben
            count_upper = input_dictionary["Großbuchstaben"]
            checksum += count_upper

            # Abfrage der Anzahl an Sonderzeichen
            count_special = input_dictionary["Sonderzeichen"]
            checksum += count_special

            # Abfrage der Anzahl an Ganzzahlen
            count_number = input_dictionary["Ganzzahlen"]
            checksum += count_number

            #Validiert die Länge (muss mindestens größer 0 sein)
            if checksum <= 0:
                entry_validation = False
            elif checksum <= 20:
                entry_validation = True
                # ---------------------------------- Generator -------------------------------------- #

                # Die Platzhalter "x" sollen durch die zufälligen Zeichen ersetzt werden
                password_charakter_list = [] # Blankliste für Platzhalter

                # Die Positionen werden zufällig aus dieser Liste entnommen
                randomized_positions = [] # Blankoliste für Positionen

                # Erstellt Listen mit Platzhaltern, bzw. Indizes
                for charakter in range(checksum):
                    password_charakter_list.append("x") # Enthält die Platzhalter
                    randomized_positions.append(charakter) # Enthält die Indizes

                # (1) Kleinbuchstaben
                if count_lower > 0:
                    for char in range(0, count_lower):
                        # es wird ein zufälliger Index aus der Positionsliste entnommen und Var zugewiesen
                        rnd_position = randomized_positions[random.randint(0, len(randomized_positions) - 1)]
                        # in Platzhalterliste wird Platzhalter mit zufälligem Kleinbuchstaben aus Alphabetliste getauscht
                        password_charakter_list[rnd_position] = alphabet[random.randint(0, len(alphabet) - 1)]
                        # der Index wird aus der Positionsliste entfernt, um Überschreiben zu verhindern
                        randomized_positions.pop(randomized_positions.index(rnd_position))

                # (2) Großbuchstaben, analog (1), bis auf .upper der Auswahl, um Großbuchstaben zu erzeugen
                if count_upper > 0:
                    for upper in range(0, count_upper):
                        rnd_position = randomized_positions[random.randint(0, len(randomized_positions) - 1)]
                        password_charakter_list[rnd_position] = alphabet[random.randint(0, len(alphabet) - 1)].upper()
                        randomized_positions.pop(randomized_positions.index(rnd_position))

                # (3) Sonderzeichen, analog (1), bis auf Sonderzeichenliste Logik genau gleich
                if count_special > 0:
                    for position in range(0, count_special):
                        rnd_position = randomized_positions[random.randint(0, len(randomized_positions) - 1)]
                        password_charakter_list[rnd_position] = sonderzeichen[random.randint(0, len(sonderzeichen) - 1)]
                        randomized_positions.pop(randomized_positions.index(rnd_position))

                # (4) Zahl, analog (1), bis dass die Methode .randint genutzt wird und int in str wegen .join() Methode
                if count_number > 0:
                    for number in range(0, count_number):
                        rnd_position = randomized_positions[random.randint(0, len(randomized_positions) - 1)]
                        password_charakter_list[rnd_position] = str(random.randint(0, 9))
                        randomized_positions.pop(randomized_positions.index(rnd_position))
                else:
                    # Falls Input nicht stimmt, sonstiger Fehler
                    print("Sonstiger Fehler")

                # Erstellt aus Liste einen String / .join() akzeptiert nur str als Datatype, desw. Umwandlung in (4)
                self.password = "".join(password_charakter_list)
                self.textvar.set(self.password)
                print(self.textvar.get())
                print(self.textvar)
            else:
                tkinter.messagebox.showinfo("Info", message = f"Passwort darf maximal 20 Zeichen lang sein.\n"
                                                              f"Aktuelle Länge: {checksum}")

        elif self.name == "Save as: ":
            password = input_dictionary["Generate"].textvar.get()
            key_name = self.textvar.get()
            if key_name != "" and password != "":
                if len(password) <= 20:
                    if key_name in pw_dictionary:
                        answere = tkinter.messagebox.askokcancel(title = "Info", message = "Key schon vorhanden. Überschreiben?")
                        if answere == True:
                            tkinter.messagebox.showinfo(title = "Info", message = f"Key: {key_name} ersetzt.")
                            pw_dictionary[key_name] = password
                            update_dictionary(pw_dictionary)
                    else:
                        pw_dictionary[key_name] = password
                        update_dictionary(pw_dictionary)
                        tkinter.messagebox.showinfo(title = "Info", message = f"{key_name} und Passwort hinzugefügt.")
                    update_treeview()
                else:
                    tkinter.messagebox.showinfo("Info", message=f"Passwort darf maximal 20 Zeichen lang sein.\n"
                                                                f"Aktuelle Länge: {len(password)}")
            else:
                if password == "":
                    tkinter.messagebox.showinfo("Info", message=f"Keinen Password generiert.")
                elif key_name == "":
                    tkinter.messagebox.showinfo("Info", message=f"Keinen Key eingegeben.")
                else:
                    print("Anderer Fehler")

    def __init__(self, frame, name, column, row):
        pad = 2
        input_dictionary[name] = self
        self.name = name
        self.password = ""
        self.button = tkinter.Button(frame, text = name, command = self.button_command)
        self.button.grid(padx = pad, pady = pad, column = 0, row = row, sticky = "we")

        self.textvar = tkinter.StringVar()
        self.entry_label = tkinter.Entry(export_window, textvariable = self.textvar)
        self.entry_label.grid(padx=2, pady=2, column= 1, row = row, columnspan = 3, sticky = "we")

###################################### Initialisierung ######################################

# Listen um das Passwort zu generieren
alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","n","m","o","p","q","r","s","t","u","v","w","x","y","z"]
sonderzeichen = ["!","§", "$", "%", "&", "/", "=", "?"]
global treeview_item

# Dictionary für das Interface
input_dictionary = {
}

# pw_dictionary = check_init()

# MainWindow
main_window = tkinter.Tk()
main_window.title("PW Manager")
return_check_init = check_init()
pw_dictionary = return_check_init[0]
passwort = return_check_init[1]
print(passwort)
######################################  UI ######################################

# Regler
regel_window = tkinter.LabelFrame(main_window)
regel_window.pack(pady=2, padx=2, fill = "x")

for item in enumerate(["Kleinbuchstaben", "Großbuchstaben", "Sonderzeichen", "Ganzzahlen"]):
    spinbox(frame = regel_window, name = item[1], row = item[0])

# Export
export_window = tkinter.LabelFrame(main_window)
export_window.pack(padx = 2, pady = 2,fill = "x")
export_window.columnconfigure(index = 3, weight = 1)

for item in enumerate(["Generate", "Save as: "]):
    button(export_window, name = item[1], column = item[0], row = item[0])

# Bool um input zu validieren
entry_validation = False

###################################### Treeview Tab ######################################

dict_window = tkinter.LabelFrame(main_window)
dict_window.pack()

dict_window_buttons = tkinter.LabelFrame(main_window)
dict_window_buttons.pack(fill = "x")

for col in [0,1,2,3]:
    dict_window_buttons.columnconfigure(index = col ,weight = 1)

password_treeview_headings = ["Key", "Password"]
password_treeview = ttk.Treeview(dict_window, columns = password_treeview_headings, show = "headings")
password_treeview.grid(column = 0, row =0, pady = 2, padx = 2)

for key in enumerate(password_treeview_headings):
    password_treeview.heading(key[0], text = key[1])

for key in pw_dictionary:
    password_treeview.insert('', tkinter.END, values=(key, pw_dictionary[key]))

password_treeview.bind('<<TreeviewSelect>>', item_selected)

password_treeview.column('Key', width = 75)
password_treeview.column('Password', width = 150)

dict_slider_y = ttk.Scrollbar(dict_window)
dict_slider_y.grid(column = 1, row =0, padx = 2, pady = 2, sticky = "NSE")

delete_button = tkinter.Button(dict_window_buttons, text = "Löschen", command = delete)
delete_button.grid(row = 0, column=4, columnspan=2, padx = 2, pady = 2, sticky = "WE")

export_button = tkinter.Button(dict_window_buttons, text = "Export", command = export)
export_button.grid(row = 0, column=1, padx = 2, pady = 2, sticky = "WE")

copy_button = tkinter.Button(dict_window_buttons, text = "Copy", command = copy)
copy_button.grid(row = 0, column=0, padx = 2, pady = 2, sticky = "WE")

main_window.resizable(width=False, height=False)

main_window.mainloop()
