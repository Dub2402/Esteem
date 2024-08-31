from .InlineKeyboards import InlineKeyboards

from dublib.Methods.JSON import ReadJSON, WriteJSON
from telebot import TeleBot
from datetime import date

import pandas
import os

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

            if self.Data[ID_Sentence]["gender"] == gender.replace("s", "") and self.Data[ID_Sentence]["status"] == "add":
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
            if self.Data[ID_Sentence]["gender"] == gender.replace("s", "") and self.Data[ID_Sentence]["status"] == "add":
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

            if self.Data[ID_Sentence]["gender"] == gender.replace("s", "") and self.Data[ID_Sentence]["status"] == "add":
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
           
    def UnloadWomen(self, bot: TeleBot, id: int):
        NameFile = "Women"
        today = date.today()
        self.BufferWomens = {"Данные": []}
        CopyData = self.Data.copy()
        
        for ID_Sentence in CopyData.keys():
            
            if self.Data[ID_Sentence]["gender"] == "Women" and self.Data[ID_Sentence]["status"] == "to_excel":
                self.BufferWomens["Данные"].append(self.Data[ID_Sentence]["sentence"])
                del self.Data[ID_Sentence]
                self.__Save(self.Data)
                
        if self.BufferWomens["Данные"]:
            df = pandas.DataFrame.from_dict(self.BufferWomens)
            df.to_excel(f"{NameFile}_{today}.xlsx", index= False)
        
        else:
            bot.send_message(
            chat_id = id,
            text = "Нет данных в файле для модерации женщин."
            )

        if os.path.exists(f"{NameFile}_{today}.xlsx"):
            with open(f"{NameFile}_{today}.xlsx", "rb") as FileReader:
                BinaryArchive = FileReader.read()
        
            try:
                bot.send_document(id, BinaryArchive, visible_file_name = f"{NameFile}_{today}.xlsx")
                os.remove(f"{NameFile}_{today}.xlsx")
            except Exception as E:
                logging.info(E)

    def UnloadMen(self, bot: TeleBot, id: int):
        NameFile = "Men"
        today = date.today()
        self.BufferMens = {"Данные": []}
        CopyData = self.Data.copy()
    
        for ID_Sentence in CopyData.keys():

            if self.Data[ID_Sentence]["gender"] == "Men" and self.Data[ID_Sentence]["status"] == "to_excel":
                self.BufferMens["Данные"].append(self.Data[ID_Sentence]["sentence"])
                del self.Data[ID_Sentence]
                self.__Save(self.Data)
            
        if self.BufferMens["Данные"]:
            df = pandas.DataFrame.from_dict(self.BufferMens)
            df.to_excel(f"{NameFile}_{today}.xlsx", index= False)
        else:
            bot.send_message(
            chat_id = id,
            text = "Нет данных в файле для модерации мужчин."
            )

        if os.path.exists(f"{NameFile}_{today}.xlsx"):
            with open(f"{NameFile}_{today}.xlsx", "rb") as FileReader:
                BinaryArchive = FileReader.read()
    
            try:
                bot.send_document(id, BinaryArchive, visible_file_name = f"{NameFile}_{today}.xlsx")
                os.remove(f"{NameFile}_{today}.xlsx")
            except Exception as E:
                logging.info(E)
        