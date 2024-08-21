from dublib.Polyglot import Markdown
import random

def SendButtonDose(User, Bot, Call, InlineKeyboardsBox):
    CallName = Markdown(User.get_property("Name")).escaped_text
    Bot.send_message(
			Call.message.chat.id, 
			f"{CallName}, если тебе будет грустно или просто захочется поднять настроение, кликай по кнопке *ДОЗА* 🖲\n\nМожешь хоть изнасиловать её, мне главное, чтобы тебе стало лучше\\! 😁 Ну а так, я тебе не дам заскучать, и буду всегда на связи\\. Скоро ты поймёшь о чем я\\!\\)",
			parse_mode = "MarkdownV2",
			reply_markup=InlineKeyboardsBox.Dose()
			)
    

def ChoiceSentence(Sentences):
	random_sentence = random.randint(1, len(Sentences))
	
	for Index in range(len(Sentences)):
		if Index == random_sentence-1:
			Text = Sentences[Index]

	return Text
			
    