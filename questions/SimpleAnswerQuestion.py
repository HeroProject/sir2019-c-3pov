from typing import Optional

from .Question import Question


class SimpleAnswerQuestion(Question):
    def __init__(self, answer: str = None, **args):
        super(SimpleAnswerQuestion, self).__init__(
            params={'answer': self._normalize_answer(answer)},
            **args
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
