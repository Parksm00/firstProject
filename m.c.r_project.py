import tkinter as tk
import tkinter.font
import random
import time
from PIL import Image, ImageTk

window = tk.Tk()
window.title("M.C.R GAME")
window.geometry("1000x1000+0+5")


img = Image.open('backgroundImage.png')
bg = ImageTk.PhotoImage(img)

label_bg = tk.Label(window, image=bg)
label_bg.place(x=-2, y=-2)


label_title = tk.Label(window, text="산성비 게임", font=("궁서체", 24), bg='#2E2E30', fg='white')
label_title.pack(pady=10)


ent = tk.Entry(window, width=20)
ent.place(x=400, y=950)


font = tkinter.font.Font(family='Arial', size=10)
lab_point = tk.Label(window, text="", font=font, width=100, height=2)
lab_point.pack(pady=10)


canvas_width = 200
canvas_height = 20
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg='white')
canvas.place(x=800, y=10)


f = open("voca_list.txt", "r", encoding='UTF-8')
data = f.read()
f.close()
voca_list = data.split("\n")

vel = 5
rain_max = 20
lucky_num = 9
lucky_text = ""
stage = 1
point = 0
k = 0
rain_num = 0
lab_list = []
damage = 0
max_damage = 10  


ent = tkinter.Entry(window, width = 20)
def enter(event):
    global lab_list
    global point
    if ent.get() == lucky_text: 
        for lab in lab_list:
            lab.destroy()
        lab_list = []
        
        
    for lab in lab_list:
        if ent.get() == lab.cget("text") : 
            lab.destroy()
            lab_list.remove(lab)
            point+=1
            break
    ent.delete(0, len(ent.get()))

ent.bind("<Return>", enter)
ent.place(x = 400, y = 950)


def draw_health_bar():
    global damage, max_damage
    
    
    canvas.delete("health_bar")
    
    
    health_percent = (max_damage - damage) / max_damage
    bar_width = int(canvas_width * health_percent)
    canvas.create_rectangle(0, 0, bar_width, canvas_height, fill='green', tags="health_bar")
    canvas.create_rectangle(0, 0, canvas_width, canvas_height, outline='black')
    
    
    canvas.create_text(canvas_width // 2, canvas_height // 2, text=f"체력: {max_damage - damage}/{max_damage}", fill='black')


while True:
    k += 1
    vel = 3 + stage * 2
    
    
    if k % 50 == 25 and rain_num < rain_max:
        random_index = random.randrange(len(voca_list))
        lab_text = voca_list[random_index]
        lab = tk.Label(window, text=lab_text, font=font)
        if rain_num == lucky_num:
            lab.config(fg='blue')
            lucky_text = lab_text
        pos_x = random.randrange(0, 900)
        pos_y = 100
        lab.place(x=pos_x, y=pos_y)
        rain_num += 1
        lab_list.append(lab)

    
    for lab in lab_list:
        pos_x = int(lab.place_info()['x'])
        pos_y = int(lab.place_info()['y'])
        pos_y += vel
        lab.place(x=pos_x, y=pos_y)

    
    for lab in lab_list:
        pos_y = int(lab.place_info()['y'])
        if pos_y >= 900:
            lab.destroy()
            lab_list.remove(lab)
            damage += 1
            break

    
    if damage >= max_damage:
        for wg in window.place_slaves():
            wg.destroy()
        lab_end = tk.Label(window, text=f'게임종료! {stage}단계 {point}점까지 도달하였습니다.')
        lab_end.place(x=450, y=450)
        break
    elif rain_num == rain_max and len(lab_list) == 0:
        lab_go = tk.Label(window, text=f"{stage}단계 통과, 1초 후 자동으로 다음 단계 시작")
        lab_go.place(x=450, y=450)
        window.update()
        time.sleep(1)
        lab_go.destroy()
        k = 0
        lucky_text = ""
        stage += 1
        rain_num = 0

    
    lab_point.config(text=f"점수 : {point}\t\t\t{stage}단계\t\t\t목숨 : {max_damage - damage}")
    
    
    draw_health_bar()
    
    
    window.update()
    time.sleep(0.03)

window.mainloop()