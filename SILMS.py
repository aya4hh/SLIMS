import tkinter as tk
from tkinter import messagebox
import time
import threading
import winsound

#current background for main menu
current_bg = "#fdf8ee"

#lists
expenses = {}
tasks = []
study_log = {}

#main menu
root = tk.Tk()
root.title("STUDENT INDEPENDENT LIVING MANAGEMENT SYSTEM")
root.geometry("1920x1000")
root.configure(bg=current_bg)
root.resizable(True, True)

#clockschuchu
clock_label = None
timer_label = None


def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

#mainmenu
def main_menu():
    global current_bg
    current_bg = "#fdf8ee"
    clear_screen()
    root.configure(bg=current_bg)

    tk.Frame(root, bg="#dfe6e9", height=1).pack(fill="x")
    tk.Frame(root, bg="#dfe6e9", height=1).pack(fill="x")
    tk.Frame(root, bg="#dfe6e9", height=1).pack(fill="x")

#title
    title_area = tk.Frame(root, bg=current_bg)
    title_area.pack(pady=(40, 0))

    title_label = tk.Label(title_area, text="SILMS", font=("Courier New", 30, "bold"), bg=current_bg, fg="#2d3436")
    title_label.pack()

    subtitle_label = tk.Label(title_area, text="made by a very tired student", font=("Courier New", 13, "italic"),
                              bg=current_bg, fg="#636e72")
    subtitle_label.pack()

    tk.Frame(root, bg="#f7e04a", height=4).pack(fill="x", padx=80, pady=14)

    global clock_label
    clock_label = tk.Label(root, font=("Courier New", 15), bg=current_bg, fg="#636e72")
    clock_label.pack()

    global timer_label
    timer_label = tk.Label(root, text="no timer running", font=("Courier New", 22, "bold"), fg="#6c5ce7", bg=current_bg)
    timer_label.pack(pady=(14, 6))

    tk.Frame(root, bg="#dfe6e9", height=1).pack(fill="x", padx=80)

#rip funds
    expense_section = tk.Frame(root, bg="#fffbe6", bd=1, relief="solid")
    expense_section.pack(fill="x", padx=80, pady=14)

    tk.Frame(expense_section, bg="#f7e04a", height=6).pack(fill="x")

    expense_title = tk.Label(expense_section, text="💰  RIP Funds", font=("Courier New", 17, "bold"), bg="#fffbe6",
                             fg="#2d3436", anchor="w")
    expense_title.pack(fill="x", padx=20, pady=(12, 6))

    tk.Frame(expense_section, bg="#dfe6e9", height=1).pack(fill="x", padx=20)

    expense_buttons = tk.Frame(expense_section, bg="#fffbe6")
    expense_buttons.pack(pady=16, padx=16)

#log an expense
    btn_add_exp = tk.Button(expense_buttons, text="log an expense..", command=add_expense, font=("Courier New", 14),
                            bg="#f7e04a", fg="#2d3436", relief="solid", bd=2, activebackground="#f7e04a",
                            activeforeground="#2d3436", cursor="circle", pady=10, padx=20, width=28)
    btn_add_exp.bind("<Enter>", lambda event: btn_add_exp.config(relief="groove", bd=3))
    btn_add_exp.bind("<Leave>", lambda event: btn_add_exp.config(relief="solid", bd=2))
    btn_add_exp.pack(side="left", padx=12)

#check moolahhh
    btn_view_exp = tk.Button(expense_buttons, text="check your moolah", command=view_expenses,
                             font=("Courier New", 14), bg="#ffeaa7", fg="#2d3436", relief="solid", bd=2,
                             activebackground="#ffeaa7", activeforeground="#2d3436", cursor="circle", pady=10, padx=20,
                             width=28)
    btn_view_exp.bind("<Enter>", lambda event: btn_view_exp.config(relief="groove", bd=3))
    btn_view_exp.bind("<Leave>", lambda event: btn_view_exp.config(relief="solid", bd=2))
    btn_view_exp.pack(side="left", padx=12)

