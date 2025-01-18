# Esteem 
**Esteem** – [Telegram](https://telegram.org)-бот, присылающий ежедневно послания, учитывающие пол, которые повышают самооценку.

# Порядок установки и использования
1. Загрузить репозиторий. Распаковать.

2. Установить [Python](https://www.python.org/downloads/) версии 3.11 и выше. Рекомендуется добавить в PATH.

3. Открыть каталог со скриптом в консоли: можно воспользоваться командой cd или встроенными возможностями файлового менеджера.

4. Создать виртуальное окружение Python.

```
python -m venv .venv
```

5. Активировать вирутальное окружение.

#### Для Windows.
    
```shell
.venv\Scripts\activate.bat
```

#### Для Linux или MacOS.

```bash
source .venv/bin/activate
```

6. Установить зависимости скрипта.

```
pip install -r requirements.txt
```

7. Настроить бота путём редактирования _Settings.json_.

### Settings.json.

```JSON
"token": ""
```

Токен бота Telegram (можно получить у [BotFather](https://t.me/BotFather)).

```JSON
"womens": ""
```

Путь к файлу с женскими посланиями и дозами. Файл должен быть в формате xlsx. В файле должно быть как минимум две колонки. Одна с названием **послания**, вторая - **доза**. При необходимости можно добавить **%s**, который автоматически будет заменяться на имя, которое дал себе пользователь.  

```JSON
"mens": ""
```

Путь к файлу с мужскими посланиями и дозами.


```JSON
"password": ""
```

Пароль для доступа к административной панели.

```JSON
"qr_id": ""
```

Путь к изображению, которое отправляется при нажатии на кнопку "Поделиться с друзьями".


```JSON
"chat_id": null
```

ID пользователя, для формирования кэша изображения описанного выше (смотреть подробнее [TeleCache](https://github.com/DUB1401/dublib/blob/main/docs/TelebotUtils/Cache.md))..

```JSON
"start_dailydose": "06:50"
```

Первый запуск рассылки посланий, в дальнейшем система сама будет определять время рассылки на каждый день в диапазоне с 07:00-20:00.

8. Запустить файл _main.py_.
```
python main.py
``` 

9. Для автоматического запуска рекомендуется провести инициализацию сервиса через [systemd](systemd/README.md) на Linux или путём добавления его в автозагрузку на Windows.

10. Перейти в чат с ботом, токен которого указан в настройках, и следовать его инструкциям.

---
**_Copyright © Dub Irina. 2024-2025._**
