from typing import Optional, Dict

from questions.BooleanQuestion import BooleanQuestion
from questions.ClosedQuestion import ClosedQuestion
from questions.Question import Question
from questions.SimpleAnswerQuestion import SimpleAnswerQuestion
from io_mapper.ConversationIO import ConversationIO


class WhatIsYourNameQuestion(SimpleAnswerQuestion):
    def __init__(self, io: ConversationIO, answer: str = None):
        super(WhatIsYourNameQuestion, self).__init__(
            io=io,
            question='What is your name?',
            answer=answer,
        )

    def _process_answer(self) -> Optional[Question]:
        #   Changed this with reply
        self._io.say('Nice to meet you %s.' % self._get_answer())
        return WhatCanIDoForYouQuestion(self._io)


class WhatCanIDoForYouQuestion(Question):
    def __init__(self, io: ConversationIO, intent: str = None, params: Dict[str, any] = None):
        super(WhatCanIDoForYouQuestion, self).__init__(
            io=io,
            question='What can I do for you? (options: locate_platform, find_destination)',
            expects_intent=True,
            intent=intent,
            params=params
        )

    def _process_answer(self) -> Optional[Question]:
        if self._intent == 'locate_platform':
            return PlatformQuestion(io=self._io, answer=self._params['answer'])
        elif self._intent == 'find_destination':
            return DestinationQuestion(io=self._io, answer=self._params['answer'])
        else:
            self._io.say('I didn\'t quite catch that.')
            return WhatCanIDoForYouQuestion(self._io)


class AnythingElseICanDoQuestion(BooleanQuestion):
    def __init__(self, io: ConversationIO, **args):
        super(AnythingElseICanDoQuestion, self).__init__(
            io=io,
            question='Anything else I can do for you?',
            **args
        )

    def _process_answer(self) -> Optional[Question]:
        if self._get_answer() == 'yes':
            return WhatCanIDoForYouQuestion(io=self._io)
        self._io.say('Thank you, and have a nice day.')
        return None


class PlatformQuestion(ClosedQuestion):
    def __init__(self, io: ConversationIO, **args):
        super(PlatformQuestion, self).__init__(
            io=io,
            question='Please specify the platform',
            answer_options=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16'],
            **args
        )

    def _process_answer(self) -> Optional[Question]:
        if not self._validate_answer():
            #   Changed accordingly to support robot
            self._io.say('I\'m sorry, but that platform does not exist at this train station')
            return PlatformQuestion(self._io)
        #   Changed to interface w/ robot
        self._io.say('You can find platform %s over there' % self._get_answer())
        return AnythingElseICanDoQuestion(self._io)


class DestinationQuestion(SimpleAnswerQuestion):
    def __init__(self, io: ConversationIO, **args):
        super(DestinationQuestion, self).__init__(
            io=io,
            question='Please specify the destination',
            **args
        )

    def _process_answer(self) -> Optional[Question]:
        print('Find Destination')
        return AnythingElseICanDoQuestion(io=self._io)
