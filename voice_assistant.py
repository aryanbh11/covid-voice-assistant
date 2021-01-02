import pyttsx3
import speech_recognition as sr
import re
import sys
from webscraper import Scraper
# pyaudio


scraper = Scraper()

# RegEx Patterns
BASIC_PATTERNS = {
    re.compile("[\w\s]+ (cases|case)"): scraper.get_cases,
    re.compile("[\w\s]+ (cases|case) worldwide"): scraper.get_cases,
    re.compile("[\w\s]+ (deaths|death)"): scraper.get_deaths,
    re.compile("[\w\s]+ (deaths|death) worldwide"): scraper.get_deaths,
}

ACTIVE_CRITICAL_PATTERNS = {
    re.compile("[\w\s]+ active cases [\w\s]+"): lambda country: scraper.get_active_cases(country),
    re.compile("[\w\s]+ critical cases [\w\s]+"): lambda country: scraper.get_critical_cases(country),
}

REGIONAL_PATTERNS = {
    re.compile("[\w\s]+ (cases|case) [\w\s]+"): lambda country: scraper.get_cases(country),
    re.compile("(cases|case) [\w\s]+"): lambda country: scraper.get_cases(country),
    re.compile("[\w\s]+ (deaths|death|died) [\w\s]+"): lambda country: scraper.get_deaths(country),
    re.compile("(deaths|death|died) [\w\s]+"): lambda country: scraper.get_deaths(country),
    re.compile("[\w\s]+ recovered [\w\s]+"): lambda country: scraper.get_recovered(country),
    re.compile("[\w\s]+ (tests|test) [\w\s]+"): lambda country: scraper.get_tests_conducted(country),
}

UPDATE_COMMANDS = ['update', 'update date']

END_PHRASES = ['stop', 'exit']

DEFAULT_RESULT = 'Sorry, I am having trouble fetching that information'


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
            print()

    return said.lower()


def pattern_checker(text, patterns, result):
    for pattern, func in patterns.items():
        if pattern.match(text):
            words = set(text.split(" "))
            for country in scraper.get_regions():
                if country in words:
                    if result == DEFAULT_RESULT:
                        result = func(country)
                    break
    return result


def main():
    print('Started Program')

    while True:
        print("Listening...")
        text = get_audio()
        print(text)
        result = DEFAULT_RESULT

        for end_phrase in END_PHRASES:
            if end_phrase in text:
                # stop loop
                speak('Thank you!')
                sys.exit('Thank you!')

        result = pattern_checker(text, ACTIVE_CRITICAL_PATTERNS, result)
        result = pattern_checker(text, REGIONAL_PATTERNS, result)

        for pattern, func in BASIC_PATTERNS.items():
            if pattern.match(text):
                if result == DEFAULT_RESULT:
                    result = func()
                break

        for update_command in UPDATE_COMMANDS:
            if update_command in text:
                if result == DEFAULT_RESULT:
                    result = "Data is being updated. This may take a moment!"
                scraper.update_data()
                break

        print(result)
        speak(result)


main()
