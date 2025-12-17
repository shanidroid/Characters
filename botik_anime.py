from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import json
import os
import requests


BOT_TOKEN = ""
DB_FILE = 'users.json'
CHARACTERS_FILE = 'characters.json'
NEKOS_API_URL = "https://nekos.best/api/v2/waifu"


def load_users():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_users(users):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)


def get_anime_image():
    try:
        response = requests.get(NEKOS_API_URL, timeout=5)
        if response.status_code == 200:
            return response.json()['results'][0]['url']
    except Exception as e:
        print(f"Ошибка загрузки изображения: {e}")
    return None


def load_characters():
    try:
        with open(CHARACTERS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            raw_list = data.get("female_anime_characters", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка загрузки {CHARACTERS_FILE}: {e}")
        return {}


    characters_dict = {}
    for char in raw_list:
        name = char["name"]
        anime = char["anime"]
        traits = char["personality_traits"]

        if name == "Кагуя Синомия":
            intro = "Ты осмелился прийти ко мне лично?.. Интересно. Я — Кагуя Синомия, вице-президент студенческого совета."
            dialog = [
                {"text": "Если ты хочешь, чтобы я призналась первой… докажи, что достоин.", "options": ["Я сделаю всё, чтобы ты улыбнулась!", "Я не боюсь твоих игр."]},
                {"text": "Хм… Ты действительно не из робких. Но готов ли идти до конца?", "options": ["Готов. Я влюбился с первого взгляда.", "Ты — мой интеллектуальный вызов."]}
            ]
            end = "Кагуя слегка улыбнулась… и прошептала: «Ты победил… любимый». Вы стали парой!"

        elif name == "Микаса Аккерман":
            intro = "Если ты не враг — не мешай. Но если ты рядом… я защищу тебя до последнего вздоха."
            dialog = [
                {"text": "Почему ты ищешь меня? Ты в опасности?", "options": ["Я хочу быть тем, кого ты защищаешь", "Я восхищаюсь твоей силой"]},
                {"text": "Ты… не похож на остальных. Ты смотришь в мои глаза без страха.", "options": ["Ты — мой человек", "Я останусь с тобой навсегда"]}
            ]
            end = "Микаса тихо взяла тебя за руку. В её глазах — тепло. Вы — пара."

        elif name == "Марин Китагава":
            intro = "Привет! Ты смотришь на меня… Может, хочешь сфоткать мой косплей? Или… чего-то большего?"
            dialog = [
                {"text": "Ты любишь косплей? Или просто… меня?", "options": ["Ты восхитительна в любом образе!", "Мне нравится твоя энергия!"]},
                {"text": "А не хочешь примерить костюм вместе со мной? Будет весело!", "options": ["Только если ты рядом!", "Давай начнём наше приключение!"]}
            ]
            end = "Марин радостно обняла тебя! «Ты — мой любимый партнёр по жизни!»"

        elif name == "Эмилия":
            intro = "О, приветствую… Надеюсь, ты не боишься моих ушей? Я — Эмилия из королевства Лугуника."
            dialog = [
                {"text": "Ты веришь в меня… даже зная, что я наполовину дух?", "options": ["Ты прекрасна внутри и снаружи", "Я с тобой, что бы ни случилось"]},
                {"text": "Тогда… пойдёшь со мной в лес? Там красиво… и тихо.", "options": ["Только с тобой мне безопасно", "Да, я хочу быть рядом вечно"]}
            ]
            end = "Эмилия взяла тебя за руку, и лёгкий снежок закружился вокруг вас. Вы стали парой!"

        elif name == "Рем":
            intro = "Рем здесь. Если ты враг — получишь лопатой. Если друг… Рем испечёт тебе пирожное."
            dialog = [
                {"text": "Ты… правда хочешь быть со мной? А не с той, с сестрой?", "options": ["Ты — единственная для меня", "Мне нужна только ты, Рем"]},
                {"text": "Тогда… Рем твоя. Навсегда.", "options": ["Спасибо, моя Рем", "Я сделаю тебя счастливой"]}
            ]
            end = "Рем улыбнулась впервые за долгое время… и прошептала: «Спасибо, что выбрал меня»."

        elif name == "Асуна Юки":
            intro = "Привет! Я Асуна — «Молния» из «Айнкрэда». Но сейчас я просто хочу быть с тобой."
            dialog = [
                {"text": "Ты готов сражаться за наши отношения, как в SAO?", "options": ["Я пройду любой босс ради тебя!", "Ты — мой главный квест"]},
                {"text": "Тогда держи мою руку… и не отпускай.", "options": ["Никогда!", "Ты — моя жизнь"]}
            ]
            end = "Асуна обняла тебя, и вы смотрите на виртуальный закат вместе. Любовь победила!"

        elif name == "Рори Меркьюри":
            intro = "Привет, смертный! Я Рори — апостол богини Эмпресс. Мне скучно… а ты?"
            dialog = [
                {"text": "Хочешь потанцевать в битве? Или просто полежать в обнимку?", "options": ["Давай устроим безумное приключение!", "Я хочу быть твоим утешением"]},
                {"text": "Хех… Ты не боишься моей бессмертной натуры?", "options": ["Ты — моя вечность", "Я буду рядом в каждой жизни"]}
            ]
            end = "Рори рассмеялась — и впервые за века почувствовала… покой. Вы — пара навеки."

        elif name == "Май Сакураджима":
            intro = "Ты смотришь на меня, как на «иконку»? Или видишь настоящую Май?"
            dialog = [
                {"text": "Готов ли ты увидеть мою уязвимость за сарказмом?", "options": ["Я люблю тебя настоящую", "Ты — больше, чем образ"]},
                {"text": "Тогда… не называй меня «Банни-гёрл». Называй по имени.", "options": ["Май… ты моя", "Я рядом, как бы ни было"]}
            ]
            end = "Май улыбнулась без маски. «Ты — мой первый настоящий друг… и любовь»."

        elif name == "Нобара Кугисаки":
            intro = "Йо! Ты выглядишь неплохо. Не то что эти слабаки в академии!"
            dialog = [
                {"text": "Ты уверен, что хочешь быть со мной? Я не из нежных!", "options": ["Ты — огонь!", "Я выдержу твой характер"]},
                {"text": "Ха! Тогда докажи — не трусь, как Итадори!", "options": ["Я с тобой до конца", "Ты — моя сила"]}
            ]
            end = "Нобара подмигнула: «Ладно, ты зачётный! Будешь моим!»"

        elif name == "Маки Дзэнэн":
            intro = "Я — Маки. Не говори лишнего. Просто будь рядом, если достоин."
            dialog = [
                {"text": "Ты хочешь быть моим напарником? Или просто болтать?", "options": ["Я хочу сражаться с тобой плечом к плечу", "Ты вдохновляешь меня"]},
                {"text": "Тогда докажи это на деле. Готов?", "options": ["Всегда", "Ты — мой ориентир"]}
            ]
            end = "Маки кивнула. В её глазах — уважение. Вы — идеальная пара бойцов."

        elif name == "Тацумаки":
            intro = "Что тебе надо, смертный? Если это не важно — исчезни."
            dialog = [
                {"text": "Ты осмелился подойти ко мне? У тебя что, нет страха?", "options": ["Ты сильнее, чем думаешь", "Я не боюсь — я восхищаюсь"]},
                {"text": "Хм… Ты… не раздражаешь. Пока.", "options": ["Позволь остаться рядом", "Я приму твой характер"]}
            ]
            end = "Тацумаки фыркнула… но не оттолкнула твою руку. «Ладно, оставайся…»"

        elif name == "Фубуки":
            intro = "Ты из моего фан-клуба? Или… хочешь большего? Я — Фубуки, лидер «Холодного снега»."
            dialog = [
                {"text": "Готов ли ты стать частью моей команды — не как фанат, а как партнёр?", "options": ["Я хочу быть твоей силой", "Ты — моя героиня"]},
                {"text": "Тогда докажи, что ты не просто ещё один поклонник.", "options": ["Я ценю тебя как личность", "Ты — мой идеал"]}
            ]
            end = "Фубуки улыбнулась уверенно: «Ты — мой новый герой»."

        elif name == "Хината Хьюга":
            intro = "З-здравствуйте… Я Хината. Надеюсь, я не помешала…"
            dialog = [
                {"text": "Ты… правда хочешь быть со мной? Я такая робкая…", "options": ["Ты очень храбрая", "Мне нравится твоя доброта"]},
                {"text": "Тогда… я постараюсь быть сильнее. Ради нас.", "options": ["Я всегда рядом", "Ты — моя опора"]}
            ]
            end = "Хината наконец-то смотрит тебе в глаза без стеснения. Вы — пара!"

        elif name == "Цунаде":
            intro = "Хм? Ты сюда за делом или… за мной? У меня нет времени на глупости."
            dialog = [
                {"text": "Ты уверен, что готов к отношениям с женщиной, которая старше тебя на десятки лет?", "options": ["Возраст — лишь цифра", "Ты — легенда, и моя любовь"]},
                {"text": "Хех… Может, ты и прав. Но я не прощу предательства.", "options": ["Я верен", "Ты — моя покойница"]}
            ]
            end = "Цунаде улыбнулась — и залила всё саке. «Ты — мой новый ученик… и любовь»."

        elif name == "Люси":
            intro = "Ты смотришь на меня… как на мечту? Или на ошибку? Я — Люси из ночного города."
            dialog = [
                {"text": "Ты готов любить меня… даже зная, какая я — наполовину машина?", "options": ["Ты — человек в самом глубоком смысле", "Я люблю тебя всей душой"]},
                {"text": "Тогда… уйдем отсюда. Найдём своё место в этом мире.", "options": ["Да, мой рай — с тобой", "Я последую за тобой в ад"]}
            ]
            end = "Люси отключила импланты и заплакала. «Ты вернул мне человечность»."

        elif name == "Мирай Курияма":
            intro = "А-а! Прости, я не хотела тебя напугать… Я Мирай. Хочешь чаю?"
            dialog = [
                {"text": "Я… неуклюжая. Ты не уйдёшь, если я уроню чашку?", "options": ["Ты милая даже в этом", "Я люблю твою искренность"]},
                {"text": "Правда? Тогда… можно держать тебя за руку?", "options": ["Всегда", "Ты — моё чудо"]}
            ]
            end = "Мирай осторожно обняла тебя. «Спасибо, что не боишься мою кровь…»"

        elif name == "Мей Мей":
            intro = "Привет, сладкий! Я Мей Мей — бизнес-леди и проклятый техник. Готов инвестировать в любовь?"
            dialog = [
                {"text": "Ты хочешь быть моим партнёром? В бизнесе… или в жизни?", "options": ["В жизни — это мой главный проект", "Ты — моя инвестиция в счастье"]},
                {"text": "Хех… Ты знаешь, сколько стоят мои услуги? А любовь — бесплатно.", "options": ["Тогда я беру всё", "Ты — бесценно"]}
            ]
            end = "Мей Мей щёлкнула вороном: «Сделка заключена. Ты — мой»."

        elif name == "Ребекка":
            intro = "Йо! Ты выжил в этом аду? Тогда, может, выживем вместе? Я — Ребекка."
            dialog = [
                {"text": "Готов ли ты мчаться со мной сквозь пули и неон?", "options": ["Я твой напарник до конца", "С тобой даже ад — рай"]},
                {"text": "Тогда держись крепче! У нас есть вся ночь!", "options": ["Вперёд, моя Ребекка!", "Я с тобой в любом мире"]}
            ]
            end = "Ребекка схватила тебя за руку и рванула в неоновую ночь. Вы — пара эджерынов!"

        elif name == "Шиона":
            intro = "Добро пожаловать. Я Шиона — дух воды. Надеюсь, твоё сердце чисто."
            dialog = [
                {"text": "Ты ищешь спокойствия… или меня?", "options": ["Ты — мой покой", "Твоя мудрость притягивает меня"]},
                {"text": "Тогда позволь мне очистить твою душу… и остаться рядом.", "options": ["Да, Шиона", "Я доверяю тебе полностью"]}
            ]
            end = "Шиона создала водяной цветок в твоих ладонях. «Ты — мой избранник»."

        elif name == "Реви":
            intro = "Если ты не по делу — уходи. Я не нянька и не подружка. Я — Реви."
            dialog = [
                {"text": "Ты хочешь быть со мной? Знай: я не буду тебя спасать.", "options": ["Я сам справлюсь, но хочу быть с тобой", "Ты — мой идеал силы"]},
                {"text": "Хм… Ты не из болтунов. Может, ты и правда достоин.", "options": ["Я уважаю тебя", "Ты — моя команда"]}
            ]
            end = "Реви бросила тебе патрон как символ. «Ты — мой человек»."

        else:
            intro = f"Привет! Я {name} из «{anime}»."
            dialog = [
                {"text": "Рада тебя видеть!", "options": ["И я тебя!", "Ты прекрасна!"]},
                {"text": "Хочешь быть со мной?", "options": ["Да!", "Конечно!"]}
            ]
            end = f"{name} улыбнулась. Вы стали парой!"

        characters_dict[name] = {
            "anime": anime,
            "traits": traits,
            "intro": intro,
            "dialog": dialog,
            "end": end
        }

    return characters_dict


characters = load_characters()
if not characters:
    raise RuntimeError(f"Не удалось загрузить персонажей из {CHARACTERS_FILE}!")



async def start(update, context):
    user_id = str(update.effective_user.id)
    users_db = load_users()
    users_db[user_id] = {
        'state': 'choose_mode',
        'chosen_girl': None,
        'dialog_step': 0
    }
    save_users(users_db)
    await update.message.reply_text(
        "Добро пожаловать в симулятор свиданий с аниме-девушками!\n\n"
        "Выберите фенкцию:\n"
        "• /by_name — выбрать персонажа по имени\n"
        "• /help — помощь по экплуатации\n"
        "• /reset — сбросить прогресс",
        reply_markup=ReplyKeyboardRemove()
    )


async def by_name(update, context):
    users_db = load_users()
    user_id = str(update.effective_user.id)
    if user_id not in users_db:
        await update.message.reply_text("Сначала начните: /start")
        return

    users_db[user_id]['state'] = 'choose_girl'
    save_users(users_db)

    names = list(characters.keys())
    keyboard = [[name] for name in names]
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        one_time_keyboard=True,
        resize_keyboard=True,
        input_field_placeholder="Выберите девушку..."
    )
    await update.message.reply_text("Выберите аниме-девушку по имени:", reply_markup=reply_markup)


async def help(update, context):
    await update.message.reply_text(
        "Команды бота:\n"
        "/start — начать игру\n"
        "/by_name — выбрать девушку по имени\n"
        "/reset — сбросить прогресс\n"
        "После выбора — следуйте подсказкам!"
    )


async def reset(update, context):
    users_db = load_users()
    user_id = str(update.effective_user.id)
    if user_id in users_db:
        del users_db[user_id]
        save_users(users_db)
    await update.message.reply_text("Прогресс сброшен. Начните заново: /start")


async def start_dialog(update, context, girl_name):
    girl = characters[girl_name]
    img_url = get_anime_image()
    if img_url:
        await update.message.reply_photo(photo=img_url, caption=girl['intro'])
    else:
        await update.message.reply_text(girl['intro'])
    await send_dialog_step(update, context, girl_name, 0)


async def send_dialog_step(update, context, girl_name, step):
    dialog = characters[girl_name]['dialog'][step]
    opts = dialog['options']
    kb = ReplyKeyboardMarkup([[opts[0], opts[1]]], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(dialog['text'], reply_markup=kb)


async def handle_message(update, context):
    users_db = load_users()
    user_id = str(update.effective_user.id)
    text = update.message.text

    if user_id not in users_db:
        await update.message.reply_text("Начните с /start")
        return

    user = users_db[user_id]
    state = user['state']

    if state == 'choose_girl':
        if text in characters:
            user['chosen_girl'] = text
            user['state'] = 'dialog'
            user['dialog_step'] = 0
            save_users(users_db)
            await start_dialog(update, context, text)
        else:
            await by_name(update, context)

    elif state == 'dialog':
        girl_name = user['chosen_girl']
        step = user['dialog_step']
        dialog = characters[girl_name]['dialog']

        if step >= len(dialog):
            return

        if text in dialog[step]['options']:
            user['dialog_step'] += 1
            save_users(users_db)

            if user['dialog_step'] >= len(dialog):
                user['state'] = 'end'
                save_users(users_db)
                end_text = characters[girl_name]['end']
                img_url = get_anime_image()
                if img_url:
                    await update.message.reply_photo(photo=img_url, caption=end_text)
                else:
                    await update.message.reply_text(end_text)
                await update.message.reply_text("Хотите начать заново? /start")
            else:
                await send_dialog_step(update, context, girl_name, user['dialog_step'])
        else:
            await send_dialog_step(update, context, girl_name, step)

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("by_name", by_name))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("reset", reset))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен каким-то пользователем")
    application.run_polling()

if __name__ == "__main__":
    main()