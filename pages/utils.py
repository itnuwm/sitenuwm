from django.utils.text import slugify

class Utils:
    @staticmethod
    def transliterate(text):
        cyrillic_to_latin = {
            u'а': 'a', u'б': 'b', u'в': 'v', u'г': 'h', u'ґ': 'g', u'д': 'd', u'е': 'e', u'є': 'ie', u'ж': 'zh',
            u'з': 'z', u'и': 'y', u'і': 'i', u'ї': 'i', u'й': 'i', u'к': 'k', u'л': 'l', u'м': 'm', u'н': 'n',
            u'о': 'o', u'п': 'p', u'р': 'r', u'с': 's', u'т': 't', u'у': 'u', u'ф': 'f', u'х': 'kh', u'ц': 'ts',
            u'ч': 'ch', u'ш': 'sh', u'щ': 'shch', u'ю': 'iu', u'я': 'ia', u'ь': '', u'’': '', u"'": '',
            u'А': 'A', u'Б': 'B', u'В': 'V', u'Г': 'H', u'Ґ': 'G', u'Д': 'D', u'Е': 'E', u'Є': 'Ye', u'Ж': 'Zh',
            u'З': 'Z', u'И': 'Y', u'І': 'I', u'Ї': 'Yi', u'Й': 'Y', u'К': 'K', u'Л': 'L', u'М': 'M', u'Н': 'N',
            u'О': 'O', u'П': 'P', u'Р': 'R', u'С': 'S', u'Т': 'T', u'У': 'U', u'Ф': 'F', u'Х': 'Kh', u'Ц': 'Ts',
            u'Ч': 'Ch', u'Ш': 'Sh', u'Щ': 'Shch', u'Ю': 'Yu', u'Я': 'Ya', u'Ь': '', u'’': '', u"'": '', u' ': ''
        }
        return ''.join(cyrillic_to_latin.get(char, char) for char in text)

    @staticmethod
    def slugify(text):
        return slugify(Utils.transliterate(text), allow_unicode=False)