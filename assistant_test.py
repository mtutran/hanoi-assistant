from gtts import gTTS
from playsound import playsound
import time


def read_file(file_path):
    with open(file_path, mode='r', encoding='utf16') as fp:
        contents = fp.read()
        list_answers = contents.split('\n')
        return list_answers


def cvt_text_to_speech(text, lang='vi', out_file='tmp_mp3'):
    obj = gTTS(text, lang=lang)
    obj.save(out_file)


def run_audio(file_path):
    playsound(file_path)


if __name__ == '__main__':
    answers = read_file('data/Answer.txt')
    for i, answer in enumerate(answers):
        print(answer)
        cvt_text_to_speech(answer, lang='en', out_file=f'audio/answer_{i}.mp3')
        cvt_text_to_speech("Hanoi has a bundle of places to visit Hanoi Old Town Quarter, Hoan Kiem Lake, Temple of Literature.op")
