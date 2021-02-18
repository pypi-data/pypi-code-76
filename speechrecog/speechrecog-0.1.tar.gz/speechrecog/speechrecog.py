#!/usr/bin/env python
# coding: utf-8

# In[1]:


import speech_recognition as sr

r = sr.Recognizer()
m = sr.Microphone()

try:
    print("A moment of silence, please...")
    with m as source: r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    while True:
        print("Say something!")
        with m as source: audio = r.listen(source)
        print("Got it! Now to recognize it...")
        try:
            # recognize speech using Google Speech Recognition
            value = r.recognize_pocketsphinx(audio)
            from google_trans_new import google_translator  

            detector = google_translator()  
            detect_result = detector.detect(value)[0]
            #print(value)
            #print(detect_result)
            if detect_result=='en':
                pass
            if detect_result=='zh-CN':
                pass
            else:
                print("Oops! Didn't catch that")
                continue
            # we need some special handling here to correctly print unicode characters to standard output
            if str is bytes:  # this version of Python uses bytes for strings (Python 2)
                print(u"You said {}".format(value).encode("utf-8"))
            else:  # this version of Python uses unicode for strings (Python 3+)
                print("You said {}".format(value))
        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
except KeyboardInterrupt:
    pass


# In[ ]:


import google_trans_new


# In[ ]:





# In[ ]:





# In[ ]:




