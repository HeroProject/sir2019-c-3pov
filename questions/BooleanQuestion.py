from questions.ClosedQuestion import ClosedQuestion
from io_mapper.ConversationIO import ConversationIO


class BooleanQuestion(ClosedQuestion):
    def __init__(self, io: ConversationIO, question: str, **args):
        super(BooleanQuestion, self).__init__(
            io=io,
            question=question,
            answer_options=['yes', 'no'],
            **args
        )
