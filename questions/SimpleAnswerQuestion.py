from typing import Optional

from questions.Question import Question
from io_mapper.ConversationIO import ConversationIO


class SimpleAnswerQuestion(Question):
    def __init__(self, io: ConversationIO, intent: str, question: str, gesture: str = None, answer: str = None):
        super(SimpleAnswerQuestion, self).__init__(
            io=io,
            intent=intent,
            question=question,
            gesture=gesture,
            params={'answer': self._normalize_answer(answer)}
        )

    def _normalize_answer(self, answer: str) -> Optional[str]:
        if type(answer) == str:
            answer = answer.strip()
            return answer if len(answer) > 0 else None
        return None

    def _get_answer(self):
        return self._params['answer']

    def _has_params(self) -> bool:
        return self._get_answer() is not None
