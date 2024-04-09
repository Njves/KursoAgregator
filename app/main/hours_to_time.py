def format_time(hours):
    # Конвертация часов в дни, часы и минуты
    days, remainder = divmod(hours, 24)
    months, days = divmod(days, 30)
    weeks, days = divmod(days, 7)

    suffixes = {
        'month': ['месяц', 'месяца', 'месяцев'],
        'week': ['неделя', 'недели', 'недель'],
        'day': ['день', 'дня', 'дней'],
        'hour': ['час', 'часа', 'часов']
    }

    # Формируем части времени с учетом правильных окончаний
    time_parts = []
    if months > 0:
        time_parts.append(f"{months} {suffixes['month'][get_word(months)]}")
    if weeks > 0:
        time_parts.append(f"{weeks} {suffixes['week'][get_word(weeks)]}")
    if days > 0:
        time_parts.append(f"{days} {suffixes['day'][get_word(days)]}")
    if remainder > 0:
        time_parts.append(f"{remainder} {suffixes['hour'][get_word(remainder)]}")

    # Собираем все части времени в одну строку
    time_string = ', '.join(time_parts)
    return time_string
    
def get_word(n):
    if n % 10 == 1 and n % 100 != 11:
        return 0
    elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
        return 1
    else:
        return 2
