from dublib.Polyglot import Markdown
import random

def SendButtonDose(User, Bot, Call, InlineKeyboardsBox):
    CallName = Markdown(User.get_property("Name")).escaped_text
    Bot.send_message(
            Call.message.chat.id, 
            f"{CallName}, каждый день я с тобой буду на связи\\!\n\nА если тебе будет мало, то просто понажимай на кнопку *ДОЗА* 🖲\n\n_А пока удачи\\! Рад был с тобой познакомиться\\!_",
            parse_mode = "MarkdownV2"
            )

def ChoiceSentence(Sentences) -> str:
    random_sentence = random.randint(1, len(Sentences))
    
    for Index in range(len(Sentences)):
        if Index == random_sentence-1:
            Text = Sentences[Index]

    return Text
            
    