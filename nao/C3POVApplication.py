from threading import Semaphore

from AbstractApplication import AbstractApplication


class C3POVApplication(AbstractApplication):
    def __init__(self, lang: str, dfKey: str, dfAgent: str):
        super().__init__()
        # Initialise the speech semaphore, required for input
        self.speechLock = Semaphore(0)

        # Set the correct language (and wait for it to be changed)
        self.setLanguage(lang)
        self.response = None
        self.speechLock.acquire()

        # Pass the required Dialogflow parameters (add your Dialogflow parameters)
        self.setDialogflowKey(dfKey)
        self.setDialogflowAgent(dfAgent)

    def ask(self, sentence: str):
        self.setAudioContext('answer_name')
        print(' listen')
        self.startListening()
        self.speechLock.acquire(timeout=15)
        self.stopListening()
        return ''

    def say(self, sentence: str):
        print(' start talking ')
        self.sayAnimated(sentence)
        print(' end talking ')
        self.speechLock.acquire()

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
        self.speechLock.release()
