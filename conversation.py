from typing import Dict, Optional, List


class Question:
    def __init__(self, question: str, expects_intent: bool = False, expects_params: bool = True,
                 intent: str = None, params: Dict[str, any] = None):
        self._question = question
        self._expects_intent = expects_intent
        self._expects_params = expects_params
        self._intent: str = self.set_intent(intent)
        self._params: Dict[str, any] = self.set_params(params)

    def ask_question(self):
        get_intent: bool = self._expects_intent and not self.has_intent()
        get_params: bool = self._expects_params and not self.has_params()
        if get_intent or get_params:
            print(self._question)
            if get_intent:
                self.set_intent(input('Intent: '))

            if get_params:
                # You can replace this with your own logic in that actually accepts multiple params.
                # By default we'll only have answer.
                self.set_params({'answer': input('Answer: ')})

    def has_intent(self) -> bool:
        return self._intent is not None

    def has_params(self) -> bool:
        return self._params is not None

    def set_intent(self, intent: str) -> Optional[str]:
        self._intent = intent.lower().strip() if type(intent) is str else None
        return self._intent

    def set_params(self, params: Dict[str, any] = None):
        self._params = params
        return self._params

    def process_answer(self) -> Optional['Question']:
        pass


class SimpleAnswerQuestion(Question):
    def __init__(self, question: str, answer: str = None):
        super(SimpleAnswerQuestion, self).__init__(
            question=question,
            params={'answer': self.normalize_answer(answer)}
        )

    def normalize_answer(self, answer: str) -> Optional[str]:
        if type(answer) == str:
            answer = answer.strip()
            return answer if len(answer) > 0 else None
        return None

    def get_answer(self):
        return self._params['answer']

    def has_params(self) -> bool:
        return self.get_answer() is not None


class ClosedQuestion(SimpleAnswerQuestion):
    def __init__(self, question: str, answer_options: List[str], answer: str = None):
        self._answer_options = answer_options
        super(ClosedQuestion, self).__init__(
            question=question,
            answer=answer
        )

    def normalize_answer(self, answer: str) -> Optional[str]:
        return super().normalize_answer(answer.lower()) if type(answer) == str else None

    def validate_answer(self) -> bool:
        return self.get_answer() in self._answer_options


class BooleanQuestion(ClosedQuestion):
    def __init__(self, question: str, **args):
        super(BooleanQuestion, self).__init__(
            question=question,
            answer_options=['yes', 'no'],
            **args
        )


class WhatIsYourNameQuestion(SimpleAnswerQuestion):
    def __init__(self, answer: str = None):
        super(WhatIsYourNameQuestion, self).__init__(
            question='What is your name?',
            answer=answer
        )

    def process_answer(self) -> Optional[Question]:
        print('Nice to meet you %s.' % self.get_answer())
        return WhatCanIDoForYouQuestion()


class WhatCanIDoForYouQuestion(Question):
    def __init__(self, intent: str = None, params: Dict[str, any] = None):
        super(WhatCanIDoForYouQuestion, self).__init__(
            question='What can I do for you? (options: locate_platform, find_destination)',
            expects_intent=True,
            intent=intent,
            params=params
        )

    def process_answer(self) -> Optional[Question]:
        if self._intent == 'locate_platform':
            return PlatformQuestion(answer=self._params['answer'])
        elif self._intent == 'find_destination':
            return DestinationQuestion(answer=self._params['answer'])
        else:
            print('I didn\'t quite catch that.')
            return WhatCanIDoForYouQuestion()


class AnythingElseICanDoQuestion(BooleanQuestion):
    def __init__(self, **args):
        super(AnythingElseICanDoQuestion, self).__init__(
            question='Anything else I can do for you?',
            **args
        )

    def process_answer(self) -> Optional[Question]:
        if self.get_answer() == 'yes':
            return WhatCanIDoForYouQuestion()
        return None


class PlatformQuestion(ClosedQuestion):
    def __init__(self, **args):
        super(PlatformQuestion, self).__init__(
            question='Please specify the platform',
            answer_options=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16'],
            **args
        )

    def process_answer(self) -> Optional[Question]:
        # platform is None if it not exists
        if not self.validate_answer():
            print('I\'m sorry, but that platform does not exist at this train station')
            return PlatformQuestion()

        print('You can find platform %s over there' % self.get_answer())
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
