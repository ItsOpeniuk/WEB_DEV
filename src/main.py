from classes import Record, AddressBook
from sorter import sorter
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit.styles import Style


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Contact"
        except TypeError:
            return "Invalid input. Please check your input."
    return wrapper
@input_error
def handle_hello():
    return "How can I help you?"
@input_error
def handle_add(name, phone):
    if name not in ADDRESS_BOOK.data.keys():
        record = Record(name)
        try:
            record.add_phone(phone)
            ADDRESS_BOOK.add_record(record)
            return f"Contact {name} added with phone number {phone}"
        except ValueError:
            return "Invalid phone"
    else:
        record = ADDRESS_BOOK.find(name)
        try:
            record.add_phone(phone)
            return f"Phone number {phone} added for contact {name}"
        except ValueError:
            return "Invalid phone"
@input_error
def handle_change(name, old_phone, new_phone):
    record = ADDRESS_BOOK.find(name)
    if record is not None:
        try:
            record.edit_phone(old_phone, new_phone)
            return f"Phone number for contact {name} changed to {new_phone}"
        except ValueError:
            return "Invalid phone"
    else:
        raise KeyError
@input_error
def handle_set_birthday(name, day):
    record = ADDRESS_BOOK.find(name)
    if record is not None:
        try:
            record.set_birthday(day)
            return f"Birthday for contact {name} is set to {day}"
        except ValueError:
            return "Please enter the date in DD.MM.YYYY format."
    else:
        raise KeyError
@input_error
def days_to_birthday(name):
    record = ADDRESS_BOOK.find(name)
    if record is not None:
        return record.days_to_birthday()
    else:
        raise KeyError
@input_error
def handle_delete(name):
    record = ADDRESS_BOOK.find(name)
    if record is not None:
        ADDRESS_BOOK.delete(name)
        return f"{name} deleted"
    else:
        raise KeyError
@input_error
def handle_phone(name):
    record = ADDRESS_BOOK.find(name)
    if record is not None:
        return record
    else:
        raise KeyError
@input_error
def handle_show_all():
    if len(ADDRESS_BOOK.data) == 0:
        raise KeyError
    else:
        all = []
        for record in ADDRESS_BOOK.data.values():
            all.append(str(record))
        return "\n".join(res for res in all)
@input_error
def handle_search(query):
    return ADDRESS_BOOK.search(query)
DEFAULT_FILE = "new_book.csv"
@input_error
def handle_open(csv_file=None):
    global ADDRESS_BOOK, DEFAULT_FILE
    if csv_file is None:
        csv_file = DEFAULT_FILE
    try:
        ADDRESS_BOOK = AddressBook(csv_file)
        DEFAULT_FILE = csv_file
        return f"Address book opened from {csv_file}"
    except FileNotFoundError:
        try:
            ADDRESS_BOOK = AddressBook(DEFAULT_FILE)
            return f"File not found. Address book opened from {DEFAULT_FILE}"
        except FileNotFoundError:
            ADDRESS_BOOK = AddressBook(None)
            return "Starting with an empty address book."
@input_error
def handle_save(csv_file=None):
    global ADDRESS_BOOK, DEFAULT_FILE
    if csv_file is None:
        csv_file = DEFAULT_FILE
        if ADDRESS_BOOK.csv_file is None:
            # Якщо ADDRESS_BOOK створено без файлу, тобто AddressBook(None), то зберегти за замовченням
            ADDRESS_BOOK.csv_file = csv_file
            ADDRESS_BOOK.save_to_disk()
            return f"Address book saved to {DEFAULT_FILE}"
        else:
            # Якщо ADDRESS_BOOK має вказаний файл, то перезаписати його
            ADDRESS_BOOK.save_to_disk()
            return f"Address book saved to {ADDRESS_BOOK.csv_file}"
    else:
        ADDRESS_BOOK.csv_file = csv_file
        ADDRESS_BOOK.save_to_disk()
        return f"Address book saved to {ADDRESS_BOOK.csv_file}"


def show_help():
    help_message = """
        Доступні команди:
        hello: Вивести вітальне повідомлення.
        open [ім'я_файлу]: Відкрити адресну книгу з вказаного файлу або останнього відкритого файлу.
        save [ім'я_файлу*]: Зберегти поточну адресну книгу *без вказівки файлу збереже в поточний.
        add [іʼмя] [телефон]: Додати новий контакт до адресної книги.
        change [іʼмя] [старий телефон] [новий телефон]: Змінити дані існуючого контакту.
        info [іʼмя]: Вивести інформацію про контакт.
        show all: Відобразити всі контакти в адресній книзі.
        set birthday [іʼмя] [дата]: Встановити день народження для контакту.
        days to birthday [іʼмя]: Розрахувати кількість днів до наступного дня народження для контакту.
        delete [іʼмя]: Видалити контакт з адресної книги.
        search [запит]: Пошук в адресній книзі за символами.
        sort: Сортує необхідну папку.
        """
    return help_message
COMMANDS = {
    "help": show_help,
    "hello": handle_hello,
    "open": handle_open,
    "save": handle_save,
    "add": handle_add,
    "change": handle_change,
    "info": handle_phone,
    "show all": handle_show_all,
    "set birthday": handle_set_birthday,
    "days to birthday": days_to_birthday,
    "delete": handle_delete,
    "search": handle_search,
    "sort": sorter
}

command_list = ['help', 'hello', 'open', 'save', 'add', 'change',
                'info', 'show all', 'set birthday', 'days to birthday',
                'delete', 'search', 'sort']

custom_style = Style.from_dict({
    'prompt': 'bg:#708090 #ffffff',
    'completion-menu.completion': 'bg:#708090 #ffffff',
    'completion-menu.completion.current': 'bg:#ffffff #2E8B57',
    'completion-menu.border': 'bg:#008000 #ffffff',
})

completer = FuzzyWordCompleter(command_list)


def get_user_input():
    return prompt('Enter a command: ', completer=completer, style=custom_style).lower()


@input_error
def main():
    global ADDRESS_BOOK
    handle_open()

    while True:
        user_input = get_user_input()
        if user_input in ["good bye", "close", "exit"]:
            print(handle_save())
            print("Good bye!")
            break
        for command in COMMANDS.keys():
            if user_input.startswith(command):
                args = user_input[len(command):].split()
                print(COMMANDS[command](*args))
                break
        else:
            print("Unknown command. Please try again.")


if __name__ == "__main__":
    main()