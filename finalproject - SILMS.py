import tkinter as tk
from tkinter import messagebox
import time
import threading
import winsound

# ─────────────────────────────────────────────
#  DATA
# ─────────────────────────────────────────────
expenses  = {}
tasks     = []
study_log = {}

# ─────────────────────────────────────────────
#  THEME / PALETTE
# ─────────────────────────────────────────────
BG_MAIN       = "#fdf8ee"
BG_EXPENSE    = "#fffbe6"
BG_TASK       = "#e8f4fc"
BG_TIMER      = "#fce8f4"

ACCENT_YELLOW = "#f7e04a"
ACCENT_BLUE   = "#74b9ff"
ACCENT_PINK   = "#fd79a8"
ACCENT_GREEN  = "#55efc4"

TEXT_DARK  = "#2d3436"
TEXT_MID   = "#636e72"
TEXT_LIGHT = "#b2bec3"

FONT_TITLE  = ("Courier New", 28, "bold")
FONT_HEAD   = ("Courier New", 17, "bold")
FONT_BODY   = ("Courier New", 14)
FONT_SMALL  = ("Courier New", 13)
FONT_CLOCK  = ("Courier New", 15)
FONT_TIMER  = ("Courier New", 22, "bold")
FONT_BIG    = ("Courier New", 25, "bold")

RULED_LINE  = "#dfe6e9"

# ─────────────────────────────────────────────
#  ROOT WINDOW
# ─────────────────────────────────────────────
root = tk.Tk()
root.title("STUDENT INDEPENDENT LIVING MANAGEMENT SYSTEM")
root.geometry("1920x1080")
root.configure(bg=BG_MAIN)
root.resizable(False, False)

# ─────────────────────────────────────────────
#  FRAME CONTAINER  (all pages live here)
# ─────────────────────────────────────────────
container = tk.Frame(root, bg=BG_MAIN)
container.pack(fill="both", expand=True)
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

frames = {}

def show_frame(name):
    if name in ("add_expense", "view_expenses",
                "add_task", "mark_task_done", "view_tasks",
                "start_timer", "view_study_log"):
        if name in frames:
            frames[name].destroy()
        f = PAGE_BUILDERS[name](container)
        f.grid(row=0, column=0, sticky="nsew")
        frames[name] = f
    frames[name].tkraise()


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def mk_btn(parent, text, cmd, bg, width=28):
    btn = tk.Button(
        parent, text=text, command=cmd,
        font=FONT_BODY, bg=bg, fg=TEXT_DARK,
        relief="solid", bd=2,
        activebackground=bg, activeforeground=TEXT_DARK,
        cursor="hand2", pady=10, padx=20,
        highlightthickness=0, width=width,
    )
    btn.bind("<Enter>", lambda e, b=btn: b.config(relief="groove", bd=3))
    btn.bind("<Leave>", lambda e, b=btn: b.config(relief="solid",  bd=2))
    return btn


def back_btn(parent):
    return tk.Button(
        parent,
        text="Return to Main Menu",
        font=("Courier New", 20),
        background="#FFB6C1",
        activebackground="#CDB4DA",
        relief="flat",
        cursor="hand2",
        pady=12, padx=24,
        command=lambda: show_frame("main"),
    )


def page_header(parent, icon, title, bg):
    tk.Frame(parent, bg=ACCENT_YELLOW, height=6).pack(fill="x")
    tk.Label(parent, text=f"{icon}  {title}",
             font=FONT_BIG, bg=bg, fg=TEXT_DARK).pack(pady=(30, 6))
    for _ in range(2):
        tk.Frame(parent, bg=RULED_LINE, height=1).pack(fill="x", padx=80, pady=1)


def lbl(parent, text, bg, font=None, fg=None):
    tk.Label(parent, text=text, font=font or FONT_SMALL,
             bg=bg, fg=fg or TEXT_MID, anchor="w").pack(fill="x", padx=120, pady=(10, 0))


def entry(parent, bg, default=""):
    e = tk.Entry(parent, font=FONT_BODY, bg="white",
                 relief="solid", bd=1, highlightthickness=1,
                 highlightbackground=RULED_LINE)
    e.insert(0, default)
    e.pack(fill="x", padx=120, ipady=8)
    return e


def flash_msg(parent, bg, text, color=TEXT_DARK):
    lbl_w = tk.Label(parent, text=text, font=FONT_BODY, bg=bg, fg=color)
    lbl_w.pack(pady=6)
    parent.after(2500, lbl_w.destroy)


