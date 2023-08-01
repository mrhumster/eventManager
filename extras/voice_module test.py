import pyttsx3

# init function to get an engine instance for the speech synthesis
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# выбираем русский голос
rus_voices = []


for v in voices:
    if v.name == 'russian':
        rus_voices.append(v)


engine.setProperty('voice', voices[0])

# say method on the engine that passing input text to be spoken
engine.say('Приветствую! Владимир Сергеевич')

# run and wait method, it proces
engine.runAndWait()