#side quest
    task_section = tk.Frame(root, bg="#e8f4fc", bd=1, relief="solid")
    task_section.pack(fill="x", padx=80, pady=14)

    tk.Frame(task_section, bg="#f7e04a", height=6).pack(fill="x")

    task_title = tk.Label(task_section, text="🧹  Side Quests", font=("Courier New", 17, "bold"), bg="#e8f4fc",
                          fg="#2d3436", anchor="w")
    task_title.pack(fill="x", padx=20, pady=(12, 6))

    tk.Frame(task_section, bg="#dfe6e9", height=1).pack(fill="x", padx=20)

    task_buttons = tk.Frame(task_section, bg="#e8f4fc")
    task_buttons.pack(pady=16, padx=16)

#add a side quest
    btn_add_task = tk.Button(task_buttons, text="add a side quest", command=add_task, font=("Courier New", 14),
                             bg="#74b9ff", fg="#2d3436", relief="solid", bd=2, activebackground="#74b9ff",
                             activeforeground="#2d3436", cursor="circle", pady=10, padx=20, width=28)
    btn_add_task.bind("<Enter>", lambda event: btn_add_task.config(relief="groove", bd=3))
    btn_add_task.bind("<Leave>", lambda event: btn_add_task.config(relief="solid", bd=2))
    btn_add_task.pack(side="left", padx=10)

#mission complete yay
    btn_mark_task = tk.Button(task_buttons, text="mission complete", command=mark_task_done,
                              font=("Courier New", 14), bg="#a29bfe", fg="#2d3436", relief="solid", bd=2,
                              activebackground="#a29bfe", activeforeground="#2d3436", cursor="circle", pady=10, padx=20,
                              width=28)
    btn_mark_task.bind("<Enter>", lambda event: btn_mark_task.config(relief="groove", bd=3))
    btn_mark_task.bind("<Leave>", lambda event: btn_mark_task.config(relief="solid", bd=2))
    btn_mark_task.pack(side="left", padx=10)

#view side questz
    btn_view_task = tk.Button(task_buttons, text="view side quests", command=view_tasks, font=("Courier New", 14),
                              bg="#74b9ff", fg="#2d3436", relief="solid", bd=2, activebackground="#74b9ff",
                              activeforeground="#2d3436", cursor="circle", pady=10, padx=20, width=28)
    btn_view_task.bind("<Enter>", lambda event: btn_view_task.config(relief="groove", bd=3))
    btn_view_task.bind("<Leave>", lambda event: btn_view_task.config(relief="solid", bd=2))
    btn_view_task.pack(side="left", padx=10)

#lock in na
    timer_section = tk.Frame(root, bg="#fce8f4", bd=1, relief="solid")
    timer_section.pack(fill="x", padx=80, pady=14)

    tk.Frame(timer_section, bg="#f7e04a", height=6).pack(fill="x")

    timer_title = tk.Label(timer_section, text="⏱  Lock In fr", font=("Courier New", 17, "bold"), bg="#fce8f4",
                           fg="#2d3436", anchor="w")
    timer_title.pack(fill="x", padx=20, pady=(12, 6))

    tk.Frame(timer_section, bg="#dfe6e9", height=1).pack(fill="x", padx=20)

    timer_buttons = tk.Frame(timer_section, bg="#fce8f4")
    timer_buttons.pack(pady=16, padx=16)

#start to lock inzch
    btn_start_timer = tk.Button(timer_buttons, text="start to lock in", command=start_timer,
                                font=("Courier New", 14), bg="#fd79a8", fg="#2d3436", relief="solid", bd=2,
                                activebackground="#fd79a8", activeforeground="#2d3436", cursor="circle", pady=10,
                                padx=20, width=28)
    btn_start_timer.bind("<Enter>", lambda event: btn_start_timer.config(relief="groove", bd=3))
    btn_start_timer.bind("<Leave>", lambda event: btn_start_timer.config(relief="solid", bd=2))
    btn_start_timer.pack(side="left", padx=12)

