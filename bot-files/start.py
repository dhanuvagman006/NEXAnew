import multiprocessing
from eyeroll import run_eye_animation
import speak
from capture import start_cam,get_base64
from main import core_Ai

def func1():
     run_eye_animation()

def func2():
    start_cam()

def func3():
    print("Done")
    while True:
        voice_text=speak.voice_to_text()
        if voice_text:
            response=core_Ai(voice_text,get_base64)
            #speak.speech_play(response)
        
if __name__ == '__main__':
    p1 = multiprocessing.Process(target=func1)
    p2 = multiprocessing.Process(target=func2)
    p3=multiprocessing.Process(target=func3)

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()