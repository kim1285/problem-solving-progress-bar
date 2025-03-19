import csv
from datetime import datetime
import time
import threading
import tkinter as tk
import pygame
import os

if os.path.exists(r"C:\Users\user\Desktop\temp_game\settings\objectives.csv"):
    with open(r"C:\Users\user\Desktop\temp_game\settings\objectives.csv", "r") as file:
        reader = csv.reader(file)
        objective_list = [i for i in next(reader)]  # next() because reader is an iterator.
        print("Previous objective list identified.")
else:
    objective_list = ["linear algebra", "statistics", "history", "rest", "bathroom", "read", "programming", "AI", "exercise"]
    print("Previous objective list doesn't exist. Initializing a default list.")

print(objective_list)

time_list = [int(0)] * len(objective_list)

# Initialize dict for objective and time total
objective_dict_p = {objective: 0 for objective in objective_list}

if not os.path.exists(r"C:\Users\user\Desktop\temp_game\settings"):
    os.makedirs(r"C:\Users\user\Desktop\temp_game\settings")

state_list = ["start", "finished", "in progress"]
input_updated = threading.Event()
current_input = ""
current_time_done = ""
status_log = ""
pygame.mixer.init()
start_time = 0
end_time = 0
elapsed_time_g = 0
# objective_dict_p = {}

# Status string example:
# 2024/11/11 14:33:47 linear algebra started.
# 2024/11/11 14:33:47 linear algebra in progress.
# 2024/11/11 14:59:02 linear algebra finished.


def convert_elapsed_time_into_format_time(elapsed_time):
    elapsed_time_p = elapsed_time
    # 9999 floor division by 60 to get minutes
    a = elapsed_time // 60
    print(a)
    # ~ modulo by 60 to get leftover seconds
    b = elapsed_time % 60
    print(b)
    # a floor division by 60 to get hours
    c = a // 60
    print(c)
    # a modulo 60 to get leftover minutes
    d = a % 60
    print(d)
    # formatting should then be...
    format_time = f"{c:02}:{d:02}:{b:02}"
    return format_time


def modify_starting_time(subject, time_p):  # i of subject and time in minutes
    objective_dict_p[objective_list[int(subject)]] = int(time_p) * 60

# def remove_objective():


def add_objective():  # needs to get the list of objectives
    new_objective = input("Add the name of the objective you would like to add.")
    objective_list.append(new_objective)
    objective_dict_p[objective_list[-1]] = int(0)
    print("objective added successfully.")


def remove_objective():  # removes objective inside the list
    objective_to_remove = int(input("Enter the i of the objective you would like to remove."))
    objective_dict_p.pop(objective_list[int(objective_to_remove)])
    objective_list.pop(objective_to_remove)
    print("objective removed successfully.")


def save_data():
    try:
        with (open(rf"C:\Users\user\Desktop\temp_game\{datetime.now().strftime('%Y_%m_%d')}_log.txt", 'w')
              as file_p):
            file_p.write(str(objective_dict_p))
            print(
                rf"Time per objectives saved to C:\Users\user\Desktop\temp_game\{datetime.now().strftime('%Y_%m_%d')}_log.txt")
        with open(rf"C:\Users\user\Desktop\temp_game\settings\objectives.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(objective_list)
    except Exception as e:
        print("Error while closing and saving the log file: ", e)


def input_function():
    global current_input
    global status_log
    global start_time
    global end_time
    global elapsed_time_g
    global objective_dict_p
    # input of -1 is exit.
    while True:
        input_function_front = input('Please enter the objective and the state of your game: ')
        if input_function_front == "m":  # m - modify: modifying the total time done today of a given subjects.
            input_tmp = input("What is the objective_i and time in minutes?").split(" ")
            objective_m, time_m = input_tmp[0], input_tmp[1]
            modify_starting_time(objective_m, time_m)
            update_current_times()
            current_input = "current status of the game"
            input_updated.set()
        elif input_function_front == "s":  # s - save
            save_data()
        elif input_function_front == "a":
            add_objective()
            update_current_times()
            current_input = "current status of the game"
            input_updated.set()
        elif input_function_front == "r":
            remove_objective()
            update_current_times()
            current_input = "current status of the game"
            input_updated.set()
        else:
            # get information from the input.
            input_function_split = input_function_front.split()
            user_objective_i = int(input_function_split[0])
            user_state = int(input_function_split[1])
            time_now_short = datetime.now().strftime("%H:%M:%S")
            if user_state == 0:
                start_time = int(f"{time.time():.0f}")
                information_to_display = f"{time_now_short} - {objective_list[user_objective_i]} {state_list[2]}"
                current_input = information_to_display
                update_current_times()
                input_updated.set()
            elif user_state == 1:
                end_time = int(f"{time.time():.0f}")
                elapsed_time_g = end_time - start_time
                objective_dict_p[objective_list[user_objective_i]] += elapsed_time_g
                information_to_display = f"{time_now_short} - {objective_list[user_objective_i]} {state_list[user_state]} "
                if ((user_objective_i == int(0) or user_objective_i == int(1) or user_objective_i == int(2)
                     or user_objective_i == int(5) or user_objective_i == int(6)
                     or user_objective_i == int(7) or user_objective_i == int(8))
                        and elapsed_time_g >= 1500):
                    print("playing sounds...")
                    thread3 = threading.Thread(target=play_sound, daemon=True)
                    thread3.start()
                current_input = information_to_display
                update_current_times()
            input_updated.set()


# I have to make a new dictionary or something to display on label_2!
def update_current_times():
    global current_time_done
    current_time_done = ""
    objective_names_list = objective_list
    objective_time_list = [objective_dict_p[objective_list[i]] for i in range(len(objective_list))]
    for i in range(len(objective_list)):
        current_time_done += str(f"{i}. {objective_names_list[i]}: {int(objective_time_list[i]) // 3600}h {(int(objective_time_list[i])) % 3600 // 60}m {int(objective_time_list[i]) % 60}s\n")


def display_input():
    if input_updated.is_set():
        input_label_1.config(text=f"{current_input}")
        input_label_2.config(text=f"{current_time_done}", anchor="w", justify="left")
        input_updated.clear()
    root.after(100, display_input)


def play_sound():
    pygame.mixer.music.load(r"C:\Users\user\Desktop\temp_game\Karma_up.mp3")
    pygame.mixer.music.play()


thread1 = threading.Thread(target=input_function, daemon=True)
thread1.start()

root = tk.Tk()
root.title("Effort Game")

input_label_1 = tk.Label(root, text="current status of the game", font=("Helvetica", 25), width=60, height=2)
input_label_1.pack(pady=0)

update_current_times()

input_label_3 = tk.Label(root, text="", font=("Helvetica", 9))

input_label_2 = tk.Label(root, text=f"{current_time_done}",
                         font=("Helvetica", 9), anchor="w", justify="left")
input_label_2.pack(pady=1)




display_input()

root.mainloop()
