from PIL import Image, ImageFont, ImageDraw, ImageColor
import pygame as pg
import os

pg.init()

def text_to_image(text: str, size: (int, int), font_filepath: str, font_size: int, color: (int, int, int), font_align="center"):
    font = ImageFont.truetype(font_filepath, size=font_size)
    img = Image.new("RGBA", (size[0], size[1]))
    draw = ImageDraw.Draw(img)
    draw_point = (0, 0)
    draw.multiline_text(draw_point, text, font=font, fill=color, align=font_align)
    img.save("cache/text.png")
    return pg.image.load("cache/text.png")

class cfg:
    icon_size = (128, 128)
    icon_table = (3, 3)
    panel_sizey = 50

class res:
    wallpaper = pg.image.load("resources/wallpaper.jpeg")
    font = "resources/font/Montserrat-Regular.ttf"

class App:
    def __init__(self, name:str, icon_path:str, onclick:str):
        self.name = name
        icon = pg.image.load(icon_path)
        self.icon = pg.transform.scale(icon, (cfg.icon_size[0], cfg.icon_size[1]))
        self.text = name
        self.onclick = onclick

size = (1920, 720)
win = pg.display.set_mode(size, pg.FULLSCREEN)

apps = []
for i in range(cfg.icon_table[0]*cfg.icon_table[1]):
    apps.append(App(f"sets {i}", "resources/apps/settings.svg", onclick=f"termux-toast \"sets {i}\""))

def run():
    global size, win, res, apps, cfg
    
    time = (2, 57)
    panel_down = False
    panel_moved = 0
    
    while True:
        cfg.panel_sizey += 5
        time = (time[0], time[1]+1)
	
        if time[1] >= 60: time = (time[0]+1, 0)
        if time[0] >= 24: time = (0, 0)
        
        sx, sy = win.get_size()
        size = (sx, sy)
        
        ### Wallpaper
        
        win.fill((0, 0, 0))
        win.blit(res.wallpaper, (0, 0))
        
        ### PANEL
        
        pg.draw.rect(win, (15, 15, 15), (0, 0, sx, cfg.panel_sizey))
        
        if len(str(time[1])) == 1: tstr = f"{time[0]}:0{time[1]}"
        else:                      tstr = f"{time[0]}:{time[1]}"
        text = text_to_image(tstr, (10*5, 20*2), res.font, 20, (255, 255, 255))#, font_align="right")
        win.blit(text, (sx-10*5-(cfg.panel_sizey/2-10/2), cfg.panel_sizey/2-15))
        
        ### APP ICONS
        
        total_icon_width = cfg.icon_table[0]-1 * cfg.icon_size[0]
        total_icon_height = cfg.icon_table[1]-1 * cfg.icon_size[1]
        
        margin_x = (size[0] - cfg.icon_size[0]-1) / (cfg.icon_table[0])
        margin_y = (size[1] - cfg.panel_sizey - cfg.icon_size[1]-1) / (cfg.icon_table[1])
        
        x = 0
        y = 0
        for i in range(len(apps)):
            app = apps[i]
            win.blit(app.icon, (margin_x*x+cfg.icon_size[0], cfg.panel_sizey+margin_y*y+cfg.icon_size[1]))
            text = text_to_image(app.name, (cfg.icon_size[0], 20*2), res.font, 20, (255, 255, 255))
            win.blit(text, (margin_x*x+cfg.icon_size[0], cfg.panel_sizey+margin_y*y+cfg.icon_size[1]*2+5))
            app.pos = (int(margin_x*x+cfg.icon_size[0]), int(cfg.panel_sizey+margin_y*y+cfg.icon_size[1]))
            x += 1
            if x+1 > cfg.icon_table[0]:
                y += 1
                x = 0
        
        for event in pg.event.get():
            if event.type == pg.QUIT: return
            if event.type == pg.MOUSEBUTTONDOWN:
                print(event.pos)
                if event.pos[1] in range(cfg.panel_sizey-5, cfg.panel_sizey+5):
                    panel_down = True
                    print(":)")
                else:
                    for app in apps:
                        if event.pos[0] in range(app.pos[0], app.pos[0]+cfg.icon_size[0]):
                            if event.pos[1] in range(app.pos[1], app.pos[1]+cfg.icon_size[1]):
                                os.system(app.onclick)
            if event.type == pg.MOUSEMOTION:
                if panel_down == True:
                    cfg.panel_sizey = event.pos[1]
            if event.type == pg.MOUSEBUTTONDOWN:
                if panel_down:
                    panel_down = False
            if event.type == pg.WINDOWFOCUSLOST: pass
        
        pg.display.flip()
    
