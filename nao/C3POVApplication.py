from threading import Semaphore
from typing import Optional

from AbstractApplication import AbstractApplication


class C3POVApplication(AbstractApplication):
    def __init__(self, lang: str, df_key: str, df_agent: str):
        super().__init__()
        # Initialise the speech semaphore, required for input
        self.speechLock = Semaphore(0)
        self.response: Optional[str] = None

        # Set the correct language (and wait for it to be changed)
        self.setLanguage(lang)
        self.speechLock.acquire()

        # Pass the required Dialogflow parameters (add your Dialogflow parameters)
        self.setDialogflowKey(df_key)
        self.setDialogflowAgent(df_agent)

    def ask(self, intent: str) -> Optional[str]:
        self.setAudioContext(intent)
        self.startListening()
        self.speechLock.acquire(timeout=15)
        self.stopListening()
        print('Response: ', self.response)
        return self.response

    def say(self, sentence: str):
        self.sayAnimated(sentence)
        self.speechLock.acquire()

    def onRobotEvent(self, event):
        if event == 'LanguageChanged':
            self.speechLock.release()
        if event == 'TextDone':
            print('Release lock')
            self.speechLock.release()

    def onAudioIntent(self, *data, intentName):
        print('Captured sound ', intentName, data)
        self.speechLock.release()
        self.response = data[0] if data else None
