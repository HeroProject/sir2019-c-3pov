'''
what's your name
where are you going
'''
import string
from typing import List, Dict, Union, Optional


class Question:
    def __init__(self, question: string):
        self._question = question
        self._answer: string = None

    def ask_question(self):
        print(self._question)
        self._answer = input()

    def process_answer(self) -> Optional['Question']:
        pass


class WhatIsYourNameQuestion(Question):
    def __init__(self):
        super(WhatIsYourNameQuestion, self).__init__('What is your name?')

    def process_answer(self) -> Optional[Question]:
        print('Nice to meet you %s.' % self._answer)
        return WhatCanIDoForYouQuestion()


class WhatCanIDoForYouQuestion(Question):
    def __init__(self):
        super(WhatCanIDoForYouQuestion, self).__init__('What can I do for you?')

    def process_answer(self) -> Optional[Question]:
        if self._answer == 'locate_platform':
            return locate_platform()
        elif self._answer == 'find_destination':
            return find_destination()
        else:
            print('I didn\'t quite catch that.')
            return WhatCanIDoForYouQuestion()


class AnythingElseICanDoQuestion(Question):
    def __init__(self):
        super(AnythingElseICanDoQuestion, self).__init__('Anything else I can do for you?')

    def process_answer(self) -> Optional[Question]:
        if self._answer == 'yes':
            return WhatCanIDoForYouQuestion()
        return None


def locate_platform() -> Optional[Question]:
    print('Locate Platform')
    return AnythingElseICanDoQuestion()


def find_destination():
    print('Find Destination')
    return AnythingElseICanDoQuestion()


question = WhatIsYourNameQuestion()
while question is not None:
    question.ask_question()
    question = question.process_answer()
