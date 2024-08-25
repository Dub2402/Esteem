from dublib.Methods.JSON import ReadJSON, WriteJSON

class Moderator:

    @property
    def GetUnModerated(self):
        return self.UnModerated
    
    def __init__(self) -> None:
        self.UnModerated = ReadJSON("Data/Moderation/Moderation.json")

    def __Save(self, Data: dict) -> None:
        WriteJSON("Data/Moderation/Moderation.json", Data)
        
    def SaveUserSentences(self, sentence, gender):
        self.UnModerated["Unmoderated"][gender].append(sentence)
        self.__Save(self.__UnModerated)        
