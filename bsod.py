import tkinter as tk
import random
import time


# ============================================================
# CONFIGURATION
# ============================================================

BG = "#0078D4"
WHITE = "#FFFFFF"

REFERENCE_WIDTH = 1920
REFERENCE_HEIGHT = 1080

ESCAPE_HOLD_TIME = 5.0


# ============================================================
# WINDOW
# ============================================================

window = tk.Tk()

window.title("Windows Error")

window.attributes("-fullscreen", True)
window.configure(bg=BG)

window.config(cursor="none")


screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()


# ============================================================
# SCALING
# ============================================================

scale_x = screen_width / REFERENCE_WIDTH
scale_y = screen_height / REFERENCE_HEIGHT

scale = min(scale_x, scale_y)


def scaled(value):
    return max(1, int(value * scale))


# ============================================================
# MAIN CONTENT
# ============================================================

content = tk.Frame(
    window,
    bg=BG
)

content.place(
    relx=0.19,
    rely=0.145,
    relwidth=0.62,
    relheight=0.72
)


# ============================================================
# SAD FACE
# ============================================================

face = tk.Label(
    content,
    text=":(",
    bg=BG,
    fg=WHITE,
    font=("Segoe UI Light", scaled(100)),
    anchor="nw"
)

face.place(
    relx=0,
    rely=0,
    anchor="nw"
)


# ============================================================
# MAIN MESSAGE
# ============================================================

message = tk.Label(
    content,
    text=(
        "Your PC ran into a problem and needs to restart. We're\n"
        "just collecting some error info, and then we'll restart for\n"
        "you."
    ),
    bg=BG,
    fg=WHITE,
    font=("Segoe UI Light", scaled(27)),
    justify="left",
    anchor="nw"
)

message.place(
    relx=0,
    rely=0.25,
    anchor="nw"
)


# ============================================================
# PROGRESS
#
# Moved lower so "you." has plenty of space.
# ============================================================

progress = tk.Label(
    content,
    text="0% complete",
    bg=BG,
    fg=WHITE,
    font=("Segoe UI Light", scaled(23)),
    anchor="w"
)

progress.place(
    relx=0,
    rely=0.47,
    anchor="nw"
)


# ============================================================
# STATUS
# ============================================================

status = tk.Label(
    content,
    text="Collecting error information...",
    bg=BG,
    fg=WHITE,
    font=("Segoe UI Light", scaled(21)),
    anchor="w"
)

status.place(
    relx=0,
    rely=0.54,
    anchor="nw"
)


# ============================================================
# LOWER INFORMATION AREA
#
# QR CODE                STOP CODE INFORMATION
#
# Both begin at exactly the same vertical position.
# ============================================================

lower_area = tk.Frame(
    content,
    bg=BG
)

lower_area.place(
    relx=0,
    rely=0.66,
    relwidth=1.0,
    relheight=0.30,
    anchor="nw"
)


# ============================================================
# QR CODE
# ============================================================

QR_SIZE = 29

random.seed(1337)

qr_matrix = [
    [
        random.choice([0, 1])
        for _ in range(QR_SIZE)
    ]
    for _ in range(QR_SIZE)
]


def add_finder_pattern(matrix, x, y):

    for row in range(7):

        for col in range(7):

            if (
                row == 0
                or row == 6
                or col == 0
                or col == 6
                or (
                    2 <= row <= 4
                    and 2 <= col <= 4
                )
            ):
                matrix[y + row][x + col] = 1

            else:
                matrix[y + row][x + col] = 0


# Three QR finder patterns
add_finder_pattern(
    qr_matrix,
    0,
    0
)

add_finder_pattern(
    qr_matrix,
    QR_SIZE - 7,
    0
)

add_finder_pattern(
    qr_matrix,
    0,
    QR_SIZE - 7
)


# ============================================================
# QR DIMENSIONS
# ============================================================

QR_PIXEL = scaled(5)

QR_BORDER = scaled(12)

qr_size = (
    QR_SIZE * QR_PIXEL
    + QR_BORDER * 2
)


# ============================================================
# QR CANVAS
# ============================================================

