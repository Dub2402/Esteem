from .InlineKeyboards import InlineKeyboards

from dublib.Methods.JSON import ReadJSON, WriteJSON
from telebot import TeleBot

class Moderator:

    @property
    def GetUnModerated(self):
        return self.UnModerated
    
    def __init__(self) -> None:
        self.UnModerated = ReadJSON("Data/Moderation/Moderation.json")

    def __Save(self, Data: dict) -> None:
        WriteJSON("Data/Moderation/Moderation.json", Data)
        
    def SaveUserSentences(self, sentence: str, gender: str):
        self.UnModerated["Unmoderated"][gender].append(sentence)
        self.__Save(self.__UnModerated)


    def SendToAdmin(self, bot: TeleBot, id: int, gender: str):
        for Index in range(0,4):
            bot.send_message(
                id, 
                self.UnModerated["Unmoderated"][gender][Index],
                reply_markup=InlineKeyboards().CheckModeration()
            )


        
