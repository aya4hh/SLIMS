import tkinter as tk
from tkinter import messagebox
import time
import threading
import winsound

#data
expenses = {}
tasks = []
study_log = {}

BG_MAIN = "#fdf8ee"  #cream
BG_EXPENSE = "#fffbe6"  #light yellow
BG_TASK = "#e8f4fc"  #light blue
BG_TIMER = "#fce8f4"  #light pink

#buttons' color
COLOR_YELLOW = "#f7e04a"
COLOR_BLUE = "#74b9ff"
COLOR_PINK = "#fd79a8"
COLOR_GREEN = "#55efc4"

#text colors
COLOR_TEXT_DARK = "#2d3436"  #black
COLOR_TEXT_GRAY = "#636e72"  #medium gray
COLOR_DIVIDER = "#dfe6e9"  #light gray

FONT_TITLE = ("Courier New", 28, "bold")
FONT_HEADER = ("Courier New", 17, "bold")
FONT_NORMAL = ("Courier New", 14)
FONT_SMALL = ("Courier New", 13)
FONT_CLOCK = ("Courier New", 15)
FONT_TIMER = ("Courier New", 22, "bold")
FONT_BIG = ("Courier New", 25, "bold")


root = tk.Tk()
root.title("STUDENT INDEPENDENT LIVING MANAGEMENT SYSTEM")
root.geometry("1920x1080")
root.configure(bg=BG_MAIN)
root.resizable(True, True)

page_container = tk.Frame(root, bg=BG_MAIN)
page_container.pack(fill="both", expand=True)

page_container.grid_rowconfigure(0, weight=1)
page_container.grid_columnconfigure(0, weight=1)


all_pages = {}


def go_to_page(page_name):
    pages_to_rebuild = [
        "add_expense", "view_expenses",
        "add_task", "mark_task_done", "view_tasks",
        "start_timer", "view_study_log"
    ]

    if page_name in pages_to_rebuild:
        if page_name in all_pages:
            all_pages[page_name].destroy()

        new_page = PAGE_BUILDERS[page_name](page_container)

        new_page.grid(row=0, column=0, sticky="nsew")

        all_pages[page_name] = new_page

    all_pages[page_name].tkraise()



def make_button(parent, button_text, click_function, button_color, button_width=28):
    button = tk.Button(
        parent,
        text=button_text,
        command=click_function,
        font=FONT_NORMAL,
        bg=button_color,
        fg=COLOR_TEXT_DARK,
        relief="solid",
        bd=2,
        activebackground=button_color,
        activeforeground=COLOR_TEXT_DARK,
        cursor="circle",
        pady=10,
        padx=20,
        highlightthickness=0,
        width=button_width,
    )

    button.bind("<Enter>", lambda event: button.config(relief="groove", bd=3))
    button.bind("<Leave>", lambda event: button.config(relief="solid", bd=2))
    return button


def make_back_button(parent):

    back_button = tk.Button(
        parent,
        text="Return to Main Menu",
        font=("Courier New", 20),
        background="#FFB6C1",  #light pink
        activebackground="#CDB4DA",  #light purple
        relief="flat",
        cursor="cross",
        pady=12,
        padx=24,
        command=lambda: go_to_page("main"),
    )
    return back_button


def make_page_header(parent, icon, title_text, background_color):
    #top
    tk.Frame(parent, bg=COLOR_YELLOW, height=6).pack(fill="x")


    tk.Label(
        parent,
        text=icon + "  " + title_text,
        font=FONT_BIG,
        bg=background_color,
        fg=COLOR_TEXT_DARK
    ).pack(pady=(30, 6))

    tk.Frame(parent, bg=COLOR_DIVIDER, height=1).pack(fill="x", padx=80, pady=1)
    tk.Frame(parent, bg=COLOR_DIVIDER, height=1).pack(fill="x", padx=80, pady=1)


def make_label(parent, label_text, background_color, label_font=None, label_color=None):
    tk.Label(
        parent,
        text=label_text,
        font=label_font or FONT_SMALL,
        bg=background_color,
        fg=label_color or COLOR_TEXT_GRAY,
        anchor="w"
    ).pack(fill="x", padx=120, pady=(10, 0))


