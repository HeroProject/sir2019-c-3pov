from threading import Semaphore

from AbstractApplication import AbstractApplication


class C3POVApplication(AbstractApplication):
    def __init__(self, lang: str, dfKey: str, dfAgent: str):
        super().__init__()
        """   VARIABLES REQUIRED FOR ROBOT INTERFACE   """

        # Set the correct language (and wait for it to be changed)
        self.langLock = Semaphore(0)
        self.setLanguage(lang)
        self.langLock.acquire()

        # Pass the required Dialogflow parameters (add your Dialogflow parameters)
        self.setDialogflowKey(dfKey)
        self.setDialogflowAgent(dfAgent)

        # Initialise the speech semaphore, required for input
        self.speechLock = Semaphore(0)
        self.varLock = Semaphore(0)

    def ask(self, sentence: str):
        return input(sentence)

    def say(self, sentence: str):
        self.sayAnimated(sentence)

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