#study log
    btn_view_log = tk.Button(timer_buttons, text="study log", command=view_study_log, font=("Courier New", 14),
                             bg="#fab1d3", fg="#2d3436", relief="solid", bd=2, activebackground="#fab1d3",
                             activeforeground="#2d3436", cursor="circle", pady=10, padx=20, width=28)
    btn_view_log.bind("<Enter>", lambda event: btn_view_log.config(relief="groove", bd=3))
    btn_view_log.bind("<Leave>", lambda event: btn_view_log.config(relief="solid", bd=2))
    btn_view_log.pack(side="left", padx=12)

#footer
    tk.Frame(root, bg="#dfe6e9", height=1).pack(fill="x", padx=80, pady=(10, 0))

    footer_area = tk.Frame(root, bg="#fdf8ee")
    footer_area.pack(pady=30)

    footer_label = tk.Label(footer_area, text="goodluck out there bestie  ✨", font=("Courier New", 13, "italic"),
                            bg=current_bg, fg="#636e72")
    footer_label.pack(pady=(0, 10))

#exit
    btn_exit = tk.Button(footer_area, text="bye bye!", command=root.destroy, font=("Courier New", 14), bg="#dfe6e9",
                         fg="#2d3436", relief="solid", bd=2, activebackground="#dfe6e9", activeforeground="#2d3436",
                         cursor="circle", pady=10, padx=20, width=28)
    btn_exit.bind("<Enter>", lambda event: btn_exit.config(relief="groove", bd=3))
    btn_exit.bind("<Leave>", lambda event: btn_exit.config(relief="solid", bd=2))
    btn_exit.pack()

#rip funds page
def add_expense():
    clear_screen()
    root.configure(bg=current_bg)

    tk.Frame(root, bg="#f7e04a", height=6).pack(fill="x")
    tk.Label(root, text="💸  RIP Funds", font=("Courier New", 25, "bold"), bg="#fffbe6", fg="#2d3436").pack(
        pady=(30, 6))
    tk.Frame(root, bg="#dfe6e9", height=1).pack(fill="x", padx=80, pady=1)
    tk.Frame(root, bg="#dfe6e9", height=1).pack(fill="x", padx=80, pady=1)

    tk.Label(root, text="what did you spend on?", font=("Courier New", 13), bg="#fffbe6", fg="#636e72",
             anchor="w").pack(fill="x", padx=120, pady=(10, 0))
    category_input = tk.Entry(root, font=("Courier New", 14), bg="white", relief="solid", bd=1, highlightthickness=1,
                              highlightbackground="#dfe6e9")
    category_input.pack(fill="x", padx=120, ipady=8)

    # Amount input
    tk.Label(root, text="how much (₱):", font=("Courier New", 13), bg="#fffbe6", fg="#636e72", anchor="w").pack(
        fill="x", padx=120, pady=(10, 0))
    amount_input = tk.Entry(root, font=("Courier New", 14), bg="white", relief="solid", bd=1, highlightthickness=1,
                            highlightbackground="#dfe6e9")
    amount_input.pack(fill="x", padx=120, ipady=8)

    message_area = tk.Frame(root, bg="#fffbe6")
    message_area.pack(pady=4)

    def add_expense_clicked():
        category = category_input.get().strip()
        amount_text = amount_input.get().strip()

        if category == "":
            msg = tk.Label(message_area, text="this page can't be empty!", font=("Courier New", 14), bg="#fffbe6",
                           fg="#e17055")
            msg.pack(pady=6)
            root.after(2500, msg.destroy)
            return

        try:
            amount = float(amount_text)
        except ValueError:
            msg = tk.Label(message_area, text="please enter a valid number!", font=("Courier New", 14), bg="#fffbe6",
                           fg="#e17055")
            msg.pack(pady=6)
            root.after(2500, msg.destroy)
            return

        if amount <= 0:
            msg = tk.Label(message_area, text="amount must be greater than zero!", font=("Courier New", 14),
                           bg="#fffbe6", fg="#e17055")
            msg.pack(pady=6)
            root.after(2500, msg.destroy)
            return

        if category in expenses:
            expenses[category] = expenses[category] + amount
        else:
            expenses[category] = amount

        msg = tk.Label(message_area, text="added ₱" + str(amount) + " to '" + category + "'", font=("Courier New", 14),
                       bg="#fffbe6", fg="#00b894")
        msg.pack(pady=6)
        root.after(2500, msg.destroy)

        category_input.delete(0, "end")
        amount_input.delete(0, "end")

    button_row = tk.Frame(root, bg="#fffbe6")
    button_row.pack(pady=20)

