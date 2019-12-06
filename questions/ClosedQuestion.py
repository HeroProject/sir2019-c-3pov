from typing import List, Optional

from .SimpleAnswerQuestion import SimpleAnswerQuestion


class ClosedQuestion(SimpleAnswerQuestion):
    def __init__(self, answer_options: List[str], answer: str = None, **args):
        super(ClosedQuestion, self).__init__(answer=answer, **args)
        self._answer_options = answer_options

    def _normalize_answer(self, answer: str) -> Optional[str]:
        return super()._normalize_answer(answer.lower()) if type(answer) == str else None

    def _validate_answer(self) -> bool:
        return self._get_answer() in self._answer_options
