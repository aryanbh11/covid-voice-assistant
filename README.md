# covid-voice-assistant
A Voice Assistant in python which scrapes the web using BeautifulSoup to answer user's questions related to COVID-19. Website being scraped for data: www.worldometers.info/coronavirus/#countries

## How to run?
### Packages Required:
The following python packages need to be installed on your machine/environment in order to run the program:
- beautifulsoup4
- requests
- lxml
- pyttsx3
- SpeechRecognition
- pyaudio

All the above mentioned packages can be simply installed by `pip install <package_name>` where package names are case sensitive. However, to install pyaudio on OSX you first need to install homebrew and then run `brew install portaudio` before the `pip` command.

### Running:
Once all packages are installed, from project directory: `python3 voice_assistant.py`

## How to use?
When the program is started, `Listening...` will be printed on the console once the assistant has fetched the data and is ready to answer questions. The user should start speaking only once `Listening...` is displayed (preferebly after a slight pause because some delay is possible). The program will print what the user spoke and the assistant's answer on the console. Once the assistant answers a question, it will recalibrate after which `Listening...` will be displayed again which is when the user can ask another question. 

### Sample Questions:
- How many COVID cases are there worldwide?
- How many people have died because of coronavirus in India?
- How many people have recovered from COVID in the UK?
- How many COVID deaths have been conducted in Australia?
- How many active cases are there in the USA?
- How many cases are critical in France? 

### Special Phrases:
- To end the program say 'stop' or 'exit'
- To update the data while program is running, say 'update' or 'update data'

## Extension Plans
- Implement GUI with a **speak** button which the user can press to talk
- Add feature to locate nearest COVID Clinic to user 
