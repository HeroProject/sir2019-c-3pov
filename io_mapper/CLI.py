from io_mapper.ConversationIO import ConversationIO


class CLI(ConversationIO):
    def ask(self, intent: str) -> str:
        print(intent)
        return input('Answer: ')

    def say(self, sentence: str):
        print(sentence)