# ─────────────────────────────────────────────
#  MAIN MENU PAGE
# ─────────────────────────────────────────────
def build_main(parent):
    f = tk.Frame(parent, bg=BG_MAIN)

    for _ in range(3):
        tk.Frame(f, bg=RULED_LINE, height=1).pack(fill="x")

    title_frame = tk.Frame(f, bg=BG_MAIN)
    title_frame.pack(pady=(40, 0))
    tk.Label(title_frame, text="📓  SILMS",
             font=("Courier New", 30, "bold"), bg=BG_MAIN, fg=TEXT_DARK).pack()
    tk.Label(title_frame, text="— made by a very tired student —",
             font=("Courier New", 13, "italic"), bg=BG_MAIN, fg=TEXT_MID).pack()

    tk.Frame(f, bg=ACCENT_YELLOW, height=4).pack(fill="x", padx=80, pady=14)

    global clock_label
    clock_label = tk.Label(f, font=FONT_CLOCK, bg=BG_MAIN, fg=TEXT_MID)
    clock_label.pack()

    global timer_label
    timer_label = tk.Label(f, text="⏳ no timer running",
                           font=FONT_TIMER, fg="#6c5ce7", bg=BG_MAIN)
    timer_label.pack(pady=(14, 6))

    tk.Frame(f, bg=RULED_LINE, height=1).pack(fill="x", padx=80)

    def section(label_text, bg, btn_fn):
        outer = tk.Frame(f, bg=bg, bd=1, relief="solid", highlightbackground=RULED_LINE)
        outer.pack(fill="x", padx=80, pady=14)
        tk.Frame(outer, bg=ACCENT_YELLOW, height=6).pack(fill="x")
        tk.Label(outer, text=label_text, font=FONT_HEAD,
                 bg=bg, fg=TEXT_DARK, anchor="w").pack(fill="x", padx=20, pady=(12, 6))
        tk.Frame(outer, bg=RULED_LINE, height=1).pack(fill="x", padx=20)
        row = tk.Frame(outer, bg=bg)
        row.pack(pady=16, padx=16)
        btn_fn(row)

    def expense_btns(r):
        mk_btn(r, "💸  log an expense",  lambda: show_frame("add_expense"),  ACCENT_YELLOW).pack(side="left", padx=12)
        mk_btn(r, "📊  view expenses",   lambda: show_frame("view_expenses"), "#ffeaa7").pack(side="left", padx=12)

    def task_btns(r):
        mk_btn(r, "✏️   add a task",      lambda: show_frame("add_task"),       ACCENT_BLUE).pack(side="left", padx=10)
        mk_btn(r, "✅  mark task done",   lambda: show_frame("mark_task_done"), "#a29bfe").pack(side="left", padx=10)
        mk_btn(r, "📋  view all tasks",   lambda: show_frame("view_tasks"),     "#74b9ff").pack(side="left", padx=10)
 
    def timer_btns(r):
        mk_btn(r, "⏱  start study timer", lambda: show_frame("start_timer"),    ACCENT_PINK).pack(side="left", padx=12)
        mk_btn(r, "📓  study log",         lambda: show_frame("view_study_log"), "#fab1d3").pack(side="left", padx=12)

    section("💰  Broke Check",   BG_EXPENSE, expense_btns)
    section("🧹  Grind Mode On", BG_TASK,    task_btns)
    section("⏱  Lock In",        BG_TIMER,   timer_btns)

    tk.Frame(f, bg=RULED_LINE, height=1).pack(fill="x", padx=80, pady=(10, 0))
    footer = tk.Frame(f, bg=BG_MAIN)
    footer.pack(pady=30)
    tk.Label(footer, text="goodluck out there bestie  ✨",
             font=("Courier New", 13, "italic"), bg=BG_MAIN, fg=TEXT_MID).pack(pady=(0, 10))
    mk_btn(footer, "🚪  exit", root.destroy, "#dfe6e9").pack()

    return f


