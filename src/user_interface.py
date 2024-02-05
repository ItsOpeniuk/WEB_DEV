from abc import ABC, abstractmethod


class UserInterface(ABC):
    @abstractmethod
    def display_user_contacts(self, user_contacts):
        pass

    @abstractmethod
    def display_user_notes(self, user_notes):
        pass

    @abstractmethod
    def display_user_commands(self, user_commands):
        pass


class WebUserInterface(UserInterface):
    def display_user_contacts(self, user_contacts):
        pass

    def display_user_notes(self, user_notes):
        pass

    def display_user_commands(self, user_commands):
        pass


class ConsoleUserInterface(UserInterface):

    def display_user_contacts(self, user_contacts):
        pass

    def display_user_notes(self, user_notes):
        pass

    def display_user_commands(self, user_commands):
        pass