#submit button
    btn_submit = tk.Button(button_row, text="add funds!", command=add_expense_clicked, font=("Courier New", 14),
                           bg="#f7e04a", fg="#2d3436", relief="solid", bd=2, activebackground="#f7e04a",
                           activeforeground="#2d3436", cursor="circle", pady=10, padx=20, width=28)
    btn_submit.bind("<Enter>", lambda event: btn_submit.config(relief="groove", bd=3))
    btn_submit.bind("<Leave>", lambda event: btn_submit.config(relief="solid", bd=2))
    btn_submit.pack(side="left", padx=10)

#return
    btn_back = tk.Button(root, text="return to main menu", font=("Courier New", 14), background="#FFB6C1",
                         activebackground="#CDB4DA", relief="flat", cursor="cross", pady=10, padx=20, width=35,
                         command=main_menu)
    btn_back.pack(pady=30)


#view expenses
def view_expenses():
    clear_screen()
    root.configure(bg="#fffbe6")

    tk.Frame(root, bg="#f7e04a", height=6).pack(fill="x")
    tk.Label(root, text="📊  Moolah", font=("Courier New", 25, "bold"), bg="#fffbe6", fg="#2d3436").pack(pady=(30, 6))
    tk.Frame(root, bg="#dfe6e9", height=1).pack(fill="x", padx=80, pady=1)
    tk.Frame(root, bg="#dfe6e9", height=1).pack(fill="x", padx=80, pady=1)

    content_area = tk.Frame(root, bg="#fffbe6")
    content_area.pack(padx=120, fill="both", expand=True, pady=10)

    if len(expenses) == 0:
        tk.Label(content_area, text="no expenses yet...", font=("Courier New", 14), bg="#fffbe6", fg="#636e72").pack(
            pady=30)
    else:
        canvas = tk.Canvas(content_area, bg="#fffbe6", highlightthickness=0)
        scrollbar = tk.Scrollbar(content_area, orient="vertical", command=canvas.yview)
        inner_frame = tk.Frame(canvas, bg="#fffbe6")

        inner_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        total_spent = 0
        for category_name, amount_spent in expenses.items():
            row = tk.Frame(inner_frame, bg="#fffbe6")
            row.pack(fill="x", pady=5)

            tk.Label(row, text="• " + category_name, font=("Courier New", 14), bg="#fffbe6", fg="#2d3436",
                     anchor="w").pack(side="left")
            tk.Label(row, text="₱" + str(round(amount_spent, 2)), font=("Courier New", 14, "bold"), bg="#fffbe6",
                     fg="#e17055", anchor="e").pack(side="right")
            tk.Frame(inner_frame, bg="#dfe6e9", height=1).pack(fill="x")

            total_spent = total_spent + amount_spent

        tk.Frame(content_area, bg="#636e72", height=2).pack(fill="x", pady=8)
        total_row = tk.Frame(content_area, bg="#fffbe6")
        total_row.pack(fill="x")
        tk.Label(total_row, text="total:", font=("Courier New", 16, "bold"), bg="#fffbe6").pack(side="left")
        tk.Label(total_row, text="₱" + str(round(total_spent, 2)), font=("Courier New", 16, "bold"), bg="#fffbe6",
                 fg="#e17055").pack(side="right")

#return
    btn_back = tk.Button(root, text="return to main menu", font=("Courier New", 14), background="#FFB6C1",
                         activebackground="#CDB4DA", relief="flat", cursor="cross", pady=10, padx=20, width=35,
                         command=main_menu)
    btn_back.pack(pady=40)


