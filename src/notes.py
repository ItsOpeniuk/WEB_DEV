from datetime import datetime


class Note:

    def __init__(self, *data):
        self.author = data[0]
        self.title = data[1]
        self.note = data[2]
        self.tags = data[3:] if len(data) > 3 else None
        self.date = datetime.now().strftime("%a %d %b %Y, %I:%M%p")

    def change_note(self, field, new_data):
        fields_mapping = {
            "author": "author",
            "title": "title",
            "note": "note",
            "date": "date",
            "tags": "tags"
        }

        if field in fields_mapping:
            setattr(self, fields_mapping[field], new_data)
        else:
            print(f"Invalid field: {field}")

    def __str__(self):
        tags_str = f", tags: {', '.join(self.tags)}" if self.tags else ""
        return f"author: {self.author}, title: {self.title}, note: {self.note}, date: {self.date}{tags_str}"


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