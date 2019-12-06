from typing import Optional

from io_mapper.ConversationIO import ConversationIO
from questions.BooleanQuestion import BooleanQuestion
from questions.ClosedQuestion import ClosedQuestion
from questions.Question import Question
from questions.SimpleAnswerQuestion import SimpleAnswerQuestion


class IAmC3POVQuestion(Question):
    def __init__(self, io: ConversationIO):
        super(IAmC3POVQuestion, self).__init__(
            io=io,
            question='Hi, I am C-3-P-O-V. I\'m here to help you with public transport.',
            gesture='wave',
            expects_params=False
        )

    def _process_answer(self) -> Optional[Question]:
        self.talk()
        return WhatCanIDoForYouQuestion(self._io)


class WhatCanIDoForYouQuestion(ClosedQuestion):
    def __init__(self, io: ConversationIO):
        super(WhatCanIDoForYouQuestion, self).__init__(
            io=io,
            intent='answer_instruction',
            question='Do you need help with a destination, platform, disruption or do you want to talk to an employee?',
            gesture='explanation',
            answer_options=['platform', 'employee', 'destination', 'disruption']
        )

    def _process_answer(self) -> Optional[Question]:
        if not self._validate_answer():
            self._io.say('I didn\'t quite catch that.')
            return WhatCanIDoForYouQuestion(io=self._io)

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

        if self._get_answer() in ['1', '2']:
            self._io.move('rarm_forwards')
            self._io.say('Platform %s is straight ahead, at the beginning of the hallway.' % self._get_answer())
        if self._get_answer() in ['3', '4']:
            self._io.move('rarm_forwards')
            self._io.say('Platform %s is straight ahead, the second of this hallway.' % self._get_answer())
        if self._get_answer() in ['5', '6', '7', '8']:
            self._io.move('larm_right')
            self._io.say('Platform %s is on our right, over there.' % self._get_answer())
        if self._get_answer() in ['9', '10', '11', '12']:
            self._io.move('rarm_left')
            self._io.say('Platform %s is on our left, over there.' % self._get_answer())
        if self._get_answer() in ['13', '14']:
            self._io.move('affirmation')
            self._io.say('Platform %s is behind us, the second last of the hallway.' % self._get_answer())
        if self._get_answer() in ['15', '16']:
            self._io.move('affirmation')
            self._io.say('Platform %s is behind us, at the end of the hallway.' % self._get_answer())

        return AnythingElseICanDoQuestion(self._io)


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
        elif self._get_answer() == 'no':
            self._io.move('wave')
            self._io.say('Thank you, and have a nice day.')
            return None

        self._io.move('dont_understand')
        self._io.say('I didn\'t catch that')
        return AnythingElseICanDoQuestion(io=self._io)


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
