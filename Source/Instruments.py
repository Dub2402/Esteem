from dublib.Polyglot import Markdown
import random

def SendButtonDose(User, Bot, Call, InlineKeyboardsBox):
    CallName = Markdown(User.get_property("Name")).escaped_text
    if User.get_property("Gender") =="W":
        Bot.send_message(
                Call.message.chat.id, 
                f"{CallName}, каждый день я буду с тобой на связи и буду напоминать тебе, что ты лучшая\\!\n\nТакже, если тебе будет мало, ты можешь использовать кнопку *ДОЗА* 🖲\n\n_А пока удачи\\! Рад был познакомиться\\!_",
                parse_mode = "MarkdownV2",
                reply_markup=InlineKeyboardsBox.Dose()
                )
    if User.get_property("Gender") =="M":
        Bot.send_message(
                Call.message.chat.id, 
                f"{CallName}, каждый день я буду с тобой на связи и буду напоминать тебе, что ты лучший\\!\n\nТакже, если тебе будет мало, ты можешь использовать кнопку *ДОЗА* 🖲\n\n_А пока удачи\\! Рад был познакомиться\\!_",
                parse_mode = "MarkdownV2",
                reply_markup=InlineKeyboardsBox.Dose()
                )
    

def ChoiceSentence(Sentences):
    random_sentence = random.randint(1, len(Sentences))
    
    for Index in range(len(Sentences)):
        if Index == random_sentence-1:
            Text = Sentences[Index]

    return Text
            
    