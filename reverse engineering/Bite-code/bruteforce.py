#!/usr/bin/env python3
import threading


def get_result(num):
    # Algorithm from bitecode
    var0 = num
    const0 = 3
    var1 = var0 << 3
    const1 = 5250245
    var2 = var0 ^ const1
    var3 = var2 ^ var1
    true_result = -889275714
    if var3 == true_result:
        return 1
    return 0


def bruteforce(start, stop, step):
    # Thread function to bruteforce from start to stop with step
    print(start, stop, step)
    for i in range(start, stop, step):
        if get_result(i):
            print('FOUND!!!')
            break


def start_all():
    stop = 1000000000
    # Step in thread function
    step_in = 1
    step = stop//4 - step_in
    threads = []
    for start in range(0, stop - step, step):
        # Create thread
        thread = threading.Thread(target=bruteforce, args=(start, start+step, step_in))
        threads.append(thread)
        thread.start()

    # Wait for end of the threads
    for thread in threads:
        thread.join()


start_all()
