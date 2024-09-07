import ocr.OCR as OCR
import sentimentanalysis.SentimentAnalysis as SentimentAnalysis
import tts.TTS as TTS
from playsound import playsound
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--device", help="Devices: CPU, NPU and GPU")
parser.add_argument("-g", "--game", help="Game: Pokemon, or LOL")
args = parser.parse_args()

if args.game == "Pokemon":
    USE_OCR = True
else: 
    USE_OCR = False

######## SETTINGS ##############
#0: Device [cpu, npu, gpu] Need to add GPU support 
#1: Quantization [True/False] Need to add different quantizations (doesn't work for now so just specify device)
if args.device == "CPU":
    settings = ['cpu']
elif args.device == "NPU":
    settings = ['npu']
elif args.device == "GPU":
    settings = ['gpu']

def leagueTextLineExtractor(line):
    # Specific characters
    ch1 = "("
    ch2 = ")"
    index_1 = line.find(ch1)
    if index_1 != -1:
        index_2 = line.find(ch2, index_1)

    if index_1 != -1 and index_2 != -1:
        # Get the substring between specific characters
        character = line[index_1 + 1 :index_2]
        message = line[line.find(":") + 1:]
    else:
        print("Not player champion text")
    
    return character, message


def read_file():
    with open("C:/Users/prith/AppData/Local/vegi_chat.txt", "r") as f:
        SMRF1 = f.readlines()
    return SMRF1

# Other option is input for Overwolf

if USE_OCR:
    game_capture = OCR(50, 930, 1000, 190, settings)
else:
    initial = read_file()

text_analysis = SentimentAnalysis(settings)
speaker = TTS(settings)
audio_file_path = './temp/dialogue_capture.wav'

if USE_OCR:
    while True:
        input("Press Enter to continue...")
        dialogue = game_capture.run()
        #dialogue = ["Testing one, two, three."]
        print(dialogue)
        emotion = text_analysis.run(dialogue[0])
        speaker.run(dialogue[0], audio_file_path)
        playsound(audio_file_path)

else:
    while True:
        current = read_file()
        if initial != current:
            for line in current:
                if line not in initial:
                    character, message = leagueTextLineExtractor(line)
                    print(character)
                    print(message)
                    emotion = text_analysis.run(message)
                    speaker.run(message, audio_file_path)
                    playsound(audio_file_path)
            initial = current