import turtle
import time
import random

# SETUP LAYAR
screen = turtle.Screen()
screen.setup(600, 700)
screen.title("Love me not")
screen.tracer(0)  # bikin animasi smooth

pen = turtle.Turtle()
pen.hideturtle()
pen.penup()

# DAFTAR BACKGROUND
backgrounds = [
    "bg1.gif", "bg2.gif", "bg3.gif", "bg4.gif",
    "bg5.gif", "bg6.gif", "bg7.gif", "bg8.gif"
]

for bg in backgrounds:
    screen.addshape(bg)

# LIRIK
lyrics = [
    "Wake up in the morning",
    "everything's alright",
    "At the end of the story",
    "you're holdin' me tight",
    "I don't need to worry",
    "am I out of my mind?",
    "And, oh, it's hard to see you",
    "but I wish you were right here",
]


# DELAY TIAP LIRIK
delays = [1.5, 2, 2.5, 2.3, 1.8, 1.3, 2.0, 3.5]


# FUNGSI TAMPIL LIRIK 
def draw_lyric(text):
    colors = ["white", "lightyellow", "lavender", "mistyrose"]

    # shadow (bayangan teks)
    pen.goto(2, -52)
    pen.color("black")
    pen.write(text, align="center", font=("Calibri", 28, "bold"))

    # teks utama
    pen.goto(0, -50)
    pen.color(random.choice(colors))
    pen.write(text, align="center", font=("Calibri", 28, "bold"))

# =========================
# MAIN SLIDE
# =========================
for i in range(len(lyrics)):
    pen.clear()
    screen.bgpic(backgrounds[i])
    draw_lyric(lyrics[i])
    screen.update()
    time.sleep(delays[i])

screen.mainloop()