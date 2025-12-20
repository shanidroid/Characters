from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.error import BadRequest
import json
import os
import asyncio

BOT_TOKEN = "8506052391:AAGGsfR_JZDJodEYPYbJDRkrJ-XoiOcatI0"

#путь к директории скрипта
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(SCRIPT_DIR, 'users.json')
CHARACTERS_FILE = os.path.join(SCRIPT_DIR, 'characters.json')

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


PHOTO_FILE_IDS = {
    "Кагуя Синомия": "AgACAgIAAxkBAAOkaUXDglTf8cRV-LRbdBAy3Dqsd9wAAu8SaxuIuylKMIrvx355FW8BAAMCAAN3AAM2BA",
    "Микаса Аккерман": "AgACAgIAAxkBAAOmaUXEMAtxWoiiTEqOKmrhQjn3lRsAAiUPaxuOpzFKvsEB3YuZDMABAAMCAAN4AAM2BA",
    "Марин Китагава": "AgACAgIAAxkBAAOoaUXEQXugMByHwRM22qLW3Knb650AAiYPaxuOpzFKComT5Fc-vqIBAAMCAAN5AAM2BA",
    "Эмилия": "AgACAgIAAxkBAAOqaUXEQyPPB9wLTRrF3IrKfH2HCo8AAicPaxuOpzFKrl9nCO45HjMBAAMCAAN5AAM2BA",
    "Рем": "AgACAgIAAxkBAAOsaUXESIusOZ0opv6EWkZg58jJKUAAAigPaxuOpzFKTmcchQ21iKcBAAMCAAN5AAM2BA",
    "Асуна Юки": "AgACAgIAAxkBAAOuaUXETOJ63yxH8RixE-7GaBRU37EAAikPaxuOpzFKA3L_AAF4nknxAQADAgADeQADNgQ",
    "Рори Меркьюри": "AgACAgIAAxkBAAOwaUXETpwDZ9Yo0EYn2zYRH8vxU50AAioPaxuOpzFKTveKQbuwZMgBAAMCAAN5AAM2BA",
    "Май Сакураджима": "AgACAgIAAxkBAAOyaUXEUcATMkvGYnCWd8jrWohdTo4AAisPaxuOpzFK6wAB-ttq4KIDAQADAgADeQADNgQ",
    "Нобара Кугисаки": "AgACAgIAAxkBAAO0aUXEVboNtQZvjR6qCSyQs4YWwAkAAiwPaxuOpzFKd6kE075WpCsBAAMCAAN4AAM2BA",
    "Маки Дзэнэн": "AgACAgIAAxkBAAO2aUXEV0_j0eFbYh90EstQ05rW_8gAAi0PaxuOpzFKuZpE16XRKfYBAAMCAAN4AAM2BA",
    "Тацумаки": "AgACAgIAAxkBAAO4aUXEW5ssuWCcThtdxaYkVBBDUqsAAi4PaxuOpzFKRXaY7tXnDJIBAAMCAAN5AAM2BA",
    "Фубуки": "AgACAgIAAxkBAAO6aUXEXR52gfx8vzTqUCfAgT-rJcgAAi8PaxuOpzFKzyOd_mV42-wBAAMCAAN4AAM2BA",
    "Хината Хьюга": "AgACAgIAAxkBAAO8aUXEYBuMAWpmF5LACEfcoE3NtdgAAjAPaxuOpzFKTqzTtuQJ2NoBAAMCAAN4AAM2BA",
    "Цунаде": "AgACAgIAAxkBAAO-aUXEYvsMMLLRrXAe00nRB2A-bhQAAjIPaxuOpzFKuj9NbVhH2UsBAAMCAAN5AAM2BA",
    "Люси": "AgACAgIAAxkBAAPAaUXEam9qCuhIfBIxrE_zTN6l8VEAAjMPaxuOpzFK_oKMF63FqkkBAAMCAAN5AAM2BA",
    "Мирай Курияма": "AgACAgIAAxkBAAPDaUXEgwdq4nKOwPAtwOQxzCzuVtcAAjQPaxuOpzFK7Wu2bmFa-3MBAAMCAAN5AAM2BA",
    "Мей Мей": "AgACAgIAAxkBAAPFaUXEiOx_OG8AAYzCSc-QoloupP8oAAI1D2sbjqcxSvYDAzbHYnZNAQADAgADeAADNgQ",
    "Ребекка": "AgACAgIAAxkBAAPHaUXEi8Isg4tpuTv4vQZY1K-OnOsAAjYPaxuOpzFKPQ_ISJEvslUBAAMCAAN4AAM2BA",
    "Шиона": "AgACAgIAAxkBAAPJaUXEj-zI68ewTbBfjx0Mndju9V8AAjcPaxuOpzFKUfVb5s-3uVIBAAMCAAN4AAM2BA",
    "Реви": "AgACAgIAAxkBAAPLaUXElCRcCC-cDdSjEq_83iZAPKsAAjgPaxuOpzFKTr54Wfm3xU0BAAMCAAN5AAM2BA"
}

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
        traits = char.get("personality_traits", [])


        if name == "Кагуя Синомия":
            intro = "Ты осмелился прийти ко мне лично?.. Интересно. Я — Кагуя Синомия, вице-президент студенческого совета академии Шучиин. Раньше я была холодной и рассудительной личностью, но вступление в совет и появление тебя изменило меня."
            dialog = [
                {"text": "Если хочешь, то ты мог бы стать ползным для меня как для вице-президента.", "options": ["К Вашим услугам, с радостью)", "Я не против, можем даже подружиться."]},
                {"text": "Хм… Ты действительно не из робких. Но готов ли идти до конца?", "options": ["Готов.", "Теперь это мой личный вызов."]}
            ]
            end = "Кагуя слегка улыбнулась… и прошептала: «Так держать, заместитель)». Вы улучшили свой статус и отношения с Синомией, Ваша уверенность показала Вас в лучшем свете!(Продолжение следует. . .)"

        elif name == "Микаса Аккерман":
            intro = "Вы вступили в Отряд Разведки. Первые дни адаптации проходят в суровой атмосфере. Во время тактической подготовки на вас неожиданно обращает внимание сама Микаса Аккерман. Её серый, аналитический взгляд останавливается на вас, оценивая."
            dialog = [
                {"text": "Новобранец, должно быть, ты очень силён, раз попал в нашу группу?", "options": ["Не думаю, что я лучше вас, Микаса", "Не думаю, что я лучше вас, Микаса"]},
                {"text": "В любом случае, я довольна твоим появлением.", "options": ["Спасибо, я не подведу!", "Я стану верным человеком для Вас, Микаса, в бою"]}
            ]
            end = "Микаса тихо взяла тебя за руку и искренне тихо сказала, что очень благодарна тебе за это. (Вы улучшили отношения с Микасой Аккерман и расположили её своей верностью) (Продолжение следует. . .)"

        elif name == "Марин Китагава":
            intro = "Вы новичок в классе, куда перевелась знаменитая на всю школу Марин Китагава — обаятельная, невероятно популярная и яркая девушка, известная своей страстью к аниме и косплею. ( Весь её мир вращается вокруг косплея, аниме, моды и образов. Если вы разделяете её страсть — вы мгновенно становитесь VIP-персоной.) После уроков вы случайно сталкиваетесь с ней на пустой лестничной клетке"
            dialog = [
                {"text": "О! Ты же новенький из нашего класса, верно? Ты любишь косплей?", "options": ["О, нет-нет, я не эксперт... Просто немного увлекаюсь.", "Да, мне это нравится. Рад встретить человека со вкусом!"]},
                {"text": "А не хочешь примерить костюм вместе со мной? Будет весело!", "options": ["Парные косплеи? Звучит интересно)", "Давай, я давно хотел попробовать что-то подобное"]}
            ]
            end = "Марин радостно обняла тебя! «Теперь ты — мой партнёр на выступлениях!» (Вы значительно улучшили отношения и сильно заинтересовали Марин общим увлечением) (Продолжение следует. . .)"

        elif name == "Эмилия":
            intro = "Вы — новый кандидат на службу при Королевском дворце Лугуника, прибывший на испытательный срок. В одной из бесконечных библиотечных залов, среди стеллажей с древними томами, вы случайно наталкиваетесь на неё. Эмилия, полуэльф с серебристыми волосами и аметистовыми глазами, в изящном белом платье, задумчиво перебирает свитки. Она оборачивается, услышав ваш шаг."
            dialog = [
                {"text": "Ты... новый служащий? Пакт сказал мне, что сегодня ждут кого-то. Приятно познакомиться. Я — Эмилия.", "options": ["Да, это я, приятно познакомиться", "Да, я прибыл на службу, прекрасная леди"]},
                {"text": " О, приветствую… Надеюсь, ты не боишься моих ушей? Я — Эмилия из королевства Лугуника.", "options": ["Леди Эмилия, мне даже нравятся ваши уши!", "Для меня честь просто находиться в вашем присутствии, леди Эмилия"]}
            ]
            end = "Её щёки слегка розовеют от такой прямой почтительности. Она выглядит немного смущённой, но тронутой (Продолжение следует. . .)"

        elif name == "Рем":
            intro = "Вы — новый слуга, только что принятый в особняк Розвааль. Вас определили на кухню для помощи по хозяйству. Войдя в столовую для утреннего инструктажа, вы видите её. Рэм, в безупречно чистом горничном платье с фартуком, стоит, выпрямив спину, руки сложены перед собой. Её ледяные голубые глаза без тени эмоций оценивают вас с ног до головы, словно сканируя"
            dialog = [
                {"text": "Первое задание — отполировать столовое серебро в бальном зале. Не оставить ни единого развода. Это Вам под силу?", "options": ["Да! Я Вас не разочарую!", "Принято, будет сделано по высшему разряду, миледи)"]},
                {"text": "Могу пожелать Вам только удачи)", "options": ["Спасибо, моя Рем", "Благодарю)"]}
            ]
            end = "Рем улыбнулась впервые за долгое время… и прошептала: «Спасибо, что будете помогать моей сестре». (Продолжение следует. . .)"

        elif name == "Асуна Юки":
            intro = "Вы — новый игрок, недавно присоединившийся к «Гильдии Игроков Прогресса» на передовой. После тяжёлой тренировки на полях низкоуровневых мобов вы заходите в тихую таверну «Спящий рыцарь» на 61-м этаже, чтобы восстановить силы. В углу, за столиком у камина, сидит она. Асуна, «Вспышка», вице-командир гильдии «Рыцари Кровавой Клятвы». Её волосы отливают огнём, а взгляд, устремлённый на голографическое меню с отчётами, сосредоточен и серьёзен. На её накидке горит знаменитая эмблема гильдии. Она отвлекается от данных, почувствовав на себе ваш взгляд."
            dialog = [
                {"text": "Ты... из новобранцев на вчерашнем рекрутинге? Видела тебя на тренировочном полигоне. Неплохие базовые навыки с одноручником, но переходы между комбо рывками оставляли тебя открытым. Это опасно на фронте.", "options": ["Спасибо за наблюдение, вице-командир. Я как раз над этим работаю. Есть ли у вас совет?", "Учту!"]},
                {"text": "Если хочешь... я могу показать тебе оптимальный паттерн для твоего типа оружия. Здесь, в таверне, есть симулятор низкого уровня. Десять минут. Но только если ты серьёзно настроен улучшаться. У меня нет времени на тех, кто сдаётся после первой неудачи", "options": ["Большое спасибо! Я рассчитываю закрыть эту слабость уникальным скиллом, который сейчас прокачиваю. На фронте я не подведу."]}
            ]
            end = "Асуна, закончив свой короткий инструктаж у симулятора, на секунду задерживается. Её взгляд, обычно устремлённый вдаль на невидимые тактические карты, смягчается и фокусируется на вас. Она делает небольшой, едва заметный кивок, но не тот отрывистый, деловой, каким отдаёт приказы. Этот кивок — чуть медленнее, с лёгким прищуром глаз, словно она ставит мысленную «галочку» напротив вашего имени в списке «перспективных, а не безнадёжных» (Продолжение следует. . .)"

        elif name == "Рори Меркьюри":
            intro = "Вы — новый гражданский сотрудник или младший дипломат, прикомандированный к группе взаимодействия с Особого Региона. После официального брифинга в лагере Сил Самообороны вы решили осмотреться. Возле импровизированного тира, раздаются оглушительные выстрелы из чего-то очень крупнокалиберного. Там стоит она. Рори Меркури, апостол Эмпресс, в своём узнаваемом чёрном готическом платье, с невозмутимым, почти скучающим выражением на лице. Она только что изрешетила манекен в доспехах из своей гигантской зубы-пулемёта, которую теперь непринуждённо кладёт на плечо. Её сверкающие глаза замечают вас."
            dialog = [
                {"text": "А~а? Ещё один человечек из «той» стороны. Ты пахнешь... бумагами, правилами и страхом. Скучно. Ты пришёл поиграть со мной? Или просто будешь стоять и дрожать?", "options": ["Боюсь, моя игра — это документы и переговоры. Но я могу понаблюдать. Ваша... техника впечатляет.", "Я хочу понаблюдать)"]},
                {"text": "Не боишься моей бессмертной натуры?", "options": ["Бояться? Пожалуй. Но больше — уважать. Бояться можно грозы или дикого зверя, а с уважением можно вести диалог. Вы — сила природы, Апостол. Глупо не признавать этого. Но я здесь, чтобы строить мосты, а не провоцировать ураганы", "Ваше бессмертие делает вас уникальным активом и... проблемой одновременно. Бояться проблемы — неэффективно. Её нужно изучать и искать точки взаимодействия. Страх сковывает разум, а он мне нужен, чтобы быть для вас интересным"]}
            ]
            end = "Рори рассмеялась — и впервые за века почувствовала… покой.(Продолжение следует. . .)"

        elif name == "Май Сакураджима":
            intro = "Вы — новый ученик, переведённый в старшую школу Минегахара. По странному стечению обстоятельств, вы оказались единственным посетителем почти пустой публичной библиотеки в будний день. И именно там вы её видите. Сидящую за дальним столиком у окна, в потоках послеобеденного солнца. Май Сакурадзима, знаменитая юная актриса, в своей обычной, элегантной, но неброской повседневной одежде"
            dialog = [
                {"text": "Ты новенький.Не вопрос, а констатация.", "options": ["Да, сегодня первый день. А вы... вы из старших классов?", "Да, а откуда Вы узнали?"]},
                {"text": "Май Сакурадзима. Третий год. И да, я часто тут сижу.  Называй по имени.", "options": ["Май… ", "Приятно познакомиться..."]}
            ]
            end = "Май улыбнулась без маски.(Продолжение следует. . .)"

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


        file_id = PHOTO_FILE_IDS.get(name)
        
        characters_dict[name] = {
            "anime": anime,
            "traits": traits,
            "intro": intro,
            "dialog": dialog,
            "end": end,
            "photo_file_id": file_id
        }

    return characters_dict