# ─────────────────────────────────────────────
#  ADD EXPENSE PAGE
# ─────────────────────────────────────────────
def build_add_expense(parent):
    f = tk.Frame(parent, bg=BG_EXPENSE)
    page_header(f, "💸", "Add Expense", BG_EXPENSE)

    lbl(f, "what did u spend on??", BG_EXPENSE)
    cat_e = entry(f, BG_EXPENSE)
    lbl(f, "how much (₱):", BG_EXPENSE)
    amt_e = entry(f, BG_EXPENSE)

    msg_frame = tk.Frame(f, bg=BG_EXPENSE)
    msg_frame.pack(pady=4)

    def submit():
        cat = cat_e.get().strip()
        if not cat:
            flash_msg(msg_frame, BG_EXPENSE, "⚠️  category can't be empty !!", "#e17055")
            return
        try:
            amt = float(amt_e.get().strip())
            if amt <= 0:
                raise ValueError
        except ValueError:
            flash_msg(msg_frame, BG_EXPENSE, "⚠️  enter a valid positive number !!", "#e17055")
            return
        expenses[cat] = expenses.get(cat, 0) + amt
        flash_msg(msg_frame, BG_EXPENSE, f"✅  added ₱{amt:.2f} to '{cat}' 📝", "#00b894")
        cat_e.delete(0, "end")
        amt_e.delete(0, "end")

    btn_row = tk.Frame(f, bg=BG_EXPENSE)
    btn_row.pack(pady=20)
    mk_btn(btn_row, "➕  add it", submit, ACCENT_YELLOW).pack(side="left", padx=10)
    back_btn(f).pack(pady=40)
    return f