#side quest page
def add_task():
    clear_screen()
    root.configure(bg="#e8f4fc")

    tk.Frame(root, bg="#f7e04a", height=6).pack(fill="x")
    tk.Label(root, text="✏️  Side Quests", font=("Courier New", 25, "bold"), bg="#e8f4fc", fg="#2d3436").pack(pady=(30, 6))
    tk.Frame(root, bg="#dfe6e9", height=1).pack(fill="x", padx=80, pady=1)
    tk.Frame(root, bg="#dfe6e9", height=1).pack(fill="x", padx=80, pady=1)

    tk.Label(root, text="what do you need to do:", font=("Courier New", 13), bg="#e8f4fc", fg="#636e72",
             anchor="w").pack(fill="x", padx=120, pady=(10, 0))
    task_input = tk.Entry(root, font=("Courier New", 14), bg="white", relief="solid", bd=1, highlightthickness=1,
                          highlightbackground="#dfe6e9")
    task_input.pack(fill="x", padx=120, ipady=8)

    tk.Label(root, text="task type:", font=("Courier New", 13), bg="#e8f4fc", fg="#636e72", anchor="w").pack(fill="x",
                                                                                                             padx=120,
                                                                                                             pady=(10,
                                                                                                                   0))

    task_type = tk.StringVar()
    task_type.set("study")

    radio_area = tk.Frame(root, bg="#e8f4fc")
    radio_area.pack(padx=120, anchor="w", pady=6)

    tk.Radiobutton(radio_area, text="study", variable=task_type, value="study", font=("Courier New", 14), bg="#e8f4fc",
                   activebackground="#e8f4fc", selectcolor="white").pack(side="left", padx=14)
    tk.Radiobutton(radio_area, text="chores", variable=task_type, value="chores", font=("Courier New", 14),
                   bg="#e8f4fc", activebackground="#e8f4fc", selectcolor="white").pack(side="left", padx=14)

    message_area = tk.Frame(root, bg="#e8f4fc")
    message_area.pack(pady=4)

    def add_task_clicked():
        task_text = task_input.get().strip()

        if task_text == "":
            msg = tk.Label(message_area, text="you forgot to type a task!", font=("Courier New", 14), bg="#e8f4fc",
                           fg="#e17055")
            msg.pack(pady=6)
            root.after(2500, msg.destroy)
            return

        new_task = {
            "task": task_text,
            "type": task_type.get(),
            "done": False
        }
        tasks.append(new_task)

        msg = tk.Label(message_area, text="task added!", font=("Courier New", 14), bg="#e8f4fc", fg="#00b894")
        msg.pack(pady=6)
        root.after(2500, msg.destroy)
        task_input.delete(0, "end")

    btn_submit = tk.Button(root, text="add task", command=add_task_clicked, font=("Courier New", 14), bg="#74b9ff",
                           fg="#2d3436", relief="solid", bd=2, activebackground="#74b9ff", activeforeground="#2d3436",
                           cursor="circle", pady=10, padx=20, width=28)
    btn_submit.bind("<Enter>", lambda event: btn_submit.config(relief="groove", bd=3))
    btn_submit.bind("<Leave>", lambda event: btn_submit.config(relief="solid", bd=2))
    btn_submit.pack(pady=20)

    btn_back = tk.Button(root, text="return to main menu", font=("Courier New", 14), background="#FFB6C1",
                         activebackground="#CDB4DA", relief="flat", cursor="cross", pady=10, padx=20, width=35,
                         command=main_menu)
    btn_back.pack(pady=40)