characters = load_characters()
if not characters:
    raise RuntimeError(f"Не удалось загрузить персонажей из {CHARACTERS_FILE}!")
else:
    print("Доступные персонажи загрузились")

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
        "Доступные команды:\n"
        "/by_name — выбрать персонажа по имени\n"
        "/help — помощь в использовании\n"
        "/reset — сбросить прогресс\n"
        "/list — список всех персонажей\n\n",
        reply_markup=ReplyKeyboardRemove()
    )

async def help_command(update, context):
    await update.message.reply_text(
        "Помощь:\n\n"
        "/start — начать игру\n"
        "/by_name — выбрать девушку по имени\n"
        "/list — показать список всех персонажей\n"
        "/reset — сбросить текущий диалог\n"
        "/help — помощь\n\n"
        "Как играть:\n"
        "1. Выберите персонажа\n"
        "2. Отвечайте на вопросы\n"
        "3. Доведите диалог до конца!\n\n"
        "Удачи в свиданиях!"
    )

async def list_characters(update, context):
    names = list(characters.keys())
    message = "Список доступных персонажей:\n\n"
    
    for i, name in enumerate(names, 1):
        anime = characters[name]["anime"]
        message += f"{i}. {name} — {anime}\n"
    
    message += "\nИспользуйте /by_name для выбора"
    
    await update.message.reply_text(message)

