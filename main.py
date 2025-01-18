from Source.InlineKeyboards import InlineKeyboards
from Source.ReplyKeyboard import ReplyKeyboard
from Source.Instruments import SendButtonDose
from Source.Reader import Reader
from Source.Thread import Reminder
from Source.AdminPanel import Panel
from Source.Moderator import Moderator

from dublib.Methods.Filesystem import ReadJSON, WriteJSON
from dublib.Methods.System import CheckPythonMinimalVersion, Clear
from dublib.Methods.Filesystem import MakeRootDirectories
from dublib.TelebotUtils import UsersManager
from dublib.TelebotUtils.Cache import TeleCache
from telebot import types
from apscheduler.schedulers.background import BackgroundScheduler

import telebot
import logging
import random
import os

Settings = ReadJSON("Settings.json")

logging.basicConfig(level=logging.INFO, encoding="utf-8", filename="LOGING.log", filemode="w",
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

logging.getLogger("pyTelegramBotAPI").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)

# Проверка поддержки используемой версии Python.
CheckPythonMinimalVersion(3, 10)

# Создание папок в корневой директории.
MakeRootDirectories(["Data/Users"])
MakeRootDirectories(["Data/Moderation"])

if os.path.exists("Data/Moderation/Moderation.json"): pass
else: 
    DefaultJson = {}
    WriteJSON("Data/Moderation/Moderation.json", DefaultJson)

# Очистка консоли.
Clear()

Bot = telebot.TeleBot(Settings["token"])
Manager = UsersManager("Data/Users")
InlineKeyboardsBox = InlineKeyboards()
ReplyKeyboardBox = ReplyKeyboard()
reader = Reader(Settings)
scheduler = BackgroundScheduler()
reminder = Reminder(Bot, Manager, Settings, reader, scheduler)
AdminPanel = Panel()


# Инициализация менеджера кэша.
Cacher = TeleCache()
# Установка данных для выгрузки медиафайлов.
Cacher.set_options(Settings["token"], Settings["chat_id"])

# Получение структуры данных кэшированного файла.
try:
	File = Cacher.get_cached_file(Settings["qr_id"], type = types.InputMediaPhoto)
	# Получение ID кэшированного файла.
	FileID = Cacher[Settings["qr_id"]]
except Exception:
	pass

#==========================================================================================#
# >>>>> ДОБАВЛЕНИЕ ЗАДАНИЙ В APSHEDULER <<<<< #
#==========================================================================================#

job = scheduler.add_job(func=reminder.StartDailyDose, trigger='cron', hour = Settings["start_dailydose"].split(":")[0], minute = Settings["start_dailydose"].split(":")[1], id = 'job_1')
scheduler.start()

AdminPanel.decorators.commands(Bot, Manager, Settings["password"])

@Bot.message_handler(commands=["start"])
def ProcessCommandStart(Message: types.Message):
    User = Manager.auth(Message.from_user)
    User.set_property("Active", True)
    User.set_expected_type(None)
    Bot.send_message(
        Message.chat.id, 
        "Ну привет! ✌️\n\nА я знал, что тебя тоже ко мне занесёт. Что ж, давай поднимем тебе самооценочку!)"
        )
    try:
        call = User.get_property("Name")
        Bot.send_message(
            Message.chat.id, 
            f"Ооо, {call}, с возвращеницем!",
            reply_markup= ReplyKeyboardBox.AddMenu(User)
            )
        
    except KeyError:
        Bot.send_message(
        Message.chat.id, 
        "Как тебя зовут?"
        )
        User.set_expected_type("Name")
    
AdminPanel.decorators.reply_keyboards(Bot, Manager)