#mission complete
def mark_task_done():
    clear_screen()
    root.configure(bg="#e8f4fc")

    tk.Frame(root, bg="#f7e04a", height=6).pack(fill="x")
    tk.Label(root, text="✅  Mark Task Done", font=("Courier New", 25, "bold"), bg="#e8f4fc", fg="#2d3436").pack(
        pady=(30, 6))
    tk.Frame(root, bg="#dfe6e9", height=1).pack(fill="x", padx=80, pady=1)
    tk.Frame(root, bg="#dfe6e9", height=1).pack(fill="x", padx=80, pady=1)

    if len(tasks) == 0:
        tk.Label(root, text="no tasks yet! go add some.", font=("Courier New", 14), bg="#e8f4fc", fg="#636e72").pack(
            pady=30)
        btn_back = tk.Button(root, text="return to main menu", font=("Courier New", 14), background="#FFB6C1",
                             activebackground="#CDB4DA", relief="flat", cursor="cross", pady=10, padx=20, width=35,
                             command=main_menu)
        btn_back.pack(pady=40)
        return

    selected_index = tk.IntVar()
    selected_index.set(-1)

    outer_frame = tk.Frame(root, bg="#e8f4fc")
    outer_frame.pack(padx=120, fill="both", expand=True, pady=10)

    canvas = tk.Canvas(outer_frame, bg="#e8f4fc", highlightthickness=0)
    scrollbar = tk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
    inner_frame = tk.Frame(canvas, bg="#e8f4fc")

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

        tk.Radiobutton(inner_frame, text=label_text, variable=selected_index, value=i, font=("Courier New", 14),
                       bg="#e8f4fc", state=button_state, activebackground="#e8f4fc", selectcolor="white",
                       anchor="w").pack(fill="x", padx=10, pady=5)

    message_area = tk.Frame(root, bg="#e8f4fc")
    message_area.pack(pady=4)

    def mark_done_clicked():
        idx = selected_index.get()

        if idx == -1:
            msg = tk.Label(message_area, text="please pick a task first!", font=("Courier New", 14), bg="#e8f4fc",
                           fg="#e17055")
            msg.pack(pady=6)
            root.after(2500, msg.destroy)
            return

        tasks[idx]["done"] = True
        msg = tk.Label(message_area, text="task marked as done! great job!", font=("Courier New", 14), bg="#e8f4fc",
                       fg="#00b894")
        msg.pack(pady=6)
        root.after(2500, msg.destroy)

    btn_submit = tk.Button(root, text="mark done", command=mark_done_clicked, font=("Courier New", 14), bg="#74b9ff",
                           fg="#2d3436", relief="solid", bd=2, activebackground="#74b9ff", activeforeground="#2d3436",
                           cursor="circle", pady=10, padx=20, width=28)
    btn_submit.bind("<Enter>", lambda event: btn_submit.config(relief="groove", bd=3))
    btn_submit.bind("<Leave>", lambda event: btn_submit.config(relief="solid", bd=2))
    btn_submit.pack(pady=16)

    btn_back = tk.Button(root, text="return to main menu", font=("Courier New", 14), background="#FFB6C1",
                         activebackground="#CDB4DA", relief="flat", cursor="cross", pady=10, padx=20, width=35,
                         command=main_menu)
    btn_back.pack(pady=40)


#view side quest
def view_tasks():
    clear_screen()
    root.configure(bg="#e8f4fc")

    tk.Frame(root, bg="#f7e04a", height=6).pack(fill="x")
    tk.Label(root, text="📋  Task List", font=("Courier New", 25, "bold"), bg="#e8f4fc", fg="#2d3436").pack(pady=(30, 6))
    tk.Frame(root, bg="#dfe6e9", height=1).pack(fill="x", padx=80, pady=1)
    tk.Frame(root, bg="#dfe6e9", height=1).pack(fill="x", padx=80, pady=1)

    content_area = tk.Frame(root, bg="#e8f4fc")
    content_area.pack(padx=120, fill="both", expand=True, pady=10)

    if len(tasks) == 0:
        tk.Label(content_area, text="nothing here yet!", font=("Courier New", 14), bg="#e8f4fc", fg="#636e72").pack(
            pady=30)
    else:
        canvas = tk.Canvas(content_area, bg="#e8f4fc", highlightthickness=0)
        scrollbar = tk.Scrollbar(content_area, orient="vertical", command=canvas.yview)
        inner_frame = tk.Frame(canvas, bg="#e8f4fc")

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

            row = tk.Frame(inner_frame, bg="#e8f4fc")
            row.pack(fill="x", pady=5, padx=6)

            tk.Label(row, text=icon, bg="#e8f4fc", font=("Courier New", 14)).pack(side="left")
            tk.Label(row, text="  " + task_item["task"] + "  [" + task_item["type"] + "]", font=("Courier New", 14),
                     bg="#e8f4fc", fg=text_color, anchor="w").pack(side="left")
            tk.Frame(inner_frame, bg="#dfe6e9", height=1).pack(fill="x", padx=6)

    btn_back = tk.Button(root, text="return to main menu", font=("Courier New", 14), background="#FFB6C1",
                         activebackground="#CDB4DA", relief="flat", cursor="cross", pady=10, padx=20, width=35,
                         command=main_menu)
    btn_back.pack(pady=40)


