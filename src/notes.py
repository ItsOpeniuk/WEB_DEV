from datetime import datetime
import csv


class Note:

    def __init__(self, *data, date=None):
        self.author = data[0]
        self.title = data[1]
        self.note = data[2]
        self.tags = data[3:] if len(data) > 3 else None
        self.date = datetime.now().strftime("%a %d %b %Y, %I:%M%p") if date is None else date

    def change_note(self, field, new_data):
        fields_mapping = {
            "author": "author",
            "title": "title",
            "note": "note",
            "tags": "tags",
            "date": "date"
        }

        if field in fields_mapping:
            setattr(self, fields_mapping[field], new_data)
        else:
            print(f"Invalid field: {field}")

    def __str__(self):
        tags_str = f"tags: {', '.join(self.tags)}, " if self.tags else ""
        return f"author: {self.author}, title: {self.title}, note: {self.note}, {tags_str}date: {self.date}"


class NoteManager:

    def __init__(self):
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)
        print("Note added successfully.")

    def remove_note(self, note):
        if note in self.notes:
            self.notes.remove(note)
            print("Note removed successfully.")
        else:
            print("Note not found in the list.")

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
                tegs_list = row["tags"].split(",") if row["tags"] else []
                note = Note(
                    row["author"],
                    row["title"],
                    row["note"],
                    *tegs_list,
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

# new_note = Note("John Doe", "Meeting", "Discuss project progress.", "important", "project")
# note_manager.add_note(new_note)

# print("\nInitial state:")
# note_manager.print_notes()

# note_manager.remove_note(new_note)

# print("\nUpdated state:")
# note_manager.print_notes()