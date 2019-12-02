from io_mapper.ConversationIO import ConversationIO
from nao import C3POVApplication


class Nao(ConversationIO):
    def __init__(self, nao: C3POVApplication):
        self.__nao = nao

    def ask(self, sentence: str):
        return self.__nao.ask(sentence)

    def say(self, sentence: str):
        print(sentence)
        self.__nao.say(sentence)
