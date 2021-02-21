from uvicmuse.MuseWrapper import MuseWrapper as ww
import threading
import asyncio


def repT(loop, w):
    while True:
        loop.run_until_complete(w.muse.start())
        asyncio.run(asyncio.sleep(2))


if __name__ == "__main__":
    print("Hello")
    loop = asyncio.get_event_loop()
    w = ww(loop,max_buff_len = 3)
    w.search_and_connect()

    # t1 = threading.Thread(target=repT, args=(loop,w,))
    # t1.start()
    # loop.run_until_complete(w.muse.start())

    print("First sample" + str(w.pull_eeg()))

    asyncio.run(asyncio.sleep(4))

    print("Second sample" + str(w.pull_eeg()))
    w.loop.run_until_complete(w.muse.start())
    asyncio.run(asyncio.sleep(4))

    print("Third sample" + str(w.pull_eeg()))
    asyncio.run(asyncio.sleep(4))

    w.loop.run_until_complete(w.muse.start())
    print("Fourth sample" + str(w.pull_eeg()))

    # t1.join()