import pyttsx3

voiceoverDir = r"D:\Python\RedditVideoGenerator\Voiceovers"


def create_voice_over(fileName, text):
    filePath = f"{voiceoverDir}/{fileName}.mp3"
    engine = pyttsx3.init()
    engine.save_to_file(text, filePath)
    engine.runAndWait()
    return filePath