def make_entry_box(parent, background_color, placeholder_text=""):
    entry_box = tk.Entry(
        parent,
        font=FONT_NORMAL,
        bg="white",
        relief="solid",
        bd=1,
        highlightthickness=1,
        highlightbackground=COLOR_DIVIDER
    )
    entry_box.insert(0, placeholder_text)
    entry_box.pack(fill="x", padx=120, ipady=8)
    return entry_box


def show_flash_message(parent, background_color, message_text, text_color=COLOR_TEXT_DARK):
    message_label = tk.Label(
        parent,
        text=message_text,
        font=FONT_NORMAL,
        bg=background_color,
        fg=text_color
    )
    message_label.pack(pady=6)
    parent.after(2500, message_label.destroy)


def build_main_menu(parent):
  

   #mainframe
    main_frame = tk.Frame(parent, bg=BG_MAIN)

    for i in range(3):
        tk.Frame(main_frame, bg=COLOR_DIVIDER, height=1).pack(fill="x")

    title_area = tk.Frame(main_frame, bg=BG_MAIN)
    title_area.pack(pady=(40, 0))

    tk.Label(
        title_area,
        text="SILMS",
        font=("Courier New", 30, "bold"),
        bg=BG_MAIN,
        fg=COLOR_TEXT_DARK
    ).pack()

    tk.Label(
        title_area,
        text="made by a very tired student",
        font=("Courier New", 13, "italic"),
        bg=BG_MAIN,
        fg=COLOR_TEXT_GRAY
    ).pack()

    tk.Frame(main_frame, bg=COLOR_YELLOW, height=4).pack(fill="x", padx=80, pady=14)

    global clock_label
    clock_label = tk.Label(main_frame, font=FONT_CLOCK, bg=BG_MAIN, fg=COLOR_TEXT_GRAY)
    clock_label.pack()

    global timer_label
    timer_label = tk.Label(
        main_frame,
        text="no timer running",
        font=FONT_TIMER,
        fg="#6c5ce7",
        bg=BG_MAIN
    )
    timer_label.pack(pady=(14, 6))

    tk.Frame(main_frame, bg=COLOR_DIVIDER, height=1).pack(fill="x", padx=80)




    expense_section = tk.Frame(main_frame, bg=BG_EXPENSE, bd=1, relief="solid")
    expense_section.pack(fill="x", padx=80, pady=14)

    tk.Frame(expense_section, bg=COLOR_YELLOW, height=6).pack(fill="x")
    tk.Label(expense_section, text="💰  Broke Check", font=FONT_HEADER, bg=BG_EXPENSE, fg=COLOR_TEXT_DARK,
             anchor="w").pack(fill="x", padx=20, pady=(12, 6))
    tk.Frame(expense_section, bg=COLOR_DIVIDER, height=1).pack(fill="x", padx=20)

    expense_buttons = tk.Frame(expense_section, bg=BG_EXPENSE)
    expense_buttons.pack(pady=16, padx=16)

    make_button(expense_buttons, "log an expense", lambda: go_to_page("add_expense"), COLOR_YELLOW).pack(side="left",
                                                                                                         padx=12)
    make_button(expense_buttons, "view expenses", lambda: go_to_page("view_expenses"), "#ffeaa7").pack(side="left",
                                                                                                       padx=12)



    task_section = tk.Frame(main_frame, bg=BG_TASK, bd=1, relief="solid")
    task_section.pack(fill="x", padx=80, pady=14)

    tk.Frame(task_section, bg=COLOR_YELLOW, height=6).pack(fill="x")
    tk.Label(task_section, text="🧹  Grind Mode On", font=FONT_HEADER, bg=BG_TASK, fg=COLOR_TEXT_DARK, anchor="w").pack(
        fill="x", padx=20, pady=(12, 6))
    tk.Frame(task_section, bg=COLOR_DIVIDER, height=1).pack(fill="x", padx=20)

    task_buttons = tk.Frame(task_section, bg=BG_TASK)
    task_buttons.pack(pady=16, padx=16)

    make_button(task_buttons, "add a task", lambda: go_to_page("add_task"), COLOR_BLUE).pack(side="left", padx=10)
    make_button(task_buttons, "mark task done", lambda: go_to_page("mark_task_done"), "#a29bfe").pack(side="left",
                                                                                                      padx=10)
    make_button(task_buttons, "view all tasks", lambda: go_to_page("view_tasks"), "#74b9ff").pack(side="left", padx=10)




    timer_section = tk.Frame(main_frame, bg=BG_TIMER, bd=1, relief="solid")
    timer_section.pack(fill="x", padx=80, pady=14)

    tk.Frame(timer_section, bg=COLOR_YELLOW, height=6).pack(fill="x")
    tk.Label(timer_section, text="⏱  Lock In", font=FONT_HEADER, bg=BG_TIMER, fg=COLOR_TEXT_DARK, anchor="w").pack(
        fill="x", padx=20, pady=(12, 6))
    tk.Frame(timer_section, bg=COLOR_DIVIDER, height=1).pack(fill="x", padx=20)

    timer_buttons = tk.Frame(timer_section, bg=BG_TIMER)
    timer_buttons.pack(pady=16, padx=16)

    make_button(timer_buttons, "start study timer", lambda: go_to_page("start_timer"), COLOR_PINK).pack(side="left",
                                                                                                        padx=12)
    make_button(timer_buttons, "study log", lambda: go_to_page("view_study_log"), "#fab1d3").pack(side="left", padx=12)

    #feet
    tk.Frame(main_frame, bg=COLOR_DIVIDER, height=1).pack(fill="x", padx=80, pady=(10, 0))

    footer_area = tk.Frame(main_frame, bg=BG_MAIN)
    footer_area.pack(pady=30)

    tk.Label(
        footer_area,
        text="goodluck out there bestie  ✨",
        font=("Courier New", 13, "italic"),
        bg=BG_MAIN,
        fg=COLOR_TEXT_GRAY
    ).pack(pady=(0, 10))

    make_button(footer_area, "exit", root.destroy, "#dfe6e9").pack()

    return main_frame




