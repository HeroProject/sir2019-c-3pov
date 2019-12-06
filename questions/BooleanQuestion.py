from .ClosedQuestion import ClosedQuestion


class BooleanQuestion(ClosedQuestion):
    def __init__(self, **args):
        super(BooleanQuestion, self).__init__(
            answer_options=['yes', 'no', 'maybe'],
            intent='answer_boolean',
            **args
        )

    def _process_answer(self):
        if not self._validate_answer() or self._get_answer() == 'maybe':
            self._io.say('I didn\'t quite catch that.')
            return self
        return None
