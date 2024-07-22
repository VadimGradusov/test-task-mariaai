"""main"""
from src.app.persons.person_builder import PersonBuilder


person = PersonBuilder('alesha').build()
print(person.ask('Start dialog'))
while not person.cancel_dialog:
    print(person.ask(input('User (you): ')))

from src.app.gpt.token_counter import TOKENS
print('Потрачено токенов за сеанс: ' + TOKENS)
