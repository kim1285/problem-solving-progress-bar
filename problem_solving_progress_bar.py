import time
import keyboard
from tqdm import tqdm

total_count = int(input("How many practice problems to solve?"))
set_number = int(input("Break down the process into how many sessions?"))


if total_count % set_number == 0:
    pbar_count = int(total_count / set_number)

    for i in range(set_number):
        with tqdm(total=pbar_count) as pbar:
            for j in range(pbar_count):
                while True:
                    if keyboard.is_pressed('q') and keyboard.is_pressed('shift'): # press shift + q to increase count.
                        time.sleep(0.5)
                        break
                pbar.set_description(f"Lin alg practice problems: {i + 1}/{set_number}")
                pbar.update(1)
        time.sleep(0.5)

    print("process done! Good job!")
    tmp = input("Press any key to exit...")

else:
    pbar_count = int(total_count // set_number)
    final_set_num = int(total_count % set_number)

    for i in range(set_number):
        with tqdm(total=pbar_count) as pbar:
            for j in range(pbar_count):
                while True:
                    if keyboard.is_pressed('q') and keyboard.is_pressed('shift'):
                        time.sleep(0.5)
                        break
                pbar.set_description(f"Lin alg practice problems: {i+1}/{set_number + 1}")
                pbar.update(1)
        time.sleep(0.5)

    with tqdm(total=final_set_num) as pbar:
        for k in range(final_set_num):
            while True:
                if keyboard.is_pressed('q'):
                    time.sleep(0.1)
                    break
            pbar.set_description(f"Lin alg practice problems: {k + set_number}/{set_number + 1}")
            pbar.update(1)



print("process done! Good job!")
my_exit = input("Press any key to exit...")

