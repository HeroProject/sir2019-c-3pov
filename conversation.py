import string
from typing import Dict, Optional, Union, List


class Question:
    def __init__(self, question: string, expects_intent: bool = False, expects_params: bool = True,
                 intent: string = None, params: Dict[string, any] = None):
        self._question = question
        self._expects_intent = expects_intent
        self._expects_params = expects_params
        self._intent: string = self.set_intent(intent)
        self._params: Dict[string, any] = self.set_params(params)

    def ask_question(self):
        if self._expects_intent and not self._intent:
            self.set_intent(input('Intent: '))

        if self._expects_params and not self._params:
            # You can replace this with your own logic in that actually accepts multiple params.
            # By default we'll only have answer.
            self.set_params({'answer': input('Answer: ')})

    def set_intent(self, intent: string):
        self._intent = intent.lower().strip()
        return self._intent

    def set_params(self, params: Dict[string, any] = None):
        self._params = params
        return self._params

    def process_answer(self) -> Optional['Question']:
        pass


class SimpleAnswerQuestion(Question):
    def __init__(self, question: string, answer: string = None):
        super(SimpleAnswerQuestion, self).__init__(
            question=question,
            params={'answer': self.parse_answer(answer)}
        )

    def parse_answer(self, answer: string) -> string:
        if type(answer) == str:
            answer = answer.strip()
            return answer if len(answer) > 0 else None
        return None

    def get_answer(self):
        return self._params['answer']


class ClosedQuestion(SimpleAnswerQuestion):
    def __init__(self, question: string, answer_options: List[Union[string, int]], answer: string = None):
        self._answer_options = answer_options
        super(ClosedQuestion, self).__init__(
            question=question,
            answer=answer
        )

    def parse_answer(self, answer: string) -> string:
        answer = super().parse_answer(answer.lower())
        return answer if answer in self._answer_options else None


class YesNoQuestion(ClosedQuestion):
    def __init__(self, question: string, **args):
        super(YesNoQuestion, self).__init__(
            question=question,
            answer_options=['yes', 'no'],
            **args
        )


class WhatIsYourNameQuestion(Question):
    def __init__(self, params: Dict[string, any] = None):
        super(WhatIsYourNameQuestion, self).__init__(
            question='What is your name?',
            params=params
        )

    def process_answer(self) -> Optional[Question]:
        print('Nice to meet you %s.' % self._params)
        return WhatCanIDoForYouQuestion()


class WhatCanIDoForYouQuestion(Question):
    def __init__(self, intent: string = None, params: Dict[string, any] = None):
        super(WhatCanIDoForYouQuestion, self).__init__(
            question='What can I do for you?',
            expects_intent=True,
            intent=intent,
            params=params
        )

    def process_answer(self) -> Optional[Question]:
        if self._intent == 'locate_platform':
            return PlatformQuestion(answer=self._params)
        elif self._intent == 'find_destination':
            return DestinationQuestion(answer=self._params)
        else:
            print('I didn\'t quite catch that.')
            return WhatCanIDoForYouQuestion()


class AnythingElseICanDoQuestion(YesNoQuestion):
    def __init__(self, answer: string = None):
        super(AnythingElseICanDoQuestion, self).__init__(
            question='Anything else I can do for you?',
            answer=answer
        )

    def process_answer(self) -> Optional[Question]:
        if self.get_answer() == 'yes':
            return WhatCanIDoForYouQuestion()
        return None


class PlatformQuestion(ClosedQuestion):
    def __init__(self, **args):
        super(PlatformQuestion, self).__init__(
            question='Please specify the platform',
            answer_options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
            **args
        )

    def parse_answer(self, answer: string) -> int:
        return int(super().parse_answer(answer))

    def process_answer(self) -> Optional[Question]:
        platform = self.get_answer()

        # platform is None if it not exists
        if not platform:
            print('I\'m sorry, but that platform does not exist at this train station')

        print('You can find platform %s ')
        return AnythingElseICanDoQuestion()


class DestinationQuestion(SimpleAnswerQuestion):
    def __init__(self, **args):
        super(DestinationQuestion, self).__init__(
            question='Please specify the destination',
            **args
        )

    def process_answer(self) -> Optional[Question]:
        print('Find Destination')
        return AnythingElseICanDoQuestion()


q = WhatIsYourNameQuestion()
while q is not None:
    q.ask_question()
    q = q.process_answer()