# ─────────────────────────────────────────────
#  VIEW EXPENSES PAGE
# ─────────────────────────────────────────────
def build_view_expenses(parent):
    f = tk.Frame(parent, bg=BG_EXPENSE)
    page_header(f, "📊", "Expenses", BG_EXPENSE)

    body = tk.Frame(f, bg=BG_EXPENSE)
    body.pack(padx=120, fill="both", expand=True, pady=10)

    if not expenses:
        tk.Label(body, text="no expenses yet... 😭",
                 font=FONT_BODY, bg=BG_EXPENSE, fg=TEXT_MID).pack(pady=30)
    else:
        canvas    = tk.Canvas(body, bg=BG_EXPENSE, highlightthickness=0)
        scrollbar = tk.Scrollbar(body, orient="vertical", command=canvas.yview)
        inner     = tk.Frame(canvas, bg=BG_EXPENSE)
        inner.bind("<Configure>",
                   lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        total = 0
        for cat, amt in expenses.items():
            row = tk.Frame(inner, bg=BG_EXPENSE)
            row.pack(fill="x", pady=5)
            tk.Label(row, text=f"• {cat}", font=FONT_BODY,
                     bg=BG_EXPENSE, fg=TEXT_DARK, anchor="w").pack(side="left")
            tk.Label(row, text=f"₱{amt:.2f}", font=("Courier New", 14, "bold"),
                     bg=BG_EXPENSE, fg="#e17055", anchor="e").pack(side="right")
            tk.Frame(inner, bg=RULED_LINE, height=1).pack(fill="x")
            total += amt

        tk.Frame(body, bg=TEXT_MID, height=2).pack(fill="x", pady=8)
        total_row = tk.Frame(body, bg=BG_EXPENSE)
        total_row.pack(fill="x")
        tk.Label(total_row, text="total 💀:", font=("Courier New", 16, "bold"),
                 bg=BG_EXPENSE).pack(side="left")
        tk.Label(total_row, text=f"₱{total:.2f}", font=("Courier New", 16, "bold"),
                 bg=BG_EXPENSE, fg="#e17055").pack(side="right")

    back_btn(f).pack(pady=40)
    return f


# ─────────────────────────────────────────────
#  ADD TASK PAGE
# ─────────────────────────────────────────────
def build_add_task(parent):
    f = tk.Frame(parent, bg=BG_TASK)
    page_header(f, "✏️", "Add Task", BG_TASK)

    lbl(f, "what do u need to do:", BG_TASK)
    task_e = entry(f, BG_TASK)
    lbl(f, "vibe check (type):", BG_TASK)
    type_var = tk.StringVar(value="study")
    radio_row = tk.Frame(f, bg=BG_TASK)
    radio_row.pack(padx=120, anchor="w", pady=6)
    for opt, emoji in [("study", "📚 study"), ("chores", "🧹 chores")]:
        tk.Radiobutton(radio_row, text=emoji, variable=type_var, value=opt,
                       font=FONT_BODY, bg=BG_TASK,
                       activebackground=BG_TASK, selectcolor="white").pack(side="left", padx=14)

    msg_frame = tk.Frame(f, bg=BG_TASK)
    msg_frame.pack(pady=4)

    def submit():
        t = task_e.get().strip()
        if not t:
            flash_msg(msg_frame, BG_TASK, "⚠️  u forgot to type a task!!", "#e17055")
            return
        tasks.append({"task": t, "type": type_var.get(), "done": False})
        flash_msg(msg_frame, BG_TASK, "✅  task added to ur list!", "#00b894")
        task_e.delete(0, "end")

    mk_btn(f, "➕  add task", submit, ACCENT_BLUE).pack(pady=20)
    back_btn(f).pack(pady=40)
    return f


# ─────────────────────────────────────────────
#  MARK TASK DONE PAGE
# ─────────────────────────────────────────────
def build_mark_task_done(parent):
    f = tk.Frame(parent, bg=BG_TASK)
    page_header(f, "✅", "Mark Task Done", BG_TASK)

    if not tasks:
        tk.Label(f, text="no tasks!! go make some lol",
                 font=FONT_BODY, bg=BG_TASK, fg=TEXT_MID).pack(pady=30)
        back_btn(f).pack(pady=40)
        return f

    sel = tk.IntVar(value=-1)
    outer = tk.Frame(f, bg=BG_TASK)
    outer.pack(padx=120, fill="both", expand=True, pady=10)

    canvas    = tk.Canvas(outer, bg=BG_TASK, highlightthickness=0)
    scrollbar = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
    inner     = tk.Frame(canvas, bg=BG_TASK)
    inner.bind("<Configure>",
               lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=inner, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for i, t in enumerate(tasks):
        done  = t["done"]
        icon  = "✅" if done else "⬜"
        label = f"{icon}  {t['task']}  [{t['type']}]"
        state = "disabled" if done else "normal"
        tk.Radiobutton(inner, text=label, variable=sel, value=i,
                       font=FONT_BODY, bg=BG_TASK, state=state,
                       activebackground=BG_TASK, selectcolor="white",
                       anchor="w").pack(fill="x", padx=10, pady=5)

    msg_frame = tk.Frame(f, bg=BG_TASK)
    msg_frame.pack(pady=4)

    def submit():
        idx = sel.get()
        if idx == -1:
            flash_msg(msg_frame, BG_TASK, "⚠️  pick a task first!", "#e17055")
            return
        tasks[idx]["done"] = True
        flash_msg(msg_frame, BG_TASK, "🎉  LETS GOOO!! task marked done!", "#00b894")

    mk_btn(f, "✅  mark done", submit, ACCENT_BLUE).pack(pady=16)
    back_btn(f).pack(pady=40)
    return f


# ─────────────────────────────────────────────
#  VIEW TASKS PAGE
# ─────────────────────────────────────────────
def build_view_tasks(parent):
    f = tk.Frame(parent, bg=BG_TASK)
    page_header(f, "📋", "Task List", BG_TASK)

    body = tk.Frame(f, bg=BG_TASK)
    body.pack(padx=120, fill="both", expand=True, pady=10)

    if not tasks:
        tk.Label(body, text="nothing here yet... goofing off?? 😅",
                 font=FONT_BODY, bg=BG_TASK, fg=TEXT_MID).pack(pady=30)
    else:
        canvas    = tk.Canvas(body, bg=BG_TASK, highlightthickness=0)
        scrollbar = tk.Scrollbar(body, orient="vertical", command=canvas.yview)
        inner     = tk.Frame(canvas, bg=BG_TASK)
        inner.bind("<Configure>",
                   lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for t in tasks:
            done  = t["done"]
            icon  = "✅" if done else "⬜"
            color = "#00b894" if done else "#d63031"
            row   = tk.Frame(inner, bg=BG_TASK)
            row.pack(fill="x", pady=5, padx=6)
            tk.Label(row, text=icon, bg=BG_TASK,
                     font=("Courier New", 14)).pack(side="left")
            tk.Label(row, text=f"  {t['task']}  [{t['type']}]",
                     font=FONT_BODY, bg=BG_TASK, fg=color,
                     anchor="w").pack(side="left")
            tk.Frame(inner, bg=RULED_LINE, height=1).pack(fill="x", padx=6)

    back_btn(f).pack(pady=40)
    return f


# ─────────────────────────────────────────────
#  START TIMER PAGE
# ─────────────────────────────────────────────
def build_start_timer(parent):
    f = tk.Frame(parent, bg=BG_TIMER)
    page_header(f, "⏱", "Start Timer", BG_TIMER)

    lbl(f, "what subject r u suffering thru:", BG_TIMER)
    sub_e = entry(f, BG_TIMER)
    lbl(f, "how long r u gonna study (mins):", BG_TIMER)
    study_e = entry(f, BG_TIMER)
    lbl(f, "break time (mins, 0 = no break):", BG_TIMER)
    break_e = entry(f, BG_TIMER, default="0")

    msg_frame = tk.Frame(f, bg=BG_TIMER)
    msg_frame.pack(pady=4)

    def submit():
        sub = sub_e.get().strip()
        if not sub:
            flash_msg(msg_frame, BG_TIMER, "⚠️  what subject?", "#e17055")
            return
        try:
            sm = int(study_e.get().strip())
            bm = int(break_e.get().strip())
            if sm <= 0 or bm < 0:
                raise ValueError
        except ValueError:
            flash_msg(msg_frame, BG_TIMER, "⚠️  enter valid numbers!!", "#e17055")
            return
        timer_label.config(text="⏳ timer starting... lock in!!")
        threading.Thread(target=timer_thread, args=(sub.title(), sm, bm), daemon=True).start()
        flash_msg(msg_frame, BG_TIMER, f"✅  timer started for {sub.title()}! go go go 🔥", "#00b894")

    mk_btn(f, "⏱  start timer", submit, ACCENT_PINK).pack(pady=20)
    back_btn(f).pack(pady=40)
    return f


# ─────────────────────────────────────────────
#  VIEW STUDY LOG PAGE
# ─────────────────────────────────────────────
def build_view_study_log(parent):
    f = tk.Frame(parent, bg=BG_TIMER)
    page_header(f, "📓", "Study Log", BG_TIMER)

    body = tk.Frame(f, bg=BG_TIMER)
    body.pack(padx=120, fill="both", expand=True, pady=10)

    if not study_log:
        tk.Label(body, text="u haven't studied anything yet 😬",
                 font=FONT_BODY, bg=BG_TIMER, fg=TEXT_MID).pack(pady=30)
    else:
        total = 0
        for sub, mins in study_log.items():
            row = tk.Frame(body, bg=BG_TIMER)
            row.pack(fill="x", pady=5)
            tk.Label(row, text=f"• {sub}", font=FONT_BODY,
                     bg=BG_TIMER, fg=TEXT_DARK, anchor="w").pack(side="left")
            tk.Label(row, text=f"{mins} min", font=("Courier New", 14, "bold"),
                     bg=BG_TIMER, fg="#6c5ce7", anchor="e").pack(side="right")
            tk.Frame(body, bg=RULED_LINE, height=1).pack(fill="x")
            total += mins

        tk.Frame(body, bg=TEXT_MID, height=2).pack(fill="x", pady=8)
        total_row = tk.Frame(body, bg=BG_TIMER)
        total_row.pack(fill="x")
        tk.Label(total_row, text="total grind time 💪:", font=("Courier New", 16, "bold"),
                 bg=BG_TIMER).pack(side="left")
        tk.Label(total_row, text=f"{total} min", font=("Courier New", 16, "bold"),
                 bg=BG_TIMER, fg="#6c5ce7").pack(side="right")

    back_btn(f).pack(pady=40)
    return f


# ─────────────────────────────────────────────
#  TIMER THREAD
# ─────────────────────────────────────────────
def timer_thread(subject, study_mins, break_mins):
    secs = study_mins * 60
    while secs:
        m, s = divmod(secs, 60)
        timer_label.config(text=f"📖 studying: {m:02d}:{s:02d}")
        time.sleep(1)
        secs -= 1
    winsound.Beep(1200, 400)
    winsound.Beep(1200, 400)
    study_log[subject] = study_log.get(subject, 0) + study_mins

    if break_mins > 0:
        secs = break_mins * 60
        while secs:
            m, s = divmod(secs, 60)
            timer_label.config(text=f"😴 break time: {m:02d}:{s:02d}")
            time.sleep(1)
            secs -= 1
        winsound.Beep(800, 400)
        winsound.Beep(800, 400)

    timer_label.config(text="🎉 timer done!! good job bestie")


# ─────────────────────────────────────────────
#  CLOCK
# ─────────────────────────────────────────────
def update_clock():
    t = time.strftime("%I:%M:%S %p")
    d = time.strftime("%A, %B %d")
    clock_label.config(text=f"📅 {d}   🕐 {t}")
    root.after(1000, update_clock)


# ─────────────────────────────────────────────
#  PAGE BUILDER REGISTRY
# ─────────────────────────────────────────────
PAGE_BUILDERS = {
    "add_expense":    build_add_expense,
    "view_expenses":  build_view_expenses,
    "add_task":       build_add_task,
    "mark_task_done": build_mark_task_done,
    "view_tasks":     build_view_tasks,
    "start_timer":    build_start_timer,
    "view_study_log": build_view_study_log,
}

# ─────────────────────────────────────────────
#  BOOTSTRAP
# ─────────────────────────────────────────────
clock_label = None
timer_label = None

main_frame = build_main(container)
main_frame.grid(row=0, column=0, sticky="nsew")
frames["main"] = main_frame

update_clock()
root.mainloop()