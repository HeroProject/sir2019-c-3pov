from time import sleep

import AbstractApplication as Base


class SampleApplication(Base.AbstractApplication):
    def main(self):
        self.setLanguage('en-US')
        self.sayAnimated('Hello people')
        sleep(2)

    def onRobotEvent(self, event):
        print(event)


# Run the application
sample = SampleApplication()
sample.main()
sample.stop()
