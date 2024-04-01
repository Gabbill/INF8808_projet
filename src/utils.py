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
La fonction suivante va permettre de traduire les mois de la variable 'date' en français 
pour une meilleur lecture et lisibilité
'''


def translate_date(date_string):
    for eng_month, fr_month in MONTH_NAMES.items():
        if eng_month in date_string:
            return date_string.replace(eng_month, fr_month)
    return date_string
