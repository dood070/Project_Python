import sys
import time

def jalanin_lirik():
    lirik = [
        ("It was in a blink of an eye", 0.07),
        ("Find a way how to say goodbye", 0.07),
        ("I've got to take me away", 0.07),
        ("from all sadness", 0.08),
        ("Stitch all my wounds", 0.07),
        ("confess all the sins", 0.06),
        ("And took all my insecure", 0.08),
        ("When will I got the love", 0.08),
        ("that is so pure?", 0.08),
        ("Gotta have to always make sure?", 0.07),
        ("That I'm not just somebody's pleasure", 0.08),
    ]

    delay = [1.0, 1.0, 1.0, 2.5, 1.0, 0.5, 1.0, 1.0, 2.5, 0.5, 1.0, 1.0]
    for i, (baris_lagu, delay_karakter) in enumerate(lirik):
        for karakter in baris_lagu:
            print(karakter, end='')
            sys.stdout.flush()
            time.sleep(delay_karakter)
        time.sleep(delay[i])
        print('')
    print("// Code by DHOO")
 
jalanin_lirik()
