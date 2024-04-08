MONTH_NAMES = {
    'January': 'janvier',
    'February': 'février',
    'March': 'mars',
    'April': 'avril',
    'May': 'mai',
    'June': 'juin',
    'July': 'juillet',
    'August': 'août',
    'September': 'septembre',
    'October': 'octobre',
    'November': 'novembre',
    'December': 'décembre'
}

'''
La fonction suivante permet de traduire les mois de la variable 'date' en français 
pour une meilleure lisibilité
'''


def translate_date(date_string):
    if date_string.startswith('0'):
        date_string = date_string[1:]
        if date_string.startswith('1'):
            date_string = date_string.replace('1', '1er', 1)

    for eng_month, fr_month in MONTH_NAMES.items():
        if eng_month in date_string:
            return date_string.replace(eng_month, fr_month)
    return date_string