def build_add_expense(parent):

    page_frame = tk.Frame(parent, bg=BG_EXPENSE)
    make_page_header(page_frame, "💸", "Add Expense", BG_EXPENSE)

    # Input fields
    make_label(page_frame, "what did you spend on?", BG_EXPENSE)
    category_input = make_entry_box(page_frame, BG_EXPENSE)

    make_label(page_frame, "how much (₱):", BG_EXPENSE)
    amount_input = make_entry_box(page_frame, BG_EXPENSE)


    message_area = tk.Frame(page_frame, bg=BG_EXPENSE)
    message_area.pack(pady=4)

    def add_expense_clicked():



        category = category_input.get().strip()
        amount_text = amount_input.get().strip()


        if category == "":
            show_flash_message(message_area, BG_EXPENSE, "category can't be empty!", "#e17055")
            return


        try:
            amount = float(amount_text)
        except ValueError:
            show_flash_message(message_area, BG_EXPENSE, "please enter a valid number!", "#e17055")
            return


        if amount <= 0:
            show_flash_message(message_area, BG_EXPENSE, "amount must be greater than zero!", "#e17055")
            return


        if category in expenses:
            expenses[category] = expenses[category] + amount
        else:
            expenses[category] = amount


        show_flash_message(message_area, BG_EXPENSE, "added ₱" + str(amount) + " to '" + category + "'", "#00b894")


        category_input.delete(0, "end")
        amount_input.delete(0, "end")

    button_row = tk.Frame(page_frame, bg=BG_EXPENSE)
    button_row.pack(pady=20)
    make_button(button_row, "add expense", add_expense_clicked, COLOR_YELLOW).pack(side="left", padx=10)

    make_back_button(page_frame).pack(pady=40)
    return page_frame