@Bot.message_handler(content_types = ["text"], regexp = "📢 Поделиться с друзьями")
def ProcessShareWithFriends(Message: types.Message):
    User = Manager.auth(Message.from_user)

    Bot.send_photo(
        Message.chat.id, 
        photo = FileID,
        caption="@Ddoza\\_bot\n@Ddoza\\_bot\n@Ddoza\\_bot\n\n*БПС \\| Бот повышения самооценки\\!*\nУлыбнись, мой милый друг, у\\-лыб\\-нись\\! 😊", 
        reply_markup=InlineKeyboardsBox.AddShare(), 
        parse_mode= "MarkdownV2"
        )

@Bot.message_handler(content_types = ["text"], regexp = "💉 ДОЗА")
def ProcessDose(Message: types.Message):
    dose = None
    User = Manager.auth(Message.from_user)
    if User.get_property("Gender") =="Women":
        dose = reader.GetWD
    if User.get_property("Gender") =="Men":
        dose = reader.GetMD
    
    random_sentence = random.randint(1, len(dose))

    for Index in range(len(dose)):
        if Index == random_sentence-1:
            Bot.send_message(
                Message.chat.id,
                text = dose[Index]
                )

@Bot.message_handler(content_types = ["text"], regexp = "⚙️ Настройки")
def ProcessChangeName(Message: types.Message):
    User = Manager.auth(Message.from_user)
    Bot.send_message(
        Message.chat.id, 
        "Выберите пункт, который вы хотите настроить:", reply_markup= InlineKeyboardsBox.SettingsMenu())
    
@Bot.message_handler(content_types = ["text"], regexp = "💟 Написать послание")
def ProcessWrite(Message: types.Message):
    User = Manager.auth(Message.from_user)
    Bot.send_message(
        Message.chat.id, 
        "Выбери, для кого ты хочешь написать послание:", reply_markup= InlineKeyboardsBox.WriteFor())

@Bot.message_handler(content_types=["text"])
def ProcessText(Message: types.Message):
    User = Manager.auth(Message.from_user)
    if AdminPanel.procedures.text(Bot, User, Message): return

    if User.expected_type == "Name":
        User.set_property("Name", Message.text)
        User.set_expected_type(None)
        CallName = User.get_property("Name")
        
        try: 
            if User.get_property("Change"):
                Bot.send_message(
                Message.chat.id,
                f"Приятно познакомиться, {CallName}!")
                Bot.send_message(
                Message.chat.id,
                "А пол-то я надеюсь ты не сменил? 🤭\nА то я уже сомневаюсь.",
                reply_markup= InlineKeyboardsBox.RepeatGender()
                )
        except:
            Bot.send_message(
                Message.chat.id,
                f"Уже неплохо, {CallName}! 😎\nДостойное имя!")
            Bot.send_message(
                Message.chat.id,
                "А ты кто вообще?", reply_markup= InlineKeyboardsBox.SelectionGender()
                )
    
    if User.expected_type == "Letter":

        if len(Message.text) > 200 and User.get_property("WriteTo") == "Dosa":
            Bot.send_message(
            Message.chat.id,
            "Превышение лимита, пожалуйста, повторите попытку."
            )
        elif len(Message.text) > 80 and User.get_property("WriteTo") == "Random":
            Bot.send_message(
            Message.chat.id,
            "Превышение лимита, пожалуйста, повторите попытку."
            )	
        else:
            User.set_temp_property("Moderation", Message.text)
            User.set_expected_type(None)
            Bot.send_message(
                Message.chat.id,
                f"Проверь, пожалуйста, все ли в норме? Если да, то подтверди\\!\n\n*Твой текст:*\n{Message.text}",
                reply_markup= InlineKeyboardsBox.CheckLetter(),
                parse_mode= "MarkdownV2"
                )

