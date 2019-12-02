from io_mapper.ConversationIO import ConversationIO


class CLI(ConversationIO):
    def ask(self, sentence: str):
        return input(sentence)

    def say(self, sentence: str):
        print(sentence)