def build_view_expenses(parent):

    page_frame = tk.Frame(parent, bg=BG_EXPENSE)
    make_page_header(page_frame, "📊", "Expenses", BG_EXPENSE)

    content_area = tk.Frame(page_frame, bg=BG_EXPENSE)
    content_area.pack(padx=120, fill="both", expand=True, pady=10)

    if len(expenses) == 0:
        tk.Label(content_area, text="no expenses yet...", font=FONT_NORMAL, bg=BG_EXPENSE, fg=COLOR_TEXT_GRAY).pack(
            pady=30)
    else:
        canvas = tk.Canvas(content_area, bg=BG_EXPENSE, highlightthickness=0)
        scrollbar = tk.Scrollbar(content_area, orient="vertical", command=canvas.yview)
        inner_frame = tk.Frame(canvas, bg=BG_EXPENSE)


        inner_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


        total_spent = 0
        for category_name, amount_spent in expenses.items():

            row = tk.Frame(inner_frame, bg=BG_EXPENSE)
            row.pack(fill="x", pady=5)

            tk.Label(row, text="• " + category_name, font=FONT_NORMAL, bg=BG_EXPENSE, fg=COLOR_TEXT_DARK,
                     anchor="w").pack(side="left")
            tk.Label(row, text="₱" + str(round(amount_spent, 2)), font=("Courier New", 14, "bold"), bg=BG_EXPENSE,
                     fg="#e17055", anchor="e").pack(side="right")


            tk.Frame(inner_frame, bg=COLOR_DIVIDER, height=1).pack(fill="x")

            total_spent = total_spent + amount_spent


        tk.Frame(content_area, bg=COLOR_TEXT_GRAY, height=2).pack(fill="x", pady=8)
        total_row = tk.Frame(content_area, bg=BG_EXPENSE)
        total_row.pack(fill="x")
        tk.Label(total_row, text="total:", font=("Courier New", 16, "bold"), bg=BG_EXPENSE).pack(side="left")
        tk.Label(total_row, text="₱" + str(round(total_spent, 2)), font=("Courier New", 16, "bold"), bg=BG_EXPENSE,
                 fg="#e17055").pack(side="right")

    make_back_button(page_frame).pack(pady=40)
    return page_frame




def build_add_task(parent):

    page_frame = tk.Frame(parent, bg=BG_TASK)
    make_page_header(page_frame, "✏️", "Add Task", BG_TASK)

    make_label(page_frame, "what do you need to do:", BG_TASK)
    task_input = make_entry_box(page_frame, BG_TASK)

    make_label(page_frame, "task type:", BG_TASK)

    task_type = tk.StringVar()
    task_type.set("study")

    radio_area = tk.Frame(page_frame, bg=BG_TASK)
    radio_area.pack(padx=120, anchor="w", pady=6)

    tk.Radiobutton(radio_area, text="study", variable=task_type, value="study", font=FONT_NORMAL, bg=BG_TASK,
                   activebackground=BG_TASK, selectcolor="white").pack(side="left", padx=14)
    tk.Radiobutton(radio_area, text="chores", variable=task_type, value="chores", font=FONT_NORMAL, bg=BG_TASK,
                   activebackground=BG_TASK, selectcolor="white").pack(side="left", padx=14)

    message_area = tk.Frame(page_frame, bg=BG_TASK)
    message_area.pack(pady=4)

    def add_task_clicked():
        task_text = task_input.get().strip()

        if task_text == "":
            show_flash_message(message_area, BG_TASK, "you forgot to type a task!", "#e17055")
            return

        new_task = {
            "task": task_text,
            "type": task_type.get(),
            "done": False
        }
        tasks.append(new_task)

        show_flash_message(message_area, BG_TASK, "task added!", "#00b894")
        task_input.delete(0, "end")

    make_button(page_frame, "add task", add_task_clicked, COLOR_BLUE).pack(pady=20)
    make_back_button(page_frame).pack(pady=40)
    return page_frame



