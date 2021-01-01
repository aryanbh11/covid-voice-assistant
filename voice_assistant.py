import pyttsx3
import speech_recognition as sr
import re
import sys
from webscraper import Scraper
# pyaudio


scraper = Scraper()

# RegEx Patterns
BASIC_PATTERNS = {
    re.compile("how many [\w\s]+ (cases|case)"): scraper.get_cases,
    re.compile("how many [\w\s]+ (cases|case) worldwide"): scraper.get_cases,
    re.compile("how many [\w\s]+ (deaths|death|died)"): scraper.get_deaths,
    re.compile("how many [\w\s]+ (deaths|death|died) worldwide"): scraper.get_deaths,
}

REGIONAL_PATTERNS = {
    re.compile("[\w\s]+ (cases|case) [\w\s]+"): lambda country: scraper.get_cases(country),
    re.compile("[\w\s]+ (deaths|death|died) [\w\s]+"): lambda country: scraper.get_deaths(country),
    re.compile("[\w\s]+ recovered [\w\s]+"): lambda country: scraper.get_recovered(country),
    re.compile("[\w\s]+ (tests|test) [\w\s]+ conducted [\w\s]+"): lambda country: scraper.get_tests_conducted(country),
}

ACTIVE_CRITICAL_PATTERNS = {
    re.compile("[\w\s]+ actives (cases|case) [\w\s]+"): lambda country: scraper.get_active_cases(country),
    re.compile("[\w\s]+ critical (cases|case) [\w\s]+"): lambda country: scraper.get_critical_cases(country),
}

UPDATE_COMMANDS = ['update', 'update date']

END_PHRASES = ['stop', 'exit']


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ''

        try:
            said = r.recognize_google(audio)

        except Exception as e:
            print("Exception: ", str(e))

    return said.lower()


def main():
    print('Started Program')

    while True:
        print("Listening...")
        text = get_audio()
        print(text)
        result = None

        for pattern, func in BASIC_PATTERNS.items():
            if pattern.match(text):
                result = func()
                break

        for pattern, func in ACTIVE_CRITICAL_PATTERNS.items():
            if pattern.match(text):
                words = set(text.split(" "))
                for country in scraper.get_regions():
                    if country in words:
                        result = func(country)
                        break

        for pattern, func in REGIONAL_PATTERNS.items():
            if pattern.match(text):
                words = set(text.split(" "))
                for country in scraper.get_regions():
                    if country in words:
                        result = func(country)
                        break

        for update_command in UPDATE_COMMANDS:
            if update_command in text:
                result = "Data is being updated. This may take a moment!"
                scraper.update_data()
                break

        if result:
            print(result)
            speak(result)

        for end_phrase in END_PHRASES:
            if end_phrase in text:
                # stop loop
                speak('Thank you!')
                sys.exit('Thank you!')


main()
