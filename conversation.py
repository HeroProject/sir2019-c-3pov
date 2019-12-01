from typing import Dict, Optional, List
from AbstractApplication import AbstractApplication
from threading import Semaphore


# NEIL CHANGES:
#   - 'Question' class is now a subclass of 'AbstractApplication'
#   - 'print' functions replaced by 'sayAnimated'
#   - Added necessary semaphores and DialogFlow params to interface w/ robot
#   - Created get_input function to handle semaphores gracefully and prevent running threads at end of program
#   - Extended onRobotEvent and onAudioIntent from 'AbstractApplication' to add our functionality
#   - Replaced input() with get_input() function, which requests an intent (Defined in Google DialogFlow web interface)
class Question(AbstractApplication):
    def __init__(
            self,
            question: str,
            expects_intent: bool = False,
            expects_params: bool = True,
            intent: str = None,
            params: Dict[str, any] = None
                 ):
        super().__init__()

        """   VARIABLES REQUIRED FOR ROBOT INTERFACE   """
        # Set the correct language (and wait for it to be changed)
        self.langLock = Semaphore(0)
        self.setLanguage('en-US')
        self.langLock.acquire()

        # Pass the required Dialogflow parameters (add your Dialogflow parameters)
        self.setDialogflowKey('newagent-xsfpqi-66f399b80178.json')
        self.setDialogflowAgent('newagent-xsfpqi')

        # Initialise the speech semaphore, required for input
        self.speechLock = Semaphore(0)
        self.varLock = Semaphore(0)
        """----------------------------------"""

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
            self.sayAnimated(self._question)
            self.get_input(self._intent)
            '''
            print(self._question)
            if get_intent:
                self._set_intent(input('Intent: '))

            if get_params:
                # You can replace this with your own logic in that actually accepts multiple params.
                # By default we'll only have answer.
                self._set_params({'answer': input('Answer: ')})
            '''
        return self._process_answer()

    """   METHODS EXTENDING FROM 'AbstractApplication'   """
    def onRobotEvent(self, event):
        if event == 'LanguageChanged':
            self.langLock.release()
        elif event == 'TextDone':
            self.speechLock.release()

        # TODO
        #   Gesture Implementation
        '''
        elif event == 'GestureDone':
            self.gestureLock.release()
        '''

    def onAudioIntent(self, *args, intent_name):
        if intent_name == self._intent and len(args) > 0:
            if self._expects_intent and not self._has_intent():
                self._set_intent(args[0])
            if self._expects_params and not self._has_params():
                self._set_params(args[0])
            self.varLock.release()

    """   REQUIRED TO HANDLE SEMAPHORES GRACEFULLY   """
    def get_input(self, intent: str):
        self.speechLock.acquire()
        self.setAudioContext(intent)
        self.startListening()
        self.varLock.acquire(timeout=5)
        self.stopListening()
        if self._expects_intent and not self._has_intent():
            self.varLock.acquire(timeout=2)
        if self._expects_params and not self._has_params():
            self.varLock.acquire(timeout=2)


class SimpleAnswerQuestion(Question):
    def __init__(self, question: str, answer: str = None):
        super(SimpleAnswerQuestion, self).__init__(
            question=question,
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


class ClosedQuestion(SimpleAnswerQuestion):
    def __init__(self, question: str, answer_options: List[str], answer: str = None):
        super(ClosedQuestion, self).__init__(
            question=question,
            answer=answer
        )
        self._answer_options = answer_options

    def _normalize_answer(self, answer: str) -> Optional[str]:
        return super()._normalize_answer(answer.lower()) if type(answer) == str else None

    def _validate_answer(self) -> bool:
        return self._get_answer() in self._answer_options


class BooleanQuestion(ClosedQuestion):
    def __init__(self, question: str, **args):
        super(BooleanQuestion, self).__init__(
            question=question,
            answer_options=['yes', 'no'],
            **args
        )


class WhatIsYourNameQuestion(SimpleAnswerQuestion):
    def __init__(self, answer: str = None):
        super(WhatIsYourNameQuestion, self).__init__(
            question='What is your name?',
            answer=answer
        )

    def _process_answer(self) -> Optional[Question]:
        #   Changed this with reply
        self.sayAnimated('Nice to meet you %s.' % self._get_answer())
        # print('Nice to meet you %s.' % self._get_answer())
        return WhatCanIDoForYouQuestion()


class WhatCanIDoForYouQuestion(Question):
    def __init__(self, intent: str = None, params: Dict[str, any] = None):
        super(WhatCanIDoForYouQuestion, self).__init__(
            question='What can I do for you? (options: locate_platform, find_destination)',
            expects_intent=True,
            intent=intent,
            params=params
        )

    def _process_answer(self) -> Optional[Question]:
        if self._intent == 'locate_platform':
            return PlatformQuestion(answer=self._params['answer'])
        elif self._intent == 'find_destination':
            return DestinationQuestion(answer=self._params['answer'])
        else:
            self.sayAnimated('I didn\'t quite catch that.')
            # print('I didn\'t quite catch that.')
            return WhatCanIDoForYouQuestion()


class AnythingElseICanDoQuestion(BooleanQuestion):
    def __init__(self, **args):
        super(AnythingElseICanDoQuestion, self).__init__(
            question='Anything else I can do for you?',
            **args
        )

    def _process_answer(self) -> Optional[Question]:
        if self._get_answer() == 'yes':
            return WhatCanIDoForYouQuestion()
        self.sayAnimated('Thank you, and have a nice day.')
        # print('Thank you, and have a nice day.')
        return None


class PlatformQuestion(ClosedQuestion):
    def __init__(self, **args):
        super(PlatformQuestion, self).__init__(
            question='Please specify the platform',
            answer_options=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16'],
            **args
        )

    def _process_answer(self) -> Optional[Question]:
        if not self._validate_answer():
            #   Changed accordingly to support robot
            self.sayAnimated('I\'m sorry, but that platform does not exist at this train station')
            # print('I\'m sorry, but that platform does not exist at this train station')
            return PlatformQuestion()
        #   Changed to interface w/ robot
        self.sayAnimated('You can find platform %s over there' % self._get_answer())
        # print('You can find platform %s over there' % self._get_answer())
        return AnythingElseICanDoQuestion()


class DestinationQuestion(SimpleAnswerQuestion):
    def __init__(self, **args):
        super(DestinationQuestion, self).__init__(
            question='Please specify the destination',
            **args
        )

    def _process_answer(self) -> Optional[Question]:
        # TODO
        #   Change to interface w/ robot
        #   Not sure if I have to include anything here... Will test next lab session - Neil @ 1/12/2019
        # print('Find Destination')
        return AnythingElseICanDoQuestion()


# Start with asking for the traveller's name.
q = WhatIsYourNameQuestion()

# Keep asking questions until we run out of questions.
while q is not None:
    q = q.ask_question()

#   Stopping the thread at the end of execution
q.stop()