#start lock in
def start_timer():
    clear_screen()
    root.configure(bg="#fce8f4")

    tk.Frame(root, bg="#f7e04a", height=6).pack(fill="x")
    tk.Label(root, text="⏱  Time to Lock In", font=("Courier New", 25, "bold"), bg="#fce8f4", fg="#2d3436").pack(
        pady=(30, 6))
    tk.Frame(root, bg="#dfe6e9", height=1).pack(fill="x", padx=80, pady=1)
    tk.Frame(root, bg="#dfe6e9", height=1).pack(fill="x", padx=80, pady=1)

    tk.Label(root, text="what subject are you studying:", font=("Courier New", 13), bg="#fce8f4", fg="#636e72",
             anchor="w").pack(fill="x", padx=120, pady=(10, 0))
    subject_input = tk.Entry(root, font=("Courier New", 14), bg="white", relief="solid", bd=1, highlightthickness=1,
                             highlightbackground="#dfe6e9")
    subject_input.pack(fill="x", padx=120, ipady=8)

    tk.Label(root, text="how long will you study (minutes):", font=("Courier New", 13), bg="#fce8f4", fg="#636e72",
             anchor="w").pack(fill="x", padx=120, pady=(10, 0))
    study_time_input = tk.Entry(root, font=("Courier New", 14), bg="white", relief="solid", bd=1, highlightthickness=1,
                                highlightbackground="#dfe6e9")
    study_time_input.pack(fill="x", padx=120, ipady=8)

    tk.Label(root, text="break time after (minutes, 0 = no break):", font=("Courier New", 13), bg="#fce8f4",
             fg="#636e72", anchor="w").pack(fill="x", padx=120, pady=(10, 0))
    break_time_input = tk.Entry(root, font=("Courier New", 14), bg="white", relief="solid", bd=1, highlightthickness=1,
                                highlightbackground="#dfe6e9")
    break_time_input.insert(0, "0")
    break_time_input.pack(fill="x", padx=120, ipady=8)

    message_area = tk.Frame(root, bg="#fce8f4")
    message_area.pack(pady=4)

    def start_timer_clicked():
        subject = subject_input.get().strip()

        if subject == "":
            msg = tk.Label(message_area, text="please enter a subject!", font=("Courier New", 14), bg="#fce8f4",
                           fg="#e17055")
            msg.pack(pady=6)
            root.after(2500, msg.destroy)
            return

        try:
            study_minutes = int(study_time_input.get().strip())
            break_minutes = int(break_time_input.get().strip())
        except ValueError:
            msg = tk.Label(message_area, text="please enter valid whole numbers!", font=("Courier New", 14),
                           bg="#fce8f4", fg="#e17055")
            msg.pack(pady=6)
            root.after(2500, msg.destroy)
            return

        if study_minutes <= 0 or break_minutes < 0:
            msg = tk.Label(message_area, text="study time must be at least 1 minute!", font=("Courier New", 14),
                           bg="#fce8f4", fg="#e17055")
            msg.pack(pady=6)
            root.after(2500, msg.destroy)
            return

        subject = subject.title()

        try:
            timer_label.config(text="timer starting... lock in!")
        except:
            pass

        timer_thread = threading.Thread(target=run_timer, args=(subject, study_minutes, break_minutes), daemon=True)
        timer_thread.start()

        msg = tk.Label(message_area, text="timer started for " + subject + "! go go go!", font=("Courier New", 14),
                       bg="#fce8f4", fg="#00b894")
        msg.pack(pady=6)
        root.after(2500, msg.destroy)

    btn_submit = tk.Button(root, text="start timer", command=start_timer_clicked, font=("Courier New", 14),
                           bg="#fd79a8", fg="#2d3436", relief="solid", bd=2, activebackground="#fd79a8",
                           activeforeground="#2d3436", cursor="circle", pady=10, padx=20, width=28)
    btn_submit.bind("<Enter>", lambda event: btn_submit.config(relief="groove", bd=3))
    btn_submit.bind("<Leave>", lambda event: btn_submit.config(relief="solid", bd=2))
    btn_submit.pack(pady=20)

    btn_back = tk.Button(root, text="return to main menu", font=("Courier New", 14), background="#FFB6C1",
                         activebackground="#CDB4DA", relief="flat", cursor="cross", pady=10, padx=20, width=35,
                         command=main_menu)
    btn_back.pack(pady=40)


