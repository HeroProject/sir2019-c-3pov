import random
import nao.AbstractApplication as Base
from threading import Semaphore


class DialogFlowSampleApplication(Base.AbstractApplication):
    """
    INTENT DICTIONARY STRUCTURE:
        self.intents[intent][0]   :     SEMAPHORE
        self.intents[intent][1]   :     CONVERSATION INTRO
        self.intents[intent][2]   :     USER RESPONSE
        self.intents[intent][3]   :     GOOD RESPONSE
        self.intents[intent][4]   :     BAD RESPONSE
    """

    '''   STANDARD CONVERSATION FUNCTION PROCESS   '''

    def converse(self, intent):
        if intent in self.intents.keys():
            self.sayAnimated(random.choice(self.intents[intent][1]))
            self.speechLock.acquire()
            self.setAudioContext(intent)
            self.startListening()
            self.intents[intent][0].acquire(timeout=5)
            self.stopListening()
            if not self.intents[intent][2]:
                self.intents[intent][0].acquire(timeout=2)
            # Respond and wait for that to finish
            if self.intents[intent][2]:
                self.add_good_reply_value(intent)
                self.sayAnimated(random.choice(self.intents[intent][3]))
            else:
                self.sayAnimated(random.choice(self.intents[intent][4]))
            self.speechLock.acquire()
        else:
            raise Exception('Intent passed does not exist')

    def add_good_reply_value(self, intent):
        reply_value = self.intents[intent][2]

        if intent == 'answer_name':
            self.intents[intent][3] = [
                'Nice to meet you ' + reply_value + '!',
                'Oh hi' + reply_value + '!',
                reply_value + 'What a beautiful name. Reminds me of my creators.'
            ]
        elif intent == 'answer_destination':
            self.intents[intent][3] = [
                'Oh, ' + reply_value + ' is lovely.',
                'I. LOVE. ' + reply_value + '!'
            ]
        elif intent == 'answer_instruction':
            if reply_value == 'platform':
                pass
            elif reply_value == 'destination':
                pass
            elif reply_value == 'employee':
                self.intents[intent][3] = [
                    'One of my homies will help you very shortly'
                ]

    def main(self):
        self.intents = \
            {
                'answer_name':
                    [Semaphore(0),
                     ['What is your name?', 'Who are you?'],
                     None,
                     [],
                     ['Sorry, I didn\'t get that']
                     ],

                'answer_destination':
                    [Semaphore(0),
                     ['Where are you headed to?', 'Where are you going?'],
                     None,
                     [],
                     ['Sorry, I didn\'t get where you\'re going']
                     ],
                'answer_instruction':
                    [Semaphore(0),
                     ['Do you need help with going somewhere, help with finding a platform, or '
                      'should I call an actual NS Human Being?'],
                     None,
                     [],
                     ['Sorry, I didn\t get it. Can you repeat, pretty please?']
                     ]
            }

        # Set the correct language (and wait for it to be changed)
        self.langLock = Semaphore(0)
        self.setLanguage('en-US')
        self.langLock.acquire()

        # Pass the required Dialogflow parameters (add your Dialogflow parameters)
        self.setDialogflowKey('../newagent-xsfpqi-fb9d36b92677.json')
        self.setDialogflowAgent('newagent-xsfpqi')

        # Make the robot ask the question, and wait until it is done speaking

        self.speechLock = Semaphore(0)

        self.converse('answer_name')
        self.converse('answer_destination')

        # Choose gesture from ns_nao folder
        self.gestures('ns_nao/Rarm_forwards')
        self.gestures('ns_nao/Rarm_left')
        self.gestures('ns_nao/Explanation')

    def gestures(self, gesture):
        self.gestureLock = Semaphore(0)
        self.doGesture(gesture)
        self.gestureLock.acquire()

    def onRobotEvent(self, event):
        if event == 'LanguageChanged':
            self.langLock.release()
        elif event == 'TextDone':
            self.speechLock.release()
        elif event == 'GestureDone':
            self.gestureLock.release()

    def onAudioIntent(self, *args, intentName):
        if intentName in self.intents.keys() and len(args) > 0:
            self.intents[intentName][2] = args[0]
            self.intents[intentName][0].release()


# Run the application
sample = DialogFlowSampleApplication()
sample.main()
sample.stop()
