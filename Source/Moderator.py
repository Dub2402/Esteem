from dublib.Methods.JSON import ReadJSON, WriteJSON

class Moderator:
    
    def __init__(self) -> None:
        self.__UnModerated = ReadJSON("Data/Moderation/Moderation.json")


    def __Save(self, Data: dict) -> None:
        WriteJSON("Data/Moderation/Moderation.json", Data)
        
    def SaveUserSentences(self, sentence, gender):
        self.__UnModerated["Unmoderated"][gender].append(sentence)
        self.__Save(self.__UnModerated)        
