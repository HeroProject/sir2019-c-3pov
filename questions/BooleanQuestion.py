from questions.ClosedQuestion import ClosedQuestion
from io_mapper.ConversationIO import ConversationIO


class BooleanQuestion(ClosedQuestion):
    def __init__(self, io: ConversationIO, question: str, **args):
        super(BooleanQuestion, self).__init__(
            io=io,
            question=question,
            answer_options=['yes', 'no', 'maybe'],
            **args
        )

    def _process_answer(self):
        if not self._validate_answer() or self._get_answer() == 'maybe':
            self._io.say('I didn\'t quite catch that.')
            return self
        return None
