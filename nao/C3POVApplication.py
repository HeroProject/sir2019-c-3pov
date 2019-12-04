from threading import Semaphore

from AbstractApplication import AbstractApplication


class C3POVApplication(AbstractApplication):
    def __init__(self, lang: str, dfKey: str, dfAgent: str):
        super().__init__()
        """   VARIABLES REQUIRED FOR ROBOT INTERFACE   """

        # Set the correct language (and wait for it to be changed)
        # self.langLock = Semaphore(0)
        self.setLanguage(lang)
        self.response = None
        # self.langLock.acquire()
        # Initialise the speech semaphore, required for input
        self.speechLock = Semaphore(0)
        # self.listenLock = Semaphore(0)
        self.speechLock.acquire()

        # Pass the required Dialogflow parameters (add your Dialogflow parameters)
        self.setDialogflowKey(dfKey)
        self.setDialogflowAgent(dfAgent)

    def ask(self, sentence: str):
        # self.speechLock = Semaphore(0)
        # self.speechLock.acquire()
        self.setAudioContext('answer_name')
        print(' listen')
        self.startListening()
        self.speechLock.acquire(timeout=15)
        self.stopListening()
        # if not self.response():
        #     self.varLock.acquire(timeout=2)
        return ''

    def say(self, sentence: str):
        print(' start talking ')
        self.sayAnimated(sentence)
        print(' end talking ')
        self.speechLock.acquire()

    """   METHODS EXTENDING FROM 'AbstractApplication'   """

    def onRobotEvent(self, event):
        if event == 'LanguageChanged':
            self.speechLock.release()
        if event == 'TextDone':
            print(' release')
            self.speechLock.release()

        # TODO
        #   Gesture Implementation
        '''
        elif event == 'GestureDone':
            self.gestureLock.release()
        '''

    def onAudioIntent(self, *args, intentName):
        print('onAudioIntent'+intentName, args)
        # if intent_name == self._intent and len(args) > 0:
        #     self.response = args[0]
        self.speechLock.release()
            # self.varLock = None

    """   REQUIRED TO HANDLE SEMAPHORES GRACEFULLY   """

    def get_input(self, intent: str):
        pass
