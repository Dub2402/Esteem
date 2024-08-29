from .InlineKeyboards import InlineKeyboards

from dublib.Methods.JSON import ReadJSON, WriteJSON
from telebot import TeleBot

import pandas

class Moderator:

    @property
    def GetUnModerated(self):
        return self.Data
    
    def __init__(self) -> None:
        self.Data = ReadJSON("Data/Moderation/Moderation.json")
        
    def __Save(self, Data: dict) -> None:
        WriteJSON("Data/Moderation/Moderation.json", Data)

    def __GetFreeID(self) -> int:
        ID = 1
        for key in self.Data.keys():
            if ID <= int(key): ID = int(key) + 1
            else: pass
        return ID
                
    def SaveUserSentences(self, sentence: str, gender: str):
        self.Data[self.__GetFreeID()] = {"gender": gender, "sentence": sentence, "status": "add"}
        self.__Save(self.Data)

    def SendToAdmin(self, bot: TeleBot, id: int, gender: str):
        Count = 0
        for ID_Sentence in self.Data.keys():

            if self.Data[ID_Sentence]["gender"] == gender and self.Data[ID_Sentence]["status"] == "add":
                Count +=1 
                Sentence = self.Data[ID_Sentence]["sentence"]
                bot.send_message(
                    id,
                    Sentence,
                    reply_markup = InlineKeyboards().CheckModeration(Sentence, ID_Sentence, gender)
                    )
                return
    
        if Count <1:
                bot.send_message(
                    id,
                    "Послания отсутствуют")
                return

    def ModerationApprove(self, bot: TeleBot, id, Message, Sentence: str, ID_Sentence: str, gender: str):
        self.Data[ID_Sentence]["status"] = "to_excel"
        self.__Save(self.Data)
        bot.delete_message(id, Message)
        Count = 0
        for ID_Sentence in self.Data.keys():
            if self.Data[ID_Sentence]["gender"] == gender and self.Data[ID_Sentence]["status"] == "add":
                Count +=1 
                Sentence = self.Data[ID_Sentence]["sentence"]
                bot.send_message(
                    id,
                    Sentence,
                    reply_markup = InlineKeyboards().CheckModeration(Sentence, ID_Sentence, gender)
                    )
                break

        if Count <1:
                bot.send_message(
                    id,
                    "Послания отсутствуют")
                return
        
    def ModerationDelete(self, bot: TeleBot, id, Message, Sentence: str, ID_Sentence: str, gender: str):
        del self.Data[ID_Sentence]
        self.__Save(self.Data)
        bot.delete_message(id, Message)
        Count = 0
        for ID_Sentence in self.Data.keys():

            if self.Data[ID_Sentence]["gender"] == gender and self.Data[ID_Sentence]["status"] == "add":
                Count +=1
                Sentence = self.Data[ID_Sentence]["sentence"]
                bot.send_message(
                    id,
                    Sentence,
                    reply_markup = InlineKeyboards().CheckModeration(Sentence, ID_Sentence, gender)
                    )
                break
        if Count <1:
                bot.send_message(
                    id,
                    "Послания отсутствуют")
                return
           
    def Unload(self):
        self.BufferMens = {"Данные": []}
        self.BufferWomens = {"Данные": []}
        
        for ID_Sentence in self.Data.keys():

            if self.Data[ID_Sentence]["gender"] == "Men" and self.Data[ID_Sentence]["status"] == "to_excel":
                print(self.Data[ID_Sentence]["sentence"])
                self.BufferMens["Данные"].append(self.Data[ID_Sentence]["sentence"])
                print(self.BufferMens)

            if self.Data[ID_Sentence]["gender"] == "Women" and self.Data[ID_Sentence]["status"] == "to_excel":
                print(self.Data[ID_Sentence]["sentence"])
                self.BufferWomens["Данные"].append(self.Data[ID_Sentence]["sentence"])
                print(self.BufferWomens)
            df = pandas.DataFrame.from_dict(self.BufferWomens)
            df.to_excel(f"oz.xlsx", index= False)


      




        
