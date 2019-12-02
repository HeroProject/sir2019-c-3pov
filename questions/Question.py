from typing import Dict, Optional

from io_mapper.ConversationIO import ConversationIO


class Question:
    def __init__(
            self,
            io: ConversationIO,
            question: str,
            expects_intent: bool = False,
            expects_params: bool = True,
            intent: str = None,
            params: Dict[str, any] = None
    ):
        self._io = io
        self._question = question
        self._expects_intent = expects_intent
        self._expects_params = expects_params
        self._intent: str = self._set_intent(intent)
        self._params: Dict[str, any] = self._set_params(params)

    def _has_intent(self) -> bool:
        return self._intent is not None

    def _has_params(self) -> bool:
        return self._params is not None

    def _set_intent(self, intent: str) -> Optional[str]:
        self._intent = intent.lower().strip() if type(intent) is str else None
        return self._intent

    def _set_params(self, params: Dict[str, any] = None):
        self._params = params
        return self._params

    def _process_answer(self) -> Optional['Question']:
        return None

    def ask_question(self) -> Optional['Question']:
        get_intent: bool = self._expects_intent and not self._has_intent()
        get_params: bool = self._expects_params and not self._has_params()
        if get_intent or get_params:
            self._io.say(self._question)
            if get_intent:
                self._set_intent(self._io.ask('Intent: '))

            if get_params:
                # You can replace this with your own logic in that actually accepts multiple params.
                # By default we'll only have answer.
                self._set_params({'answer': self._io.ask('Answer: ')})

        return self._process_answer()