async def by_name(update, context):
    users_db = load_users()
    user_id = str(update.effective_user.id)
    
    if user_id not in users_db:
        await update.message.reply_text("Сначала начните: /start")
        return

    users_db[user_id]['state'] = 'choose_girl'
    save_users(users_db)

    names = list(characters.keys())
    keyboard = []

    for i in range(0, len(names), 2):
        row = names[i:i+2]
        keyboard.append(row)
    
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        one_time_keyboard=True,
        resize_keyboard=True,
        input_field_placeholder="Выберите девушку"
    )
    
    try:
        await update.message.reply_text(
            "Выберите аниме-девушку для свидания:",
            reply_markup=reply_markup
        )
    except Exception as e:
        print(f"Ошибка отправки клавиатуры: {e}")
        await update.message.reply_text(
            "Выберите девушку из списка:\n\n" + "\n".join(names)
        )

async def reset(update, context):
    users_db = load_users()
    user_id = str(update.effective_user.id)
    
    if user_id in users_db:
        del users_db[user_id]
        save_users(users_db)
    
    await update.message.reply_text(
        "Прогресс сброшен\n\n"
        "Начните заново: /start",
        reply_markup=ReplyKeyboardRemove()
    )

async def start_dialog(update, context, girl_name):
    girl = characters[girl_name]
    
    if girl.get('photo_file_id'):
        try:
            await update.message.reply_photo(
                photo=girl['photo_file_id'],
                caption=f"{girl_name}\n\n{girl['intro']}"
            )
        except BadRequest as e:
            print(f"Ошибка отправки фото для {girl_name}: {e}")
            await update.message.reply_text(
                f"{girl_name}\n\n{girl['intro']}"
            )
    else:
        await update.message.reply_text(
            f"{girl_name}\n\n{girl['intro']}"
        )

    await send_dialog_step(update, context, girl_name, 0)