qr_canvas = tk.Canvas(
    lower_area,
    width=qr_size,
    height=qr_size,
    bg=WHITE,
    highlightthickness=0,
    bd=0
)

qr_canvas.place(
    relx=0,
    rely=0,
    anchor="nw"
)


# ============================================================
# DRAW QR
#
# White background/border
# Windows blue modules
# ============================================================

for y in range(QR_SIZE):

    for x in range(QR_SIZE):

        if qr_matrix[y][x]:

            x1 = (
                QR_BORDER
                + x * QR_PIXEL
            )

            y1 = (
                QR_BORDER
                + y * QR_PIXEL
            )

            x2 = (
                QR_BORDER
                + (x + 1) * QR_PIXEL
            )

            y2 = (
                QR_BORDER
                + (y + 1) * QR_PIXEL
            )

            qr_canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=BG,
                outline=BG
            )


# ============================================================
# STOP CODE INFORMATION
#
# Starts at exactly the same Y position as QR.
# ============================================================

stopcode = tk.Label(
    lower_area,
    text=(
        "For more information about this issue and possible "
        "fixes, visit https://www.windows.com/stopcode\n\n"
        "If you call a support person, give them this info:\n"
        "Stop code: CRITICAL_PROCESS_DIED"
    ),
    bg=BG,
    fg=WHITE,
    font=("Segoe UI Light", scaled(14)),
    justify="left",
    anchor="nw",
    wraplength=scaled(620)
)

stopcode.place(
    relx=0.18,
    rely=0,
    anchor="nw"
)


# ============================================================
# PROGRESS ANIMATION
# ============================================================

progress_value = 0


def change_progress():

    global progress_value

    if progress_value >= 100:

        progress.config(
            text="100% complete"
        )

        status.config(
            text="Recovery complete."
        )

        return


    progress_value += 1

    progress.config(
        text=f"{progress_value}% complete"
    )


    # --------------------------------------------------------
    # STATUS CHANGES
    # --------------------------------------------------------

    if progress_value == 25:

        status.config(
            text="Collecting error information..."
        )

    elif progress_value == 40:

        status.config(
            text="Attempting automatic recovery..."
        )

    elif progress_value == 65:

        status.config(
            text="Checking system files..."
        )

    elif progress_value == 82:

        status.config(
            text="Verifying system integrity..."
        )

    elif progress_value == 95:

        status.config(
            text="Finalizing recovery..."
        )

    elif progress_value == 100:

        status.config(
            text="Recovery complete."
        )

        return


    # --------------------------------------------------------
    # VARIABLE DELAY
    # --------------------------------------------------------

    if progress_value < 20:

        delay = random.randint(
            100,
            500
        )

    elif progress_value < 40:

        delay = random.randint(
            200,
            800
        )

    elif progress_value < 70:

        delay = random.randint(
            400,
            1500
        )

    elif progress_value < 90:

        delay = random.randint(
            700,
            2500
        )

    else:

        delay = random.randint(
            1000,
            3500
        )


    # Occasional long pause
    if random.randint(1, 25) == 1:

        delay = random.randint(
            5000,
            9000
        )


    window.after(
        delay,
        change_progress
    )


# Start progress after two seconds
window.after(
    2000,
    change_progress
)


# ============================================================
# EMERGENCY ESCAPE
#
# Hold Escape for 5 seconds to close.
# ============================================================

escape_pressed_at = None


def escape_down(event=None):

    global escape_pressed_at

    if escape_pressed_at is None:

        escape_pressed_at = time.monotonic()

        check_escape()


def escape_up(event=None):

    global escape_pressed_at

    escape_pressed_at = None


def check_escape():

    global escape_pressed_at

    if escape_pressed_at is None:
        return


    elapsed = (
        time.monotonic()
        - escape_pressed_at
    )


    if elapsed >= ESCAPE_HOLD_TIME:

        window.destroy()

        return


    window.after(
        100,
        check_escape
    )


window.bind(
    "<KeyPress-Escape>",
    escape_down
)

window.bind(
    "<KeyRelease-Escape>",
    escape_up
)


# ============================================================
# START
# ============================================================

window.mainloop()