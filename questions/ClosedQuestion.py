from typing import List, Optional

from questions.SimpleAnswerQuestion import SimpleAnswerQuestion
from io_mapper.ConversationIO import ConversationIO


class ClosedQuestion(SimpleAnswerQuestion):
    def __init__(self, io: ConversationIO, question: str, answer_options: List[str], answer: str = None):
        super(ClosedQuestion, self).__init__(
            io=io,
            question=question,
            answer=answer
        )
        self._answer_options = answer_options

    def _normalize_answer(self, answer: str) -> Optional[str]:
        return super()._normalize_answer(answer.lower()) if type(answer) == str else None

    def _validate_answer(self) -> bool:
        return self._get_answer() in self._answer_options