#study log
def view_study_log():
    clear_screen()
    root.configure(bg="#fce8f4")

    tk.Frame(root, bg="#f7e04a", height=6).pack(fill="x")
    tk.Label(root, text="📓  Study Log", font=("Courier New", 25, "bold"), bg="#fce8f4", fg="#2d3436").pack(pady=(30, 6))
    tk.Frame(root, bg="#dfe6e9", height=1).pack(fill="x", padx=80, pady=1)
    tk.Frame(root, bg="#dfe6e9", height=1).pack(fill="x", padx=80, pady=1)

    content_area = tk.Frame(root, bg="#fce8f4")
    content_area.pack(padx=120, fill="both", expand=True, pady=10)

    if len(study_log) == 0:
        tk.Label(content_area, text="you haven't studied anything yet!", font=("Courier New", 14), bg="#fce8f4",
                 fg="#636e72").pack(pady=30)
    else:
        total_minutes = 0

        for subject_name, minutes_studied in study_log.items():
            row = tk.Frame(content_area, bg="#fce8f4")
            row.pack(fill="x", pady=5)

            tk.Label(row, text="• " + subject_name, font=("Courier New", 14), bg="#fce8f4", fg="#2d3436",
                     anchor="w").pack(side="left")
            tk.Label(row, text=str(minutes_studied) + " min", font=("Courier New", 14, "bold"), bg="#fce8f4",
                     fg="#6c5ce7", anchor="e").pack(side="right")
            tk.Frame(content_area, bg="#dfe6e9", height=1).pack(fill="x")

            total_minutes = total_minutes + minutes_studied

        tk.Frame(content_area, bg="#636e72", height=2).pack(fill="x", pady=8)
        total_row = tk.Frame(content_area, bg="#fce8f4")
        total_row.pack(fill="x")
        tk.Label(total_row, text="total study time:", font=("Courier New", 16, "bold"), bg="#fce8f4").pack(side="left")
        tk.Label(total_row, text=str(total_minutes) + " min", font=("Courier New", 16, "bold"), bg="#fce8f4",
                 fg="#6c5ce7").pack(side="right")

    btn_back = tk.Button(root, text="return to main menu", font=("Courier New", 14), background="#FFB6C1",
                         activebackground="#CDB4DA", relief="flat", cursor="cross", pady=10, padx=20, width=35,
                         command=main_menu)
    btn_back.pack(pady=40)


def run_timer(subject, study_minutes, break_minutes):
    total_seconds = study_minutes * 60

    while total_seconds > 0:
        minutes_left = total_seconds // 60
        seconds_left = total_seconds % 60
        time_display = "studying: " + str(minutes_left).zfill(2) + ":" + str(seconds_left).zfill(2)

        try:
            timer_label.config(text=time_display)
        except:
            pass

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

            try:
                timer_label.config(text=time_display)
            except:
                pass

            time.sleep(1)
            total_seconds = total_seconds - 1

        winsound.Beep(800, 400)
        winsound.Beep(800, 400)

    try:
        timer_label.config(text="timer done!! great job!")
    except:
        pass


def update_clock():
    current_time = time.strftime("%I:%M:%S %p")
    current_date = time.strftime("%A, %B %d")

    try:
        clock_label.config(text=current_date + "   " + current_time)
    except:
        pass

    root.after(1000, update_clock)


main_menu()

update_clock()

root.mainloop()