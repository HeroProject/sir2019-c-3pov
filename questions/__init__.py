from typing import Optional

from io_mapper.ConversationIO import ConversationIO
from questions.BooleanQuestion import BooleanQuestion
from questions.ClosedQuestion import ClosedQuestion
from questions.Question import Question
from questions.SimpleAnswerQuestion import SimpleAnswerQuestion


class WhatIsYourNameQuestion(SimpleAnswerQuestion):
    def __init__(self, io: ConversationIO, answer: str = None):
        super(WhatIsYourNameQuestion, self).__init__(
            io=io,
            intent='answer_name',
            question='What is your name?',
            answer=answer,
        )

    def _process_answer(self) -> Optional[Question]:
        #   Changed this with reply
        self._io.say('Nice to meet you %s.' % self._get_answer())
        return WhatCanIDoForYouQuestion(self._io)


class WhatCanIDoForYouQuestion(ClosedQuestion):
    def __init__(self, io: ConversationIO):
        super(WhatCanIDoForYouQuestion, self).__init__(
            io=io,
            intent='answer_instruction',
            question='Do you need help with a destination, platform, disruption or do you want to talk to an employee?',
            answer_options=['platform', 'employee', 'destination', 'disruption']
        )

    def _process_answer(self) -> Optional[Question]:
        if not self._validate_answer():
            self._io.say('I didn\'t quite catch that.')
            return WhatCanIDoForYouQuestion(self._io)

        if self._get_answer() == 'platform':
            return PlatformQuestion(io=self._io)
        elif self._get_answer() == 'destination':
            return DestinationQuestion(io=self._io)
        elif self._get_answer() == 'disruption':
            return DestinationQuestion(io=self._io)
        elif self._get_answer() == 'employee':
            self._io.say('You can find an employee at the ticket office.')
            return AnythingElseICanDoQuestion(io=self._io)

        return WhatCanIDoForYouQuestion(io=self._io)


class AnythingElseICanDoQuestion(BooleanQuestion):
    def __init__(self, io: ConversationIO, **args):
        super(AnythingElseICanDoQuestion, self).__init__(
            io=io,
            intent='answer_instruction',
            question='Anything else I can do for you?',
            **args
        )

    def _process_answer(self) -> Optional[Question]:
        if self._get_answer() is None:
            self._io.say('I didn\'t quite catch that')
        elif self._get_answer() == 'no':
            self._io.say('Thank you, and have a nice day.')
            return None
        return AnythingElseICanDoQuestion(io=self._io)


class PlatformQuestion(ClosedQuestion):
    def __init__(self, io: ConversationIO, **args):
        super(PlatformQuestion, self).__init__(
            io=io,
            intent='answer_platform_nr',
            question='Please specify the platform',
            answer_options=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16'],
            **args
        )

    def _process_answer(self) -> Optional[Question]:
        if not self._validate_answer():
            self._io.say('I\'m sorry, but that platform does not exist at this train station')
            return PlatformQuestion(self._io)

        self._io.say('You can find platform %s over there' % self._get_answer())
        return AnythingElseICanDoQuestion(self._io)


class DestinationQuestion(SimpleAnswerQuestion):
    def __init__(self, io: ConversationIO, **args):
        super(DestinationQuestion, self).__init__(
            io=io,
            intent='answer_destination',
            question='Please specify the destination',
            **args
        )

    def _process_answer(self) -> Optional[Question]:
        print('Find Destination')
        return AnythingElseICanDoQuestion(io=self._io)
