from enum import Enum

class LocationType(Enum):
    COUNTRY = 'COUNTRY'
    STATE = 'STATE'
    CITY = 'CITY'

    @classmethod
    def choices(cls):
        return [(tag.value, tag.name) for tag in cls]


class LanguageCode(Enum):
    ENGLISH = 'en'
    FRENCH = 'fr'
    SPANISH = 'es'
    GERMAN = 'de'
    ITALIAN = 'it'
    PORTUGUESE = 'pt'
    CHINESE = 'zh'
    ARABIC = 'ar'
    JAPANESE = 'ja'
    RUSSIAN = 'ru'
    BENGALI = 'bn'
    HINDI = 'hi'
    URDU = 'ur'
    KOREAN = 'ko'
    TURKISH = 'tr'
    POLISH = 'pl'
    DUTCH = 'nl'
    SWEDISH = 'sv'
    GREEK = 'el'
    ROMANIAN = 'ro'
    DANISH = 'da'
    FINNISH = 'fi'
    CZECH = 'cs'
    HUNGARIAN = 'hu'
    BULGARIAN = 'bg'
    SLOVAK = 'sk'
    SLOVENIAN = 'sl'
    CROATIAN = 'hr'
    SERBIAN = 'sr'
    BOSNIAN = 'bs'
    MACEDONIAN = 'mk'
    LATVIAN = 'lv'
    LITHUANIAN = 'lt'
    ESTONIAN = 'et'
    UKRAINIAN = 'uk'
    BELARUSIAN = 'be'
    GEORGIAN = 'ka'
    ARMENIAN = 'hy'
    PERSIAN = 'fa'
    THAI = 'th'
    VIETNAMESE = 'vi'
    MALAY = 'ms'
    INDONESIAN = 'id'
    TAGALOG = 'tl'
    FILIPINO = 'tl'
    SWAHILI = 'sw'
    ZULU = 'zu'
    AMHARIC = 'am'
    SOMALI = 'so'
    TAMIL = 'ta'
    TELUGU = 'te'
    KANNADA = 'kn'
    MALAYALAM = 'ml'
    SINHALESE = 'si'
    BURMESE = 'my'
    LAO = 'lo'
    KHMERS = 'km'
    TIBETAN = 'bo'
    NEPALI = 'ne'
    ICELANDIC = 'is'
    NORWEGIAN = 'no'
    HEBREW = 'he'
    YIDDISH = 'yi'

    @classmethod
    def choices(cls):
        return [(tag.value, tag.name) for tag in cls]