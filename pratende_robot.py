import AbstractApplication as Base
from threading import Semaphore
from random import randint

dictionary = {'answer_intent': ["How can I help you?", "Yo brah, what can I do for you today?",
                                              "Hey, how may I assist you?"],
                            'answer_name': ["What is your name?", "How do they call you?",
                                            "Which name did your parents give you?"],
                            'answer_fav_color': ["What is your favorite color?", "Which color do your prefer?",
                                                 "Could you name your favorite color?"],
                            'answer_destination': ["Where you do want to go?", "Where do you need to go today?",
                                                   "What is your destination?"],
                            'repeat': ["I am sorry I did not get that", "Sorry, I did not hear you",
                                       "Sorry I did not catch what you said"]}


class DialogFlowSampleApplication(Base.AbstractApplication):
    def ask(self, question, intent):
        # Make the robot ask the question, and wait until it is done speaking
        self.speechLock = Semaphore(0)
        self.sayAnimated(question)
        self.speechLock.acquire()

        # Listen for an answer for at most 5 seconds
        self.answer = None
        self.answerLock = Semaphore(0)
        self.setAudioContext(intent)
        self.startListening()
        self.answerLock.acquire(timeout=5)
        self.stopListening()
        if not self.answer:  # wait one more second after stopListening (if needed)
            self.answerLock.acquire(timeout=1)

        # Respond and wait for that to finish
        if self.answer:
            return self.answer
        else:
            self.sayAnimated(dictionary['repeat'][randint(0, 2)])
            self.ask(question, intent)

    def main(self):
        # Set the correct language (and wait for it to be changed)
        self.langLock = Semaphore(0)
        self.setLanguage('en-US')
        self.langLock.acquire()

        # Pass the required Dialogflow parameters (add your Dialogflow parameters)
        self.setDialogflowKey('newagent-xsfpqi-be69c3c98fe1.json')
        self.setDialogflowAgent('newagent-xsfpqi')

        # Asks user how robot can help
        #reply = self.ask(dictionary['answer_intent'][randint(0, 2)], 'answer_intent')
        reply = 'answer_name'
        second_reply = self.ask(dictionary[reply][randint(0, 2)], reply)
        if reply == 'answer_name':
            self.sayAnimated('Nice to meet you ' + second_reply + '!')
        elif reply == 'answer_fav_color':
            self.sayAnimated('I really like the color ' + second_reply + ' too!')

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
        if intentName == 'answer_name' and len(args) > 0:
            self.name = args[0]
            self.nameLock.release()


# Run the application
sample = DialogFlowSampleApplication()
sample.main()
sample.stop()
