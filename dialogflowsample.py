from IPython.core import logger

import AbstractApplication as Base
from threading import Semaphore

intents = {'answer_name': [Semaphore(0), ''],
           'answer_destination': [Semaphore(0), '']
           }


class DialogFlowSampleApplication(Base.AbstractApplication):
    def main(self):
        # Set the correct language (and wait for it to be changed)
        self.langLock = Semaphore(0)
        self.setLanguage('en-US')
        self.langLock.acquire()

        # Pass the required Dialogflow parameters (add your Dialogflow parameters)
        self.setDialogflowKey('newagent-xsfpqi-be69c3c98fe1.json')
        self.setDialogflowAgent('newagent-xsfpqi')

        # Make the robot ask the question, and wait until it is done speaking

        self.speechLock = Semaphore(0)
        '''
        self.sayAnimated('Hello, what is your name?')
        self.speechLock.acquire()

        # Listen for an answer for at most 5 seconds
        self.name = None
        self.nameLock = Semaphore(0)
        self.setAudioContext('answer_name')
        self.startListening()
        self.nameLock.acquire(timeout=5)
        self.stopListening()
        if not self.name:  # wait one more second after stopListening (if needed)
            self.nameLock.acquire(timeout=1)
        # Respond and wait for that to finish
        if self.name:
            self.sayAnimated('Nice to meet you ' + self.name + '!')
        else:
            self.sayAnimated('Sorry, I didn\'t catch your name.')
            '''

        # second intent
        self.sayAnimated('Where are you going?')
        self.speechLock.acquire()
        # Listen for an answer for at most 5 seconds
        self.location = None
        self.locationLock = Semaphore(0)
        self.setAudioContext('answer_destination')
        self.startListening()
        self.locationLock.acquire(timeout=5)
        self.stopListening()
        if not self.location:  # wait one more second after stopListening (if needed)
            self.locationLock.acquire(timeout=1)
        if self.location:
            self.sayAnimated('Is your location '+str(self.location)+"?")
        else:
            self.sayAnimated('Sorry, I didn\'t get that.')
        #self.speechLock.acquire()

        # Display a gesture (replace <gestureID> with your gestureID)
        self.gestureLock = Semaphore(0)
        self.doGesture('<gestureID>/behavior_1')
        self.gestureLock.acquire()

    def onRobotEvent(self, event):
        if event == 'LanguageChanged':
            self.langLock.release()
        elif event == 'TextDone':
            self.speechLock.release()
        elif event == 'GestureDone':
            self.gestureLock.release()

    def onAudioIntent(self, *args, intentName):
        #raise Exception('exception')
        if intentName in intents and len(args) > 0:
            self.location = args[0]
            self.locationLock.release()
            # self.name = args[0]
            # self.nameLock.release()


# Run the application
sample = DialogFlowSampleApplication()
sample.main()
sample.stop()
