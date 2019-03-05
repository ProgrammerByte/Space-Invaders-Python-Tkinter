from tkinter import *
from random import randint
from tkinter import messagebox

#10 x 5 grid of aliens

class gamewindow():
    def __init__(s):
        s.root = Tk()
        s.root.title("Space Invaders")
        s.root.grid()

        s.root.bind("<KeyPress>", lambda event="<KeyPress>": gamewindow.keypress(event, s))
        s.root.bind("<KeyRelease>", lambda event="<KeyRelease>": gamewindow.keyrelease(event, s))

        s.canvas = Canvas(height = 1000, width = 1000, bg = "Black")
        s.canvas.grid()

        s.spriteindex = 0
        sprite1 = PhotoImage(file = "Sprite1.png")
        sprite2 = PhotoImage(file = "Sprite2.png")
        s.spritelist = [sprite1, sprite2]
        s.alienvertices = list()
        s.aliens = list()
        s.aliensprite = list()
        
        for i in range(8):
            s.aliens.append([])
            s.alienvertices.append([])
            s.aliensprite.append([])
            for x in range(5):
                s.aliens[i].append("")
                s.alienvertices[i].append(["","","",""])
                s.aliensprite[i].append("")

                xdistance = (100 * i) + 125
                ydistance = (60 * x) + 5
                
                s.alienvertices[i][x] = [xdistance, ydistance, xdistance + 50, ydistance + 50]
                s.aliens[i][x] = s.canvas.create_rectangle(s.alienvertices[i][x], fill = "Black")
                s.aliensprite[i][x] = s.canvas.create_image(xdistance + 45, ydistance + 25, image = s.spritelist[0])
                

        s.player = s.canvas.create_rectangle(450, 900, 550, 950, fill = "White")

        s.direction = "None"
        s.playerrecharge = "True"
        s.playershoot = "False"
        s.playerbullet = "None"
        s.change = "False"
        s.finished = "N"
        s.aliendirection = 5
        s.alienbullets = list()
        
        gamewindow.refresh(s)
        gamewindow.alienmove(s)



        s.root.mainloop()

    def playermove(s): #Deals with user input and the movement of bullets
        if s.direction == "Left" and s.playerposition[0] - 10 >= 0:
            s.canvas.move(s.player, -5, 0)
        elif s.direction == "Right" and s.playerposition[2] + 10 <= 1000:
            s.canvas.move(s.player, 5, 0)

        if s.playershoot == "True" and s.playerrecharge == "True" and s.playerbullet == "None":
            s.playerrecharge = "False"
            s.playerbullet = s.canvas.create_line(s.centerx, 900, s.centerx, 850, fill = "Red", width = 10)

        if s.playerbullet != "None":
            s.canvas.move(s.playerbullet, 0, -10)
            
            s.playerbulletposition = list(s.canvas.bbox(s.playerbullet))
            if s.playerbulletposition[1] <= 0:
                s.canvas.delete(s.playerbullet)
                s.playerbullet = "None"

            for z in range(2):
                tempz = z * 2
                i = 0
                while i < len(s.alienvertices):
                    x = 0
                    while x < len(s.alienvertices[i]):
                        
                        if s.alienvertices[i][x][0] <= s.playerbulletposition[tempz + 0] <= s.alienvertices[i][x][2] and s.alienvertices[i][x][1] <= s.playerbulletposition[tempz + 1] <= s.alienvertices[i][x][3]:
                            s.canvas.delete(s.aliensprite[i][x])
                            del s.aliensprite[i][x]
                            s.canvas.delete(s.aliens[i][x])
                            del s.alienvertices[i][x]
                            del s.aliens[i][x]
                            s.canvas.delete(s.playerbullet)
                            s.playerbullet = "None"
                        x += 1
                    i += 1

    def alienmove(s): #Everything related to alien movement and their bullets
        if s.finished == "N":
            currentdirection = s.aliendirection
            currentchange = s.change
            if s.spriteindex == 1:
                s.spriteindex = 0
            else:
                s.spriteindex = 1

            totalaliens = 0
            for i in range(len(s.aliens)):
                for x in range(len(s.aliens[i])):
                    if s.finished == "N":
                        totalaliens += 1

                        if s.alienvertices[i][x][1] >= 850:
                            s.finished = "Y"
                            messagebox.showinfo("GAME OVER", "You have lost!!!")
                        
                        if s.alienvertices[i][x][0] <= 5 and s.aliendirection == -5:
                            s.aliendirection = 5
                            s.change = "True"
                        elif s.alienvertices[i][x][2] >= 995 and s.aliendirection == 5:
                            s.aliendirection = -5
                            s.change = "True"

                        if currentchange == "True":
                            if s.change == "True":
                                s.change = "False"
                                
                            s.alienvertices[i][x][1] += 50
                            s.alienvertices[i][x][3] += 50
                            
                        s.alienvertices[i][x][0] += currentdirection
                        s.alienvertices[i][x][2] += currentdirection
                            
                        s.canvas.delete(s.aliens[i][x])
                        s.aliens[i][x] = s.canvas.create_rectangle(s.alienvertices[i][x], fill = "Black")

                        s.canvas.delete(s.aliensprite[i][x])
                        s.aliensprite[i][x] = s.canvas.create_image(int((s.alienvertices[i][x][0] + s.alienvertices[i][x][2]) / 2), int((s.alienvertices[i][x][1] + s.alienvertices[i][x][3]) / 2), image = s.spritelist[s.spriteindex])



                        chance = randint(1, 100)
                        if chance == 10:
                            s.alienbullets.append("")

                            centerx = int((s.alienvertices[i][x][0] + s.alienvertices[i][x][2]) / 2)
                            centery = int((s.alienvertices[i][x][1] + s.alienvertices[i][x][3]) / 3)
                            
                            s.alienbullets[len(s.alienbullets) - 1] = s.canvas.create_line(centerx, centery, centerx, centery + 50, fill = "Yellow", width = 10)

            if totalaliens == 0:
                s.finished = "Y"
                messagebox.showinfo("GAME OVER", "You have won!!!")

            time = int((totalaliens / 80) * 1000)
            s.root.after(time, gamewindow.alienmove, s)
        
    def refresh(s):
        if s.finished == "N":
            s.playerposition = list(s.canvas.bbox(s.player))
            s.centerx = int((s.playerposition[2] + s.playerposition[0]) / 2)

            gamewindow.playermove(s)
            
            for i in range(len(s.alienbullets)):
                if s.finished == "N":
                    vertices = list(s.canvas.bbox(s.alienbullets[i]))

                    for z in range(2):
                        tempz = z * 2
                        for x in range(len(s.playerposition)):
                            if s.finished == "N":
                                if s.playerposition[0] <= vertices[tempz + 0] <= s.playerposition[2] and s.playerposition[1] <= vertices[tempz + 1] <= s.playerposition[3]:
                                    s.finished = "Y"
                                    messagebox.showinfo("GAME OVER", "You have lost!!!")
                        
                s.canvas.move(s.alienbullets[i], 0, 5)


            s.root.after(10, gamewindow.refresh, s)
            
    def keypress(event, s):
        key = event.keysym
        if key == "a" or key == "A" or key == "Left":
            s.direction = "Left"
        elif key == "d" or key == "D" or key == "Right":
            s.direction = "Right"
        elif key == "space":
            s.playershoot = "True"

    def keyrelease(event, s):
        key = event.keysym
        if key == "a" or key == "A" or key == "Left" or key == "d" or key == "D" or key == "Right":
            s.direction = "None"
        elif key == "space":
            s.playershoot = "False"
            s.playerrecharge = "True"


if __name__ == "__main__":
    gamewindow()
    quit()
