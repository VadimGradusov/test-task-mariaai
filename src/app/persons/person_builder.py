"""Person builder"""
import os
from src.app.instruments import instruments
from src.app.gpt.request import make


class Expert:
    """Person class"""

    def __init__(self):
        self.__person_type = 'expert'
        self.__message_contents = []

    def __call__(self, situation):
        """Making request to an expert"""
        self.add_message_content('user', situation)
        response = make(self.__message_contents)
        self.add_message_content('assistant', response)
        return response

    def add_message_content(self, usertype: str, content: str):
        """Add message content"""
        self.__message_contents.append({'role': usertype, 'content': content})

    @property
    def person_type(self):
        """Person type"""
        return self.__person_type



class Person:
    """Person class"""
    def __init__(self, expert, person_type):
        self.__expert = expert
        self.__message_contents = []
        self.__person_type = person_type
        self.__cancel_dialog = 0

    def add_message_content(self, usertype: str, content: str):
        """Add message content"""
        self.__message_contents.append({'role': usertype, 'content': content})

    def ask(self, content):
        """Ask person"""
        self.add_message_content('user', content)
        while True:
            response = make(self.__message_contents)
            _response = eval(response)

            situation = f'User tells person: {content}\n' \
                        f'Person answers: {response}\n'
            expert_opinion = self.__expert(situation)
            _expert_opinion = eval(expert_opinion)
            print(f'LOG: {_expert_opinion}\n\n')

            # Expert thinks answer is correct
            if _expert_opinion['correct_answer']:
                self.__cancel_dialog = _expert_opinion['cancel_dialog']
                if _response['instrument']:
                    instruments[self.person_type][_response['instrument']](**_response['kwargs'])
                break

            # If expert thinks answer is not correct cycle continues
            else:
                situation += '\n\nExpert opinion' + _expert_opinion['content']
                self.__message_contents[-1] = {'role': 'user', 'content': situation}
        self.add_message_content('assistant', response)
        return eval(response)['content']

    @property
    def person_type(self):
        """Person type"""
        return self.__person_type

    @property
    def cancel_dialog(self):
        """Cancel dialog"""
        return self.__cancel_dialog


class PersonBuilder:
    """Person builder"""
    def __init__(self, person_type):
        self.person_type = person_type

    def build(self):
        """Build person"""
        expert = Expert()
        self.set_system_prompt(expert, f'{os.getcwd()}/src/resources/'
                                       f'persons/{expert.person_type}/prompts/expert.prompt')

        person = Person(expert, 'alesha')
        self.set_system_prompt(person, f'{os.getcwd()}/src/resources/'
                                       f'persons/{person.person_type}/prompts/person.prompt',
                               f'{os.getcwd()}/src/resources/'
                               f'persons/{person.person_type}/specs/specs.json'
                               )
        return person

    @staticmethod
    def set_system_prompt(person, prompt_path, specs_path=None):
        """Set system prompt"""
        with open(prompt_path, 'r') as file:
            prompt_contents = file.read()
        if specs_path:
            with open(specs_path, 'r') as file:
                prompt_contents += file.read()
        person.add_message_content('system', prompt_contents)