def build_mark_task_done(parent):

    page_frame = tk.Frame(parent, bg=BG_TASK)
    make_page_header(page_frame, "✅", "Mark Task Done", BG_TASK)

    if len(tasks) == 0:
        tk.Label(page_frame, text="no tasks yet! go add some.", font=FONT_NORMAL, bg=BG_TASK, fg=COLOR_TEXT_GRAY).pack(
            pady=30)
        make_back_button(page_frame).pack(pady=40)
        return page_frame

    selected_index = tk.IntVar()
    selected_index.set(-1)


    outer_frame = tk.Frame(page_frame, bg=BG_TASK)
    outer_frame.pack(padx=120, fill="both", expand=True, pady=10)

    canvas = tk.Canvas(outer_frame, bg=BG_TASK, highlightthickness=0)
    scrollbar = tk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
    inner_frame = tk.Frame(canvas, bg=BG_TASK)
    inner_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for i in range(len(tasks)):
        current_task = tasks[i]
        is_done = current_task["done"]

        if is_done:
            icon = "✅"
            button_state = "disabled"
        else:
            icon = "⬜"
            button_state = "normal"

        label_text = icon + "  " + current_task["task"] + "  [" + current_task["type"] + "]"

        tk.Radiobutton(
            inner_frame,
            text=label_text,
            variable=selected_index,
            value=i,
            font=FONT_NORMAL,
            bg=BG_TASK,
            state=button_state,
            activebackground=BG_TASK,
            selectcolor="white",
            anchor="w"
        ).pack(fill="x", padx=10, pady=5)

    message_area = tk.Frame(page_frame, bg=BG_TASK)
    message_area.pack(pady=4)

    def mark_done_clicked():
        idx = selected_index.get()

        if idx == -1:
            show_flash_message(message_area, BG_TASK, "please pick a task first!", "#e17055")
            return


        tasks[idx]["done"] = True
        show_flash_message(message_area, BG_TASK, "task marked as done! great job!", "#00b894")

    make_button(page_frame, "mark done", mark_done_clicked, COLOR_BLUE).pack(pady=16)
    make_back_button(page_frame).pack(pady=40)
    return page_frame



def build_view_tasks(parent):
    """Page that shows all tasks with their status."""

    page_frame = tk.Frame(parent, bg=BG_TASK)
    make_page_header(page_frame, "📋", "Task List", BG_TASK)

    content_area = tk.Frame(page_frame, bg=BG_TASK)
    content_area.pack(padx=120, fill="both", expand=True, pady=10)

    if len(tasks) == 0:
        tk.Label(content_area, text="nothing here yet!", font=FONT_NORMAL, bg=BG_TASK, fg=COLOR_TEXT_GRAY).pack(pady=30)
    else:
        canvas = tk.Canvas(content_area, bg=BG_TASK, highlightthickness=0)
        scrollbar = tk.Scrollbar(content_area, orient="vertical", command=canvas.yview)
        inner_frame = tk.Frame(canvas, bg=BG_TASK)
        inner_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for task_item in tasks:
            is_done = task_item["done"]

            if is_done:
                icon = "✅"
                text_color = "#00b894"
            else:
                icon = "⬜"
                text_color = "#d63031"

            row = tk.Frame(inner_frame, bg=BG_TASK)
            row.pack(fill="x", pady=5, padx=6)

            tk.Label(row, text=icon, bg=BG_TASK, font=("Courier New", 14)).pack(side="left")
            tk.Label(row, text="  " + task_item["task"] + "  [" + task_item["type"] + "]",
                     font=FONT_NORMAL, bg=BG_TASK, fg=text_color, anchor="w").pack(side="left")

            tk.Frame(inner_frame, bg=COLOR_DIVIDER, height=1).pack(fill="x", padx=6)

    make_back_button(page_frame).pack(pady=40)
    return page_frame


def build_start_timer(parent):


    page_frame = tk.Frame(parent, bg=BG_TIMER)
    make_page_header(page_frame, "⏱", "Start Timer", BG_TIMER)

    make_label(page_frame, "what subject are you studying:", BG_TIMER)
    subject_input = make_entry_box(page_frame, BG_TIMER)

    make_label(page_frame, "how long will you study (minutes):", BG_TIMER)
    study_time_input = make_entry_box(page_frame, BG_TIMER)

    make_label(page_frame, "break time after (minutes, 0 = no break):", BG_TIMER)
    break_time_input = make_entry_box(page_frame, BG_TIMER, placeholder_text="0")

    message_area = tk.Frame(page_frame, bg=BG_TIMER)
    message_area.pack(pady=4)

    def start_timer_clicked():
        subject = subject_input.get().strip()

        if subject == "":
            show_flash_message(message_area, BG_TIMER, "please enter a subject!", "#e17055")
            return

        try:
            study_minutes = int(study_time_input.get().strip())
            break_minutes = int(break_time_input.get().strip())
        except ValueError:
            show_flash_message(message_area, BG_TIMER, "please enter valid whole numbers!", "#e17055")
            return

        if study_minutes <= 0 or break_minutes < 0:
            show_flash_message(message_area, BG_TIMER, "study time must be at least 1 minute!", "#e17055")
            return

        subject = subject.title()

        timer_label.config(text="timer starting... lock in!")

        timer_thread = threading.Thread(
            target=run_timer,
            args=(subject, study_minutes, break_minutes),
            daemon=True
        )
        timer_thread.start()

        show_flash_message(message_area, BG_TIMER, "timer started for " + subject + "! go go go!", "#00b894")

    make_button(page_frame, "start timer", start_timer_clicked, COLOR_PINK).pack(pady=20)
    make_back_button(page_frame).pack(pady=40)
    return page_frame



