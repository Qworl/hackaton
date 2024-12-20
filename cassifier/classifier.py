from transformers import pipeline

# Инициализация пайплайна для анализа тональности
classifier = pipeline("sentiment-analysis")

financial_keywords = [
    "деньги", "счет", "оплата", "комиссия", "финансы", "выплата", "транзакция",
    "перевод", "баланс", "кредит", "дебет", "платеж", "доход", "расход", "инвестиция",
    "валюта", "акция", "дивиденд", "сбережения", "накопления", "налоги", "проценты",
    "обналичивание", "контракт", "финансовый", "выручка", "бюджет", "списание",
    "пополнение", "займ", "долг", "перевод", "счет-фактура", "чек", "монеты"
]

employee_error_keywords = [
    "сотрудник", "работник", "человек", "оператор", "кассир", "операционист", "филиал",
    "персонал", "менеджер", "администратор", "инспектор", "руководитель", "управляющий",
    "сотрудница", "штат", "кадры", "команда", "подразделение",
    "партнер", "коллега", "начальник", "супервайзер", "кадровик", "консультант", "представитель",
    "работодатель", "секретарь", "служащий", "заместитель", "рекрутер"
]

tariff_disagreement_keywords = [
    "тариф", "правила", "договор", "заключение", "расторжение", "условия",
    "план", "подписка", "пакет", "пользование", "ограничение", "изменение",
    "разрешение", "регламент", "обязательства", "предоставление", "приложение",
    "контракт", "пересмотр", "дополнение", "уточнение", "законодательство",
    "пункты", "соглашение", "положения", "обновление", "изменение", "изменения"
]

technical_failure_keywords = [
    "сбой", "авария", "замедление", "проблема", "завис", "погас",
    "ошибка", "неисправность", "неполадка", "отказ", "обрыв", "нарушение",
    "неработает", "перебой", "вылет", "глюк", "подвисание", "дефект",
    "поломка", "искажение", "разрыв", "отключение", "заморозка",
    "недоступность", "неактивен", "сбой системы", "глючит", "неустойчивость", "зависание"
]

service_speed_keywords = [
    "медленно", "быстро", "оперативно", "скорость", "производительность",
    "задержка", "ускорение", "замедление", "тормозит", "эффективность",
    "мгновенно", "ожидание", "динамика", "время", "проворство", "расторопность",
    "ускоренно", "немедленно", "затянуто", "реакция", "обработка", "опаздывает",
    "быстродействие", "моментально", "затор", "ускорить", "оперативность", "скоро"
]

gratitude_keywords = [
    "спасибо", "благодарю", "признателен",
    "спасибочки", "благодарность", "признательность", "благодарствую",
    "поклон", "спасибки", "спасибища", "спасение", "ценю", "мерси"
]

# Пример данных
feedbacks = [
    {"title": "Проблема с подключением", "text": "Сегодня я не смог войти в свой аккаунт из-за технического сбоя."},
    {"title": "Предложение улучшить сервис", "text": "Было бы здорово, если бы вы добавили больше функций."},
    {"title": "Благодарность за помощь", "text": "Спасибо за быстрое решение моей проблемы."},
    {"title": "Недоволен качеством", "text": "Очень разочарован вашим сервисом."},
    {"title": "Стабильная работа", "text": "Все работает хорошо, но всегда есть куда расти."},
]


# Классификация отзывов
def classify_feedback(title: str, text: str):
    full_text = (title + " " + text).lower()
    sentiment = classifier(full_text)[0]

    # Основные категории
    if sentiment['label'] == 'NEGATIVE':
        cur_category = 'Претензия'
    elif sentiment['label'] == 'POSITIVE':
        if any(word in full_text for word in gratitude_keywords):
            cur_category = 'Благодарность'
        else:
            cur_category = 'Предложение'
    else:
        cur_category = 'Предложение'

    # Подкатегории
    cur_subcategory, cur_finance_related = None, False


    if any(word in full_text for word in financial_keywords):
        cur_finance_related = True
    if any(word in full_text for word in employee_error_keywords):
        cur_subcategory = 'Ошибка сотрудника'
    elif any(word in full_text for word in tariff_disagreement_keywords):
        cur_subcategory = 'Несогласие с тарифами'
    elif any(word in full_text for word in technical_failure_keywords):
        cur_subcategory = 'Технический сбой'
    elif any(word in full_text for word in service_speed_keywords):
        cur_subcategory = 'Скорость обслуживания'

    return cur_category, cur_subcategory, cur_finance_related


# Применение функции классификации
results = []
for feedback in feedbacks:
    category, subcategory, finance_related = classify_feedback(feedback['title'], feedback['text'])
    results.append({
        "title": feedback["title"],
        "text": feedback["text"],
        "category": category,
        "subcategory": subcategory,
        "finance_related": finance_related
    })

# Вывод результатов
for result in results:
    print(f"Title: {result['title']}\nCategory: {result['category']}\n"
          f"Subcategory: {result.get('subcategory', 'Нет')}\n"
          f"Finance Related: {'Да' if result['finance_related'] else 'Нет'}\n")