AdminPanel.decorators.inline_keyboards(Bot, Manager)

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("Return"))
def ProcessWithoutReminders(Call: types.CallbackQuery):
    User = Manager.auth(Call.from_user)
    Bot.delete_message(Call.message.chat.id, Call.message.id)
    
    Bot.answer_callback_query(Call.id)	

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("Men"))
def ProcessMen(Call: types.CallbackQuery):
    User = Manager.auth(Call.from_user)
    User.set_property("Gender", "Men")
    Bot.send_message(
        Call.message.chat.id, 
        "Я так и понял, что тут самец!)",
        reply_markup=ReplyKeyboardBox.AddMenu(User)
        )
    
    SendButtonDose(User, Bot, Call, InlineKeyboardsBox)
    User.clear_temp_properties()

    Bot.answer_callback_query(Call.id)

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("Women"))
def ProcessWomen(Call: types.CallbackQuery):
    User = Manager.auth(Call.from_user)
    User.set_property("Gender","Women")
    Bot.send_message(
        Call.message.chat.id, 
        "Уфф, а я чувствовал, что пахнет самочкой)", 
        reply_markup=ReplyKeyboardBox.AddMenu(User)
        )

    SendButtonDose(User, Bot, Call, InlineKeyboardsBox)
    User.clear_temp_properties()

    Bot.answer_callback_query(Call.id)

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("GirlFriend"))
def ProcessWomen(Call: types.CallbackQuery):
    User = Manager.auth(Call.from_user)

    Bot.send_message(
            Call.message.chat.id, 
            "Отличный выбор!\nА теперь выбери для чего:", 
            reply_markup=InlineKeyboardsBox.WriteTo()
    )
    User.set_temp_property("WriteFor", "Women")

    Bot.answer_callback_query(Call.id)

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("BoyFriend"))
def ProcessMen(Call: types.CallbackQuery):
    User = Manager.auth(Call.from_user)

    Bot.send_message(
            Call.message.chat.id, 
            "Отличный выбор!\nА теперь выбери для чего:", 
            reply_markup=InlineKeyboardsBox.WriteTo()
    )
    User.set_temp_property("WriteFor", "Men")

    Bot.answer_callback_query(Call.id)

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("Random"))
def ProcessMen(Call: types.CallbackQuery):
    User = Manager.auth(Call.from_user)
    Bot.send_message(
            Call.message.chat.id, 
            f"Супер! Кто-то скоро обрадуется твому посланию!)\nУ тебя лимит на 200 символов 👇"
    )
    User.set_temp_property("WriteTo", "Random")
    User.set_expected_type("Letter")

    Bot.answer_callback_query(Call.id)

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("Dosa"))
def ProcessMen(Call: types.CallbackQuery):
    User = Manager.auth(Call.from_user)
    Bot.send_message(
            Call.message.chat.id, 
            f"Отлично! Кому-то скоро очень крупно повезет!)\nУ тебя лимит на 80 символов 👇"
    )
    User.set_temp_property("WriteTo", "Dosa")
    User.set_expected_type("Letter")

    Bot.answer_callback_query(Call.id)

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("Edit"))
def ProcessEdit(Call: types.CallbackQuery):
    User = Manager.auth(Call.from_user)
    try:
        if User.get_property("Moderation"):
            Bot.send_message(
                    Call.message.chat.id, 
                    "Отправь исправленный текст:"
                    )
            User.set_expected_type("Letter")
    except: Bot.send_message(
            Call.message.chat.id, 
            "Вы отправили пустое сообщение."
            )
    Bot.answer_callback_query(Call.id)

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("Send"))
def ProcessSend(Call: types.CallbackQuery):
    User = Manager.auth(Call.from_user)

    try: 
        Moderator().SaveUserSentences(User.get_property("Moderation"), User.get_property("WriteFor"), User.get_property("WriteTo"))
        Bot.send_message(
                Call.message.chat.id, 
                "Спасибо, текст принят!) Скоро модераторы его проверят, и твое послание увидит большой мир 😘. Пиши ещё!"
                )
    except: Bot.send_message(
            Call.message.chat.id, 
            "Вы отправили пустое сообщение."
            )
    User.clear_temp_properties()

    Bot.answer_callback_query(Call.id)

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("Dose"))
def ProcessDose(Call: types.CallbackQuery):
    dose = None
    User = Manager.auth(Call.from_user)
    if User.get_property("Gender") =="Women":
        dose = reader.GetWD
    if User.get_property("Gender") =="Men":
        dose = reader.GetMD
    
    random_sentence = random.randint(1, len(dose))

    for Index in range(len(dose)):
        if Index == random_sentence-1:
            Bot.send_message(
                Call.message.chat.id,
                text = dose[Index]
                )
            
    Bot.answer_callback_query(Call.id)

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("Change"))
def ProcessChangeName(Call: types.CallbackQuery):
    User = Manager.auth(Call.from_user)
    User.set_expected_type("Name")
    Bot.send_message(
            Call.message.chat.id, 
            "Ну и как теперь тебя называть?")
    User.set_temp_property("Change", True)

    Bot.answer_callback_query(Call.id)

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("Info"))
def ProcessInfo(Call: types.CallbackQuery):
    User = Manager.auth(Call.from_user)

    Bot.send_message(
        Call.message.chat.id,
        text = "@Ddoza\\_bot предназначен сугубо для развлечения и поднятия настроения ☺️\\!\n\nВы будете ежедневно получать сообщения поддержки от нашего любимого бота в абсолютно *рандомное время*, а также сами можете нажимать на кнопку \"💉Доза\" и извлекать определённый заряд позитива\\!\n\nНе упустите шанс написать свое *собственное послание* послание\\! ✉️ Ведь оно может прийти не только другим, но и вам самим 😉\\!\n\n_*Пользуйтесь, и не забывайте делиться с друзьями\\!*_",
        parse_mode= "MarkdownV2"
    )

    Bot.answer_callback_query(Call.id)

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("Settings_daily"))
def ProcessSettingsDaily(Call: types.CallbackQuery):
    User = Manager.auth(Call.from_user)
    
    Bot.send_message(
            Call.message.chat.id, 
            "Выберите подходящий режим:",
            reply_markup=InlineKeyboardsBox.SettingsDaily())
    
    Bot.answer_callback_query(Call.id)

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("Deactivate"))
def ProcessSettingsDaily(Call: types.CallbackQuery):
    User = Manager.auth(Call.from_user)
    
    Bot.send_message(
            Call.message.chat.id, 
            "Эх ты.. А я думал мы друзья! 🥺",
            reply_markup=InlineKeyboardsBox.Sorry())
    
    Bot.answer_callback_query(Call.id)

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("Activate"))
def ProcessSettingsDaily(Call: types.CallbackQuery):
    User = Manager.auth(Call.from_user)
    
    Bot.send_message(
            Call.message.chat.id, 
            "Я рад, что ты взялся за голову! 😉",
            reply_markup=InlineKeyboardsBox.Good())
    
    Bot.answer_callback_query(Call.id)

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("Sorry"))
def ProcessSorry(Call: types.CallbackQuery):
    User = Manager.auth(Call.from_user)
    Bot.send_message(
            Call.message.chat.id, 
            "Ежедневные послания отключены!")
    Bot.delete_message(Call.message.chat.id, Call.message.id)
    User.set_property("Active", False)
    

    Bot.answer_callback_query(Call.id)

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("Good"))
def ProcessGood(Call: types.CallbackQuery):
    User = Manager.auth(Call.from_user)
    Bot.send_message(
            Call.message.chat.id, 
            "Ежедневные послания включены!")
    Bot.delete_message(Call.message.chat.id, Call.message.id)
    User.set_property("Active", True)
    
    Bot.answer_callback_query(Call.id)

@Bot.message_handler(content_types = ["audio", "document", "video"])
def File(Message: types.Message):
    User = Manager.auth(Message.from_user)
    AdminPanel.procedures.files(Bot, User, Message)

AdminPanel.decorators.photo(Bot, Manager)

Bot.infinity_polling()