def build_view_study_log(parent):

    page_frame = tk.Frame(parent, bg=BG_TIMER)
    make_page_header(page_frame, "📓", "Study Log", BG_TIMER)

    content_area = tk.Frame(page_frame, bg=BG_TIMER)
    content_area.pack(padx=120, fill="both", expand=True, pady=10)

    if len(study_log) == 0:
        tk.Label(content_area, text="you haven't studied anything yet!", font=FONT_NORMAL, bg=BG_TIMER,
                 fg=COLOR_TEXT_GRAY).pack(pady=30)
    else:
        total_minutes = 0

        for subject_name, minutes_studied in study_log.items():
            row = tk.Frame(content_area, bg=BG_TIMER)
            row.pack(fill="x", pady=5)

            tk.Label(row, text="• " + subject_name, font=FONT_NORMAL, bg=BG_TIMER, fg=COLOR_TEXT_DARK, anchor="w").pack(
                side="left")
            tk.Label(row, text=str(minutes_studied) + " min", font=("Courier New", 14, "bold"), bg=BG_TIMER,
                     fg="#6c5ce7", anchor="e").pack(side="right")

            tk.Frame(content_area, bg=COLOR_DIVIDER, height=1).pack(fill="x")

            total_minutes = total_minutes + minutes_studied

        tk.Frame(content_area, bg=COLOR_TEXT_GRAY, height=2).pack(fill="x", pady=8)
        total_row = tk.Frame(content_area, bg=BG_TIMER)
        total_row.pack(fill="x")
        tk.Label(total_row, text="total study time:", font=("Courier New", 16, "bold"), bg=BG_TIMER).pack(side="left")
        tk.Label(total_row, text=str(total_minutes) + " min", font=("Courier New", 16, "bold"), bg=BG_TIMER,
                 fg="#6c5ce7").pack(side="right")

    make_back_button(page_frame).pack(pady=40)
    return page_frame



def run_timer(subject, study_minutes, break_minutes):

    total_seconds = study_minutes * 60

    while total_seconds > 0:

        minutes_left = total_seconds // 60
        seconds_left = total_seconds % 60

        time_display = "studying: " + str(minutes_left).zfill(2) + ":" + str(seconds_left).zfill(2)
        timer_label.config(text=time_display)

        time.sleep(1)
        total_seconds = total_seconds - 1


    winsound.Beep(1200, 400)
    winsound.Beep(1200, 400)


    if subject in study_log:
        study_log[subject] = study_log[subject] + study_minutes
    else:
        study_log[subject] = study_minutes


    if break_minutes > 0:
        total_seconds = break_minutes * 60

        while total_seconds > 0:
            minutes_left = total_seconds // 60
            seconds_left = total_seconds % 60

            time_display = "break time: " + str(minutes_left).zfill(2) + ":" + str(seconds_left).zfill(2)
            timer_label.config(text=time_display)

            time.sleep(1)
            total_seconds = total_seconds - 1


        winsound.Beep(800, 400)
        winsound.Beep(800, 400)


    timer_label.config(text="timer done!! great job!")


def update_clock():

    current_time = time.strftime("%I:%M:%S %p")
    current_date = time.strftime("%A, %B %d")

    clock_label.config(text=current_date + "   " + current_time)

    root.after(1000, update_clock)



PAGE_BUILDERS = {
    "add_expense": build_add_expense,
    "view_expenses": build_view_expenses,
    "add_task": build_add_task,
    "mark_task_done": build_mark_task_done,
    "view_tasks": build_view_tasks,
    "start_timer": build_start_timer,
    "view_study_log": build_view_study_log,
}

clock_label = None
timer_label = None

main_page = build_main_menu(page_container)
main_page.grid(row=0, column=0, sticky="nsew")
all_pages["main"] = main_page

update_clock()

root.mainloop()