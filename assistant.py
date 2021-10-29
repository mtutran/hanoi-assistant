import multiprocessing
import time
import pyttsx3
import speech_recognition as sr
from fuzzywuzzy import fuzz
import cv2


def read_questions():
    with open('data/Question.txt', mode='r', encoding='utf16') as fp:
        contents = fp.read()
        list_questions = contents.split('\n')
        return list_questions


def read_answers():
    with open('data/Answer.txt', mode='r', encoding='utf16') as fp:
        contents = fp.read()
        list_answers = contents.split('\n')
        return list_answers


def find_question_index(list_questions, guest_question):
    max_score = -1
    question_index = -1
    guest_question = guest_question.lower()
    for i, question in enumerate(list_questions):
        question = question.lower()
        score = fuzz.ratio(guest_question, question)
        if score > max_score:
            max_score = score
            question_index = i
    if max_score > 50:
        return question_index
    else:
        return -1


def say(text):
    global engine
    engine.say(text)
    engine.runAndWait()


is_running = False
engine = pyttsx3.init()


def communicate_with():
    global is_running
    global engine
    if is_running:
        return
    is_running = True
    # Handle
    stop_sent = ["No", "I don't", "No thanks"]
    list_questions = read_questions()
    list_answers = read_answers()
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    engine = pyttsx3.init()
    with microphone as source:
        # th = threading.Thread(target=start_prg)
        # th.start()
        say("Hi, nice to meet you!")
        recognizer.adjust_for_ambient_noise(source)
        communicate = True
        count_failed = 0
        while communicate:
            say("What do you want to know?")
            print("Listening...")
            audio = recognizer.listen(source, timeout=7, phrase_time_limit=2)
            try:
                question = recognizer.recognize_google(audio)
                print("Question: ", question)
                question_id = find_question_index(list_questions, question)
                if question_id != -1:
                    print("Answer: ", list_answers[question_id])
                    say(list_answers[question_id])
                else:
                    say("I don't know!",)
                say("Is there any other information you want to know?")
                print("Listening...")
                audio = recognizer.listen(source, timeout=7, phrase_time_limit=2)
                reply = recognizer.recognize_google(audio)
                print(reply)
                is_stop = False
                for stop in stop_sent:
                    if stop.lower() in reply:
                        is_stop = True
                print(is_stop)
                if is_stop:
                    say("Bye. Have a nice day!")
                    break
            except sr.RequestError:
                print("API Error")
                say("API Error")
                count_failed += 1
            except sr.UnknownValueError:
                print("UnknownValueError")
                say("Can you repeat?")
                count_failed += 1
            if count_failed >= 3:
                break
            time.sleep(0.1)
    is_running = False


# def start_prg():
#     hello = ["Hi", "Hello", "Hey"]
#     recognizer = sr.Recognizer()
#     global engine
#     with microphone as source:
#         recognizer.adjust_for_ambient_noise(source)
#         audio = recognizer.listen(source, timeout=3, phrase_time_limit= )
#         user = recognizer.recognize_google(audio, language='en')
#         is_hello = False
#         for hi in hello:
#             if fuzz.ratio(hello, user) > 0.6:
#                 is_hello = True
#             if is_hello:
#                 break


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, scaleFactor=1.12, minNeighbors=12, minSize=(100, 100))
        if len(faces) > 0 and (not is_running):
            is_running = True
            th = multiprocessing.Process(target=communicate_with)
            th.start()

        for x, y, w, h in faces:
            cv2.rectangle(frame, pt1=(x, y), pt2=(x + w, y + h), color=(0, 255, 0), thickness=2)
        cv2.imshow('frame', frame)
        key = cv2.waitKey(3)
        if (key & 0xFF) == ord('q'):
            if th is not None:
                th.terminate()
            break
    cv2.destroyAllWindows()
