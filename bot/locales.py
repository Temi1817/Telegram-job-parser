LOCALES = {
    'ru': {
        'choose_language': '🌐 Выберите язык интерфейса:',
        'language_set': '✅ Язык установлен: Русский 🇷🇺',
        'welcome': (
            '👋 *Привет!* Я бот для поиска IT-вакансий.\n\n'
            '🔎 Собираю вакансии с *HH.kz*, *Habr Career* и *RemoteOK*,\n'
            'фильтрую по вашим критериям и отправляю новые каждые 30 минут.\n\n'
            '👉 Нажмите *⚙️ Фильтры* чтобы настроить поиск.'
        ),
        # ── Main menu reply buttons ────────────────────────────────────────────
        'btn_search':       '🔍 Найти вакансии',
        'btn_filters':      '⚙️ Фильтры',
        'btn_stats':        '📊 Статистика',
        'btn_pause':        '⏸ Пауза',
        'btn_resume':       '▶️ Продолжить',
        'btn_change_lang':  '🌐 Язык',
        'btn_help':         'ℹ️ Помощь',
        # ── Filters menu ──────────────────────────────────────────────────────
        'filters_menu':         '⚙️ *Ваши фильтры:*',
        'no_filters':           'Фильтры не настроены',
        'set_keywords':         '🔑 Введите ключевые слова через запятую\n_(например: Python, Django, Backend)_:',
        'keywords_saved':       '✅ Ключевые слова: *{keywords}*',
        'set_salary':           '💰 Введите минимальную зарплату в KZT\n_(или 0 чтобы не ограничивать)_:',
        'salary_saved':         '✅ Минимальная зарплата: *{salary} KZT*',
        'set_city':             '🏙️ Введите город\n_(или "удалённо" для remote-вакансий)_:',
        'city_saved':           '✅ Город: *{city}*',
        'set_experience':       '📊 Выберите опыт работы:',
        'experience_saved':     '✅ Опыт: *{experience}*',
        'exp_no':               '🟢 Без опыта',
        'exp_1_3':              '🔵 1–3 года',
        'exp_3_6':              '🟣 3–6 лет',
        'exp_6':                '🔴 Более 6 лет',
        'exp_any':              '⚪️ Любой',
        'set_language_filter':  '🌐 Выберите язык вакансий:',
        'lang_ru':              '🇷🇺 Русский',
        'lang_en':              '🇬🇧 Английский',
        'lang_any':             '🌍 Любой',
        'filters_reset':        '✅ Фильтры сброшены!',
        # ── Sources ───────────────────────────────────────────────────────────
        'sources_title':        (
            '🗂 *Источники вакансий*\n\n'
            'Нажмите на источник чтобы включить или выключить.\n'
            '✅ — активен  ·  ☐ — выключен'
        ),
        'sources_saved':        '✅ Источники сохранены!',
        'no_sources_selected':  '⚠️ Включите хотя бы один источник!',
        'filter_sources':       'Источники',
        'btn_back_to_filters':  '← Назад к фильтрам',
        # ── Inline filter buttons ─────────────────────────────────────────────
        'btn_edit_keywords':    '🔑 Ключевые слова',
        'btn_edit_salary':      '💰 Зарплата',
        'btn_edit_city':        '🏙️ Город',
        'btn_edit_experience':  '📊 Опыт',
        'btn_edit_lang':        '🌐 Язык вакансий',
        'btn_search_now':       '🔍 Искать сейчас',
        'btn_reset_filters':    '🗑 Сбросить',
        'btn_clear_history':    '🔄 Очистить историю',
        'btn_sources':          '🗂 Источники',
        'btn_open_vacancy':     '🔗 Открыть вакансию',
        # ── Filter labels ─────────────────────────────────────────────────────
        'filter_keywords':      'Ключевые слова',
        'filter_salary':        'Мин. зарплата',
        'filter_city':          'Город',
        'filter_experience':    'Опыт',
        'filter_vacancy_lang':  'Язык вакансий',
        'not_set':              'не задано',
        'salary_not_set':       'не указана',
        'btn_back':             '← Назад',
        'invalid_salary':       '❌ Введите число (например: 200000)',
        # ── Stats ─────────────────────────────────────────────────────────────
        'stats_title':          '📊 *Ваша статистика:*',
        'stats_total':          '📨 Всего отправлено: *{count}* вак.',
        'stats_today':          '📅 Сегодня: *{count}*',
        'stats_week':           '📆 За 7 дней: *{count}*',
        'stats_active':         '🤖 Автопоиск: {status}',
        'stats_keywords':       '🔎 Поиск: _{keywords}_',
        'status_on':            'Включён ✅',
        'status_off':           'Выключен ⏸',
        'history_cleared':      '✅ История очищена! Теперь вы снова увидите все вакансии.',
        # ── Search & notifications ────────────────────────────────────────────
        'searching':            '🔍 Ищу подходящие вакансии...',
        'no_new_jobs':          '😕 Новых подходящих вакансий пока нет.\nПроверю снова через 30 минут.',
        'paused':               '⏸ Автопоиск приостановлен.',
        'resumed':              '✅ Автопоиск возобновлён!',
        'already_paused':       'Автопоиск уже приостановлен.',
        'already_active':       'Автопоиск уже активен.',
        'setup_filters_first':  '⚠️ Сначала настройте ключевые слова через ⚙️ Фильтры',
        # ── Help ──────────────────────────────────────────────────────────────
        'help': (
            'ℹ️ *Как пользоваться ботом:*\n\n'
            '🔍 *Найти вакансии* — поиск прямо сейчас\n'
            '⚙️ *Фильтры* — ключевые слова, зарплата, город, опыт\n'
            '📊 *Статистика* — сколько вакансий отправлено\n'
            '⏸ *Пауза* — остановить автоматические уведомления\n'
            '▶️ *Продолжить* — возобновить уведомления\n'
            '🌐 *Язык* — сменить язык интерфейса\n\n'
            '🤖 Бот проверяет новые вакансии *каждые 30 минут*.\n'
            '🗂 Источники: *HH.kz*, *Habr Career*, *RemoteOK*'
        ),
    },

    'kz': {
        'choose_language': '🌐 Интерфейс тілін таңдаңыз:',
        'language_set': '✅ Тіл орнатылды: Қазақша 🇰🇿',
        'welcome': (
            '👋 *Сәлем!* Мен IT-вакансияларды іздейтін ботпын.\n\n'
            '🔎 *HH.kz*, *Habr Career* және *RemoteOK* сайттарынан\n'
            'вакансияларды жинап, критерийлер бойынша сүзіп, 30 минут сайын жіберемін.\n\n'
            '👉 *⚙️ Сүзгілер* батырмасын басып баптаңыз.'
        ),
        'btn_search':       '🔍 Вакансия іздеу',
        'btn_filters':      '⚙️ Сүзгілер',
        'btn_stats':        '📊 Статистика',
        'btn_pause':        '⏸ Тоқтату',
        'btn_resume':       '▶️ Жалғастыру',
        'btn_change_lang':  '🌐 Тіл',
        'btn_help':         'ℹ️ Анықтама',
        'filters_menu':         '⚙️ *Ағымдағы сүзгілеріңіз:*',
        'no_filters':           'Сүзгілер орнатылмаған',
        'set_keywords':         '🔑 Кілт сөздерді үтірмен бөліп жазыңыз\n_(мысалы: Python, Django, Backend)_:',
        'keywords_saved':       '✅ Кілт сөздер: *{keywords}*',
        'set_salary':           '💰 Минималды жалақыны KZT-мен енгізіңіз\n_(немесе 0 шектеусіз)_:',
        'salary_saved':         '✅ Минималды жалақы: *{salary} KZT*',
        'set_city':             '🏙️ Қаланы енгізіңіз\n_(немесе "қашықтан" remote үшін)_:',
        'city_saved':           '✅ Қала: *{city}*',
        'set_experience':       '📊 Жұмыс тәжірибесін таңдаңыз:',
        'experience_saved':     '✅ Тәжірибе: *{experience}*',
        'exp_no':               '🟢 Тәжірибесіз',
        'exp_1_3':              '🔵 1–3 жыл',
        'exp_3_6':              '🟣 3–6 жыл',
        'exp_6':                '🔴 6 жылдан астам',
        'exp_any':              '⚪️ Кез келген',
        'set_language_filter':  '🌐 Вакансия тілін таңдаңыз:',
        'lang_ru':              '🇷🇺 Орысша',
        'lang_en':              '🇬🇧 Ағылшынша',
        'lang_any':             '🌍 Кез келген',
        'filters_reset':        '✅ Сүзгілер тазаланды!',
        'sources_title':        (
            '🗂 *Вакансия көздері*\n\n'
            'Қосу/өшіру үшін көзге басыңыз.\n'
            '✅ — белсенді  ·  ☐ — өшірілген'
        ),
        'sources_saved':        '✅ Көздер сақталды!',
        'no_sources_selected':  '⚠️ Кемінде бір көзді қосыңыз!',
        'filter_sources':       'Көздер',
        'btn_back_to_filters':  '← Сүзгілерге қайту',
        'btn_edit_keywords':    '🔑 Кілт сөздер',
        'btn_edit_salary':      '💰 Жалақы',
        'btn_edit_city':        '🏙️ Қала',
        'btn_edit_experience':  '📊 Тәжірибе',
        'btn_edit_lang':        '🌐 Вакансия тілі',
        'btn_search_now':       '🔍 Қазір іздеу',
        'btn_reset_filters':    '🗑 Тазалау',
        'btn_clear_history':    '🔄 Тарихты тазалау',
        'btn_sources':          '🗂 Көздер',
        'btn_open_vacancy':     '🔗 Вакансияны ашу',
        'filter_keywords':      'Кілт сөздер',
        'filter_salary':        'Мин. жалақы',
        'filter_city':          'Қала',
        'filter_experience':    'Тәжірибе',
        'filter_vacancy_lang':  'Вакансия тілі',
        'not_set':              'орнатылмаған',
        'salary_not_set':       'белгіленбеген',
        'btn_back':             '← Артқа',
        'invalid_salary':       '❌ Санды енгізіңіз (мысалы: 200000)',
        'stats_title':          '📊 *Сіздің статистикаңыз:*',
        'stats_total':          '📨 Барлығы жіберілді: *{count}* вак.',
        'stats_today':          '📅 Бүгін: *{count}*',
        'stats_week':           '📆 7 күнде: *{count}*',
        'stats_active':         '🤖 Автоіздеу: {status}',
        'stats_keywords':       '🔎 Іздеу: _{keywords}_',
        'status_on':            'Қосулы ✅',
        'status_off':           'Өшірілген ⏸',
        'history_cleared':      '✅ Тарих тазаланды! Барлық вакансияларды қайта көресіз.',
        'searching':            '🔍 Сәйкес вакансияларды іздеуде...',
        'no_new_jobs':          '😕 Жаңа сәйкес вакансиялар жоқ.\n30 минуттан кейін тексеремін.',
        'paused':               '⏸ Автоіздеу тоқтатылды.',
        'resumed':              '✅ Автоіздеу жалғастырылды!',
        'already_paused':       'Автоіздеу қазірдің өзінде тоқтатылған.',
        'already_active':       'Автоіздеу қазірдің өзінде белсенді.',
        'setup_filters_first':  '⚠️ Алдымен ⚙️ Сүзгілер арқылы кілт сөздерді орнатыңыз',
        'help': (
            'ℹ️ *Ботты қалай пайдалану:*\n\n'
            '🔍 *Вакансия іздеу* — қазір іздеу\n'
            '⚙️ *Сүзгілер* — кілт сөздер, жалақы, қала, тәжірибе\n'
            '📊 *Статистика* — қанша вакансия жіберілді\n'
            '⏸ *Тоқтату* — автоматты хабарламаларды тоқтату\n'
            '▶️ *Жалғастыру* — хабарламаларды қайта қосу\n'
            '🌐 *Тіл* — интерфейс тілін өзгерту\n\n'
            '🤖 Бот жаңа вакансияларды *30 минут сайын* тексереді.\n'
            '🗂 Көздер: *HH.kz*, *Habr Career*, *RemoteOK*'
        ),
    },

    'en': {
        'choose_language': '🌐 Choose interface language:',
        'language_set': '✅ Language set: English 🇬🇧',
        'welcome': (
            '👋 *Hello!* I\'m an IT job search bot.\n\n'
            '🔎 I collect jobs from *HH.kz*, *Habr Career* and *RemoteOK*,\n'
            'filter by your criteria and send new ones every 30 minutes.\n\n'
            '👉 Press *⚙️ Filters* to set up your search.'
        ),
        'btn_search':       '🔍 Search Jobs',
        'btn_filters':      '⚙️ Filters',
        'btn_stats':        '📊 Statistics',
        'btn_pause':        '⏸ Pause',
        'btn_resume':       '▶️ Resume',
        'btn_change_lang':  '🌐 Language',
        'btn_help':         'ℹ️ Help',
        'filters_menu':         '⚙️ *Your current filters:*',
        'no_filters':           'No filters set',
        'set_keywords':         '🔑 Enter keywords separated by commas\n_(e.g.: Python, Django, Backend)_:',
        'keywords_saved':       '✅ Keywords: *{keywords}*',
        'set_salary':           '💰 Enter minimum salary in KZT\n_(or 0 for no limit)_:',
        'salary_saved':         '✅ Minimum salary: *{salary} KZT*',
        'set_city':             '🏙️ Enter city\n_(or "remote" for remote work)_:',
        'city_saved':           '✅ City: *{city}*',
        'set_experience':       '📊 Select work experience:',
        'experience_saved':     '✅ Experience: *{experience}*',
        'exp_no':               '🟢 No experience',
        'exp_1_3':              '🔵 1–3 years',
        'exp_3_6':              '🟣 3–6 years',
        'exp_6':                '🔴 More than 6 years',
        'exp_any':              '⚪️ Any',
        'set_language_filter':  '🌐 Select vacancy language:',
        'lang_ru':              '🇷🇺 Russian',
        'lang_en':              '🇬🇧 English',
        'lang_any':             '🌍 Any',
        'filters_reset':        '✅ Filters reset!',
        'sources_title':        (
            '🗂 *Job Sources*\n\n'
            'Tap a source to enable or disable it.\n'
            '✅ — active  ·  ☐ — disabled'
        ),
        'sources_saved':        '✅ Sources saved!',
        'no_sources_selected':  '⚠️ Enable at least one source!',
        'filter_sources':       'Sources',
        'btn_back_to_filters':  '← Back to filters',
        'btn_edit_keywords':    '🔑 Keywords',
        'btn_edit_salary':      '💰 Salary',
        'btn_edit_city':        '🏙️ City',
        'btn_edit_experience':  '📊 Experience',
        'btn_edit_lang':        '🌐 Vacancy language',
        'btn_search_now':       '🔍 Search now',
        'btn_reset_filters':    '🗑 Reset',
        'btn_clear_history':    '🔄 Clear history',
        'btn_sources':          '🗂 Sources',
        'btn_open_vacancy':     '🔗 Open vacancy',
        'filter_keywords':      'Keywords',
        'filter_salary':        'Min salary',
        'filter_city':          'City',
        'filter_experience':    'Experience',
        'filter_vacancy_lang':  'Vacancy language',
        'not_set':              'not set',
        'salary_not_set':       'not specified',
        'btn_back':             '← Back',
        'invalid_salary':       '❌ Please enter a number (e.g.: 200000)',
        'stats_title':          '📊 *Your statistics:*',
        'stats_total':          '📨 Total sent: *{count}* jobs',
        'stats_today':          '📅 Today: *{count}*',
        'stats_week':           '📆 Last 7 days: *{count}*',
        'stats_active':         '🤖 Auto-search: {status}',
        'stats_keywords':       '🔎 Search: _{keywords}_',
        'status_on':            'On ✅',
        'status_off':           'Off ⏸',
        'history_cleared':      '✅ History cleared! You\'ll see all vacancies again.',
        'searching':            '🔍 Searching for matching jobs...',
        'no_new_jobs':          '😕 No new matching jobs found.\nI\'ll check again in 30 minutes.',
        'paused':               '⏸ Auto-search paused.',
        'resumed':              '✅ Auto-search resumed!',
        'already_paused':       'Auto-search is already paused.',
        'already_active':       'Auto-search is already active.',
        'setup_filters_first':  '⚠️ Please set up keywords via ⚙️ Filters first',
        'help': (
            'ℹ️ *How to use the bot:*\n\n'
            '🔍 *Search Jobs* — search right now\n'
            '⚙️ *Filters* — keywords, salary, city, experience\n'
            '📊 *Statistics* — how many jobs were sent\n'
            '⏸ *Pause* — stop automatic notifications\n'
            '▶️ *Resume* — turn notifications back on\n'
            '🌐 *Language* — change interface language\n\n'
            '🤖 The bot checks for new jobs *every 30 minutes*.\n'
            '🗂 Sources: *HH.kz*, *Habr Career*, *RemoteOK*'
        ),
    }
}


def t(lang: str, key: str, **kwargs) -> str:
    lang = lang if lang in LOCALES else 'ru'
    text = LOCALES[lang].get(key, LOCALES['ru'].get(key, key))
    if kwargs:
        return text.format(**kwargs)
    return text


def _collect(key: str) -> set:
    return {LOCALES[lang][key] for lang in LOCALES if key in LOCALES[lang]}


BTN_SEARCH      = _collect('btn_search')
BTN_FILTERS     = _collect('btn_filters')
BTN_STATS       = _collect('btn_stats')
BTN_PAUSE       = _collect('btn_pause')
BTN_RESUME      = _collect('btn_resume')
BTN_CHANGE_LANG = _collect('btn_change_lang')
BTN_HELP        = _collect('btn_help')
