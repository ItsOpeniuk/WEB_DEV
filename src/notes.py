from datetime import datetime
import csv
import re


class Note:

    def __init__(self, *data, date=None):
        self.author = data[0]
        self.title = data[1]
        self.note = data[2]
        self.tags = data[3] if len(data) > 3 else None
        self.date = datetime.now().strftime("%d.%m.%Y,%H:%M")

    def change_note(self, field, new_data):
        fields_mapping = {
            "author": "author",
            "title": "title",
            "note": "note",
            "tags": "tags",
            "date": "date"
        }

        if field in fields_mapping:
            if field == 'date':
                # Перевірка є тільки на формат дати
                date_pattermn = re.compile(
                    r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.\d{4},(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9])$")
                if not date_pattermn.math(new_data):
                    raise ValueError(
                        "Invalid date format. Should be DD.MM.YYYY,HH:MM")
            setattr(self, fields_mapping[field], new_data)
        else:
            print(f"Invalid field: {field}")

    def __str__(self):
        tags_str = f"tags: {self.tags}; " if self.tags else ""
        return f"author: {self.author}; title: {self.title}; note: {self.note}; {tags_str}date: {self.date}."


class NoteManager:

    def __init__(self, csv_file=None):
        self.csv_file = csv_file
        self.notes = []
        if csv_file is not None:
            self.load_notes()

    def add_note(self, note):
        self.notes.append(note)
        print("Note added successfully.")

    def remove_note(self, note):
        if note in self.notes:
            self.notes.remove(note)
            print("Note removed successfully.")
        else:
            print("Note not found in the list.")

    def add_tag(self, note, tag):
        if note in self.notes:
            note.tags += ", " + tag
            print("Tag added successfully.")
        else:
            print("Note not found in the list.")

    def search_notes(self, info):
        result = []
        for note in self.notes:
            if info in note.author or info in note.title or info in note.note or info in note.tags or info in note.date:
                result.append(note)
        return result

    def search_notes_by_tags(self, search_tags: str):
        # Користувач вводить через кому теги, ця функція їх розбиває на список
        # і для кожного тегу провводить пошук по нотатках
        search_tag_list = [x.strip() for x in search_tags.split(",")]
        result = set()
        for note in self.notes:
            for tag in search_tag_list:
                if tag in note.tags:
                    result.add(note)
        return result

    def save_notes(self):
        with open("notes_save.csv", "w", newline='') as fd:
            fields = ["author", "title", "note", "tags", "date"]
            writer = csv.DictWriter(fd, fieldnames=fields)
            writer.writeheader()

            for note in self.notes:
                writer.writerow({
                    "author": note.author,
                    "title": note.title,
                    "note": note.note,
                    "tags": note.tags,
                    "date": note.date
                })

    def load_notes(self):
        with open("notes_save.csv", "r") as fd:
            reader = csv.DictReader(fd)
            for row in reader:
                note = Note(
                    row["author"],
                    row["title"],
                    row["note"],
                    row["tags"],
                    date=row["date"]
                )
                self.notes.append(note)

    def clear_notes(self):
        self.notes = []
        print("Notes cleared successfully.")

    def print_notes(self):
        if not self.notes:
            print("No notes available.")
        else:
            for note in self.notes:
                print(note)


# note_manager = NoteManager()

# new_note1 = Note("Person1", "Meeting", "Discuss project progress.", "important", "project")
# note_manager.add_note(new_note1)

# new_note2 = Note("Person2", "Work", "Don't forget about project.", "not so important", "project")
# note_manager.add_note(new_note2)

# new_note3 = Note("Person3", "Walk", "Don't go through the park.", "silly", "outside")
# note_manager.add_note(new_note3)

# new_note4 = Note("Person4", "Shopping", "Buy new coat.", "winter", "clothes")
# note_manager.add_note(new_note4)

# new_note5 = Note("Person5", "Hollyday", "Mayami has cool cafes.", "cafes", date="22.12.2010, 22:59")
# note_manager.add_note(new_note5)

# new_note6 = Note("Person6", "Sleep", "Go to sleep at 11PM.", "important", "sleep")
# note_manager.add_note(new_note6)

# #--------------------------------------------

# print("\nInitial state:")
# note_manager.print_notes()

# #--------------------------------------------

# res = note_manager.search_notes("important")
# print(f"\nSearch result (important):")
# for i in res:
#     print(f"\t- {str(i)}")

# res = note_manager.search_notes("sleep")
# print(f"\nSearch result (sleep):")
# for i in res:
#     print(f"\t- {str(i)}")

# res = note_manager.search_notes("22.12.2010, 22:59")
# print(f"\nSearch result (22.12.2010, 22:59):")
# for i in res:
#     print(f"\t- {str(i)}")

# res = note_manager.search_notes("Don't")
# print(f"\nSearch result (Don't):")
# for i in res:
#     print(f"\t- {str(i)}")

# res = note_manager.search_notes("Person3")
# print(f"\nSearch result (Person3):")
# for i in res:
#     print(f"\t- {str(i)}")

# #--------------------------------------------

# print("\nSearch by tags:")
# res = note_manager.search_notes_by_tags("important, winter")
# print(f"\nSearch result (important, winter):")
# for i in res:
#     print(f"\t- {str(i)}")

# #--------------------------------------------
# note_manager.clear_notes()

# print("\nUpdated state:")
# note_manager.print_notes()
