from io_mapper.ConversationIO import ConversationIO
from questions import WhatCanIDoForYouQuestion


def conversation(io: ConversationIO):
    # Start with asking for the traveller's name.
    question = WhatCanIDoForYouQuestion(io)

    # Keep asking questions until we run out of questions.
    while question is not None:
        question = question.ask_question()