async def send_dialog_step(update, context, girl_name, step):
    girl = characters[girl_name]
    dialog_step = girl['dialog'][step]


    keyboard = [[dialog_step['options'][0]], [dialog_step['options'][1]]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


    await update.message.reply_text(
        dialog_step['text'],
        reply_markup=reply_markup
    )

async def handle_message(update, context):
    text = update.message.text


    users_db = load_users()
    user_id = str(update.effective_user.id)
    
    if user_id not in users_db:
        await update.message.reply_text("Начните с /start")
        return
    
    user_state = users_db[user_id]['state']
    
    if user_state == 'choose_mode':
        await update.message.reply_text(
            "Используйте команды:\n"
            "/by_name — выбрать персонажа\n"
            "/help — помощь\n"
            "/reset — сбросить прогресс"
        )
        
    elif user_state == 'choose_girl':
        if text in characters:
            user = users_db[user_id]
            user['chosen_girl'] = text
            user['state'] = 'dialog'
            user['dialog_step'] = 0
            save_users(users_db)
            
            await start_dialog(update, context, text)
        else:
            names = list(characters.keys())
            keyboard = []
            
            for i in range(0, len(names), 2):
                row = names[i:i+2]
                keyboard.append(row)
            
            reply_markup = ReplyKeyboardMarkup(
                keyboard,
                one_time_keyboard=True,
                resize_keyboard=True
            )
            
            await update.message.reply_text(
                f"Персонаж '{text}' не найден.\n\n"
                "Выберите девушку из списка:",
                reply_markup=reply_markup
            )
    
    elif user_state == 'dialog':
        girl_name = users_db[user_id]['chosen_girl']
        step = users_db[user_id]['dialog_step']
        
        if girl_name not in characters:
            await update.message.reply_text("Ошибка: персонаж не найден. Начните заново: /start")
            users_db[user_id]['state'] = 'choose_mode'
            save_users(users_db)
            return
            
        dialog = characters[girl_name]['dialog']
        
        if step >= len(dialog):
            return


        if text in dialog[step]['options']:
            users_db[user_id]['dialog_step'] += 1
            save_users(users_db)
            
            if users_db[user_id]['dialog_step'] >= len(dialog):
                users_db[user_id]['state'] = 'end'
                save_users(users_db)
                
                end_text = characters[girl_name]['end']
                
                girl_data = characters[girl_name]
                if girl_data.get('photo_file_id'):
                    try:
                        await update.message.reply_photo(
                            photo=girl_data['photo_file_id'],
                            caption=f"Конец диалога!\n\n{end_text}"
                        )
                    except BadRequest:
                        await update.message.reply_text(
                            f"Конец диалога!\n\n{end_text}"
                        )
                else:
                    await update.message.reply_text(
                        f"Конец диалога!\n\n{end_text}"
                    )
                    
                await update.message.reply_text(
                    "Диалог успешно завершён!\n\n"
                    "Что хотите сделать дальше?\n"
                    "• /by_name — выбрать другую девушку\n"
                    "• /start — начать заново\n"
                    "• /list — список персонажей",
                    reply_markup=ReplyKeyboardRemove()
                )
            else:
                await send_dialog_step(update, context, girl_name, users_db[user_id]['dialog_step'])
        else:
            await send_dialog_step(update, context, girl_name, step)
    
    elif user_state == 'end':
        await update.message.reply_text(
            "Диалог завершён. Используйте команды:\n"
            "/start — начать заново\n"
            "/by_name — выбрать другую девушку"
        )

async def error_handler(update, context):
    print(f"Ошибка: {context.error}")
    
    try:
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "Произошла ошибка. Пожалуйста, попробуйте снова или используйте /start"
            )
    except Exception as e:
        print(f"Ошибка в обработчике ошибок: {e}")

async def get_file_id(update, context):
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        file_unique_id = update.message.photo[-1].file_unique_id
        
        await update.message.reply_text(
            f"Информация о фото:\n\n"
            f"File ID:\n{file_id}\n\n"
            f"File Unique ID:\n{file_unique_id}"
        )
    else:
        await update.message.reply_text("Отправьте фото (не файл!)")

def main():
    application = Application.builder() \
        .token(BOT_TOKEN) \
        .read_timeout(30) \
        .write_timeout(30) \
        .connect_timeout(30) \
        .pool_timeout(30) \
        .build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("list", list_characters))
    application.add_handler(CommandHandler("by_name", by_name))
    application.add_handler(CommandHandler("reset", reset))
    application.add_handler(CommandHandler("get_file_id", get_file_id))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.add_handler(MessageHandler(filters.PHOTO, get_file_id))

    application.add_error_handler(error_handler)
    
    print("=" * 50)
    print("Бот запущен")
    print(f"Загружено персонажей: {len(characters)}")


    application.run_polling(
        drop_pending_updates=True,
        allowed_updates=["message", "callback_query"]
    )

if __name__ == "__main__":
    main()