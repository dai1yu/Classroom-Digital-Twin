# -*- coding: utf-8 -*-
"""
课堂数字孪生可视化大屏
运行环境：Python 3.9+，pygame
安装依赖：pip install pygame
运行：python classroom_digital_twin.py

说明：
- 独立运行的 2.5D 数字孪生驾驶舱示例，无需外部模型或图片资源。
- 中央实训室采用程序化等距透视绘制，包含 HPY-RS03 恒佩优立式一体化实训控制台、
  按键面板、急停按钮、手轮、顶部三色信号灯、桌椅及监控摄像头。
- 底部按钮可交互：设备告警、一键巡检、视角复位、实训任务下发。
"""

import math
import random
import sys
import time
from datetime import datetime

import pygame

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1600, 900
FPS = 60
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("课堂数字孪生可视化平台 | 智能制造实训室")
CLOCK = pygame.time.Clock()

# Theme
BG = (3, 15, 29)
PANEL = (5, 27, 46)
PANEL2 = (7, 38, 59)
CYAN = (22, 218, 235)
CYAN_SOFT = (63, 173, 198)
BLUE = (31, 111, 190)
TEXT = (193, 233, 242)
MUTED = (94, 157, 176)
GREEN = (37, 232, 174)
YELLOW = (255, 184, 65)
RED = (255, 82, 92)
WHITE = (225, 248, 252)
GRID = (19, 74, 94)

FONT_CACHE = {}
def font(size, bold=False):
    key = (size, bold)
    if key not in FONT_CACHE:
        names = ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "Arial"]
        chosen = None
        for n in names:
            try:
                chosen = pygame.font.SysFont(n, size, bold=bold)
                break
            except Exception:
                pass
        FONT_CACHE[key] = chosen or pygame.font.Font(None, size)
    return FONT_CACHE[key]

def txt(surface, s, x, y, size=16, color=TEXT, bold=False, anchor="topleft"):
    im = font(size, bold).render(str(s), True, color)
    r = im.get_rect()
    setattr(r, anchor, (int(x), int(y)))
    surface.blit(im, r)
    return r

def line(surface, color, a, b, width=1):
    pygame.draw.line(surface, color, a, b, width)

def panel(surface, rect, title, subtitle=None):
    x, y, w, h = rect
    pygame.draw.rect(surface, (3, 23, 39), rect, border_radius=5)
    pygame.draw.rect(surface, (13, 102, 128), rect, 1, border_radius=5)
    # Corner accents
    line(surface, CYAN, (x, y+17), (x, y), 3)
    line(surface, CYAN, (x, y), (x+42, y), 3)
    line(surface, CYAN, (x+w-42, y), (x+w, y), 3)
    line(surface, CYAN, (x+w, y), (x+w, y+17), 3)
    txt(surface, title, x+16, y+12, 18, TEXT, True)
    if subtitle:
        txt(surface, subtitle, x+w-14, y+17, 9, CYAN_SOFT, False, "topright")
    line(surface, (17, 75, 94), (x+14, y+43), (x+w-14, y+43), 1)

def glow_dot(surface, x, y, color, radius=4):
    pygame.draw.circle(surface, (*color, 35), (int(x), int(y)), radius+6)
    pygame.draw.circle(surface, color, (int(x), int(y)), radius)

def draw_header(surface, w):
    pygame.draw.rect(surface, (3, 20, 34), (0, 0, w, 94))
    line(surface, (12, 106, 130), (0, 93), (w, 93), 1)
    txt(surface, "课堂数字孪生可视化平台", 28, 17, 29, (199, 247, 252), True)
    txt(surface, "CLASSROOM DIGITAL TWIN  /  INTELLIGENT MANUFACTURING TRAINING CENTER", 31, 56, 10, CYAN_SOFT)
    labels = ["实训总览", "设备管理", "数据分析", "视频监控"]
    start = max(560, w-650)
    for i, label in enumerate(labels):
        x = start+i*112
        pygame.draw.rect(surface, (5, 42, 62), (x, 30, 98, 35), 1, border_radius=3)
        txt(surface, label, x+49, 38, 13, CYAN if i == 0 else TEXT, True, "midtop")
    txt(surface, datetime.now().strftime("%Y/%m/%d  %H:%M:%S"), w-25, 42, 12, CYAN_SOFT, False, "midright")

def iso(x, y, z=0, cx=800, cy=465, scale=1.0):
    # Isometric projection
    return (cx+(x-y)*0.88*scale, cy+(x+y)*0.43*scale-z*scale)

def poly3(surface, pts, color, width=0, cx=800, cy=465, scale=1):
    p = [iso(x,y,z,cx,cy,scale) for x,y,z in pts]
    pygame.draw.polygon(surface, color, p, width)

def draw_room(surface, t, patrol=False, camera_shift=0):
    w, h = surface.get_size()
    # Main visualization viewport
    area = pygame.Rect(282, 104, w-564, h-218)
    pygame.draw.rect(surface, (3, 17, 29), area)
    old_clip = surface.get_clip()
    surface.set_clip(area)

    cx = area.centerx + camera_shift
    cy = area.centery + 45
    sc = min(area.w/1050, area.h/540)
    # distant wall and floor
    poly3(surface, [(-420,-210,0),(420,-210,0),(420,-210,210),(-420,-210,210)], (5,29,43), cx,cy,sc)
    poly3(surface, [(-420,-210,0),(420,-210,0),(420,300,0),(-420,300,0)], (24,47,57), cx,cy,sc)
    # wall panels / horizontal rails
    for z in [45, 105, 165]:
        a=iso(-420,-208,z,cx,cy,sc); b=iso(420,-208,z,cx,cy,sc)
        line(surface,(24,83,99),a,b,2)
    for x in range(-360,421,90):
        a=iso(x,-207,0,cx,cy,sc); b=iso(x,-207,205,cx,cy,sc)
        line(surface,(13,61,78),a,b,1)
    # ceiling beams and lights
    for x in [-350,-120,110,340]:
        a=iso(x,-205,215,cx,cy,sc); b=iso(x,210,215,cx,cy,sc)
        line(surface,(34,78,91),a,b,7)
    for x in [-250,0,250]:
        p=iso(x,-110,207,cx,cy,sc)
        pygame.draw.ellipse(surface,(38,104,125),(p[0]-27*sc,p[1]-5*sc,54*sc,10*sc))
        pygame.draw.ellipse(surface,(91,221,236),(p[0]-17*sc,p[1]-2*sc,34*sc,4*sc))
    # floor grid
    for x in range(-400,401,40):
        line(surface,(47,91,99),iso(x,-210,1,cx,cy,sc),iso(x,280,1,cx,cy,sc),1)
    for y in range(-200,281,40):
        line(surface,(47,91,99),iso(-400,y,1,cx,cy,sc),iso(400,y,1,cx,cy,sc),1)
    # safety lane markings
    for y in [-130, 165]:
        a=iso(-390,y,2,cx,cy,sc); b=iso(390,y,2,cx,cy,sc)
        line(surface,(221,185,49),a,b,max(2,int(3*sc)))
    for x in [-385,385]:
        line(surface,(221,185,49),iso(x,-150,2,cx,cy,sc),iso(x,180,2,cx,cy,sc),max(2,int(3*sc)))

    # CCTV camera fixtures
    for x,y in [(-330,-190),(330,-190)]:
        p=iso(x,y,190,cx,cy,sc)
        pygame.draw.circle(surface,(91,130,143),(int(p[0]),int(p[1])),int(7*sc))
        pygame.draw.rect(surface,(90,129,142),(p[0],p[1],22*sc,9*sc),border_radius=2)
        pygame.draw.polygon(surface,(25,56,73),[(p[0]+20*sc,p[1]),(p[0]+36*sc,p[1]+5*sc),(p[0]+20*sc,p[1]+10*sc)])

    # training consoles in two rows
    positions = [(-250,-70),(-85,-70),(80,-70),(245,-70),(-170,65),(35,65),(235,65)]
    for idx,(x,y) in enumerate(positions):
        draw_console(surface, x,y,cx,cy,sc,idx,t)
    # tables and chairs
    for x,y in [(-330,75),(330,80),(-300,-5),(315,-10)]:
        draw_table_chair(surface,x,y,cx,cy,sc)
    # instructor desk
    draw_instructor_desk(surface, -5, 180, cx,cy,sc)
    # floating subtle scanning beam
    scan_y = area.top + 110 + int((math.sin(t*0.65)+1)*0.5*(area.h-220))
    line(surface,(11,112,150),(area.left+12,scan_y),(area.right-12,scan_y),1)
    # viewport label
    txt(surface,"SMART MANUFACTURING LAB  /  3D LIVE VIEW",area.left+17,area.top+13,10,CYAN_SOFT,True)
    txt(surface,"7 个实训工位  ·  2 路监控  ·  在线仿真",area.right-18,area.top+13,10,MUTED,False,"topright")
    if patrol:
        p=iso(235,65,0,cx,cy,sc)
        pygame.draw.circle(surface,YELLOW,(int(p[0]),int(p[1]-26*sc)),int(8*sc),2)
    surface.set_clip(old_clip)
    pygame.draw.rect(surface,(14,91,113),area,1)

def draw_console(surface,x,y,cx,cy,sc,idx,t):
    # Body is an isometric cuboid
    ww,dd,hh=66,42,78
    poly3(surface,[(x-ww/2,y-dd/2,0),(x+ww/2,y-dd/2,0),(x+ww/2,y+dd/2,0),(x-ww/2,y+dd/2,0)],(13,30,39),0,cx,cy,sc)
    poly3(surface,[(x-ww/2,y-dd/2,0),(x+ww/2,y-dd/2,0),(x+ww/2,y-dd/2,hh),(x-ww/2,y-dd/2,hh)],(45,77,88),0,cx,cy,sc)
    poly3(surface,[(x+ww/2,y-dd/2,0),(x+ww/2,y+dd/2,0),(x+ww/2,y+dd/2,hh),(x+ww/2,y-dd/2,hh)],(20,47,61),0,cx,cy,sc)
    poly3(surface,[(x-ww/2,y-dd/2,hh),(x+ww/2,y-dd/2,hh),(x+ww/2,y+dd/2,hh),(x-ww/2,y+dd/2,hh)],(56,100,113),0,cx,cy,sc)
    # front control panel
    p1=iso(x-23,y-dd/2-1,hh-30,cx,cy,sc); p2=iso(x+23,y-dd/2-1,hh-30,cx,cy,sc)
    p3=iso(x+23,y-dd/2-1,hh-5,cx,cy,sc); p4=iso(x-23,y-dd/2-1,hh-5,cx,cy,sc)
    pygame.draw.polygon(surface,(5,19,29),[p1,p2,p3,p4])
    # screen
    sp=iso(x,y-dd/2-2,hh-12,cx,cy,sc)
    pygame.draw.rect(surface,(5,38,56),(sp[0]-12*sc,sp[1]-7*sc,24*sc,13*sc),border_radius=2)
    pygame.draw.rect(surface,(28,174,202),(sp[0]-9*sc,sp[1]-5*sc,18*sc,8*sc),1)
    # buttons
    for j in range(3):
        bp=iso(x-15+j*13,y-dd/2-3,hh-43,cx,cy,sc)
        pygame.draw.circle(surface,[CYAN_SOFT,GREEN,YELLOW][j],(int(bp[0]),int(bp[1])),max(2,int(2.7*sc)))
    # emergency stop button, handwheel
    ep=iso(x+18,y-dd/2-4,hh-43,cx,cy,sc)
    pygame.draw.circle(surface,(90,19,24),(int(ep[0]),int(ep[1])),max(4,int(6*sc)))
    pygame.draw.circle(surface,RED,(int(ep[0]),int(ep[1])),max(3,int(4*sc)))
    hp=iso(x+ww/2+3,y-5,hh-18,cx,cy,sc)
    pygame.draw.circle(surface,(13,22,29),(int(hp[0]),int(hp[1])),max(5,int(9*sc)),max(2,int(2*sc)))
    pygame.draw.circle(surface,(112,157,170),(int(hp[0]),int(hp[1])),max(3,int(5*sc)),1)
    # three-color stack light
    lp=iso(x-ww/2+5,y-dd/2,hh+15,cx,cy,sc)
    pygame.draw.line(surface,(115,151,163),(lp[0],lp[1]+3*sc),(lp[0],lp[1]-15*sc),max(1,int(2*sc)))
    for k,col in enumerate([(236,69,77),(255,190,62),(42,229,161)]):
        pygame.draw.circle(surface,col,(int(lp[0]),int(lp[1]-(k*5+4)*sc)),max(2,int(3.5*sc)))
    # front brand plate
    bp=iso(x,y-dd/2-2,hh-62,cx,cy,sc)
    if sc>.52:
        txt(surface,"HPY-RS03",bp[0],bp[1],max(7,int(8*sc)),(155,217,226),True,"center")
    # status base glow
    base=iso(x,y,1,cx,cy,sc)
    pygame.draw.ellipse(surface,(8,119,150),(base[0]-25*sc,base[1]-5*sc,50*sc,10*sc),1)

def draw_table_chair(surface,x,y,cx,cy,sc):
    poly3(surface,[(x-30,y-18,38),(x+30,y-18,38),(x+30,y+18,38),(x-30,y+18,38)],(72,102,112),0,cx,cy,sc)
    for dx in [-23,23]:
        for dy in [-12,12]:
            a=iso(x+dx,y+dy,0,cx,cy,sc); b=iso(x+dx,y+dy,37,cx,cy,sc)
            line(surface,(52,86,99),a,b,max(2,int(3*sc)))
    # chair seat and back
    p=iso(x+42,y+4,20,cx,cy,sc)
    pygame.draw.ellipse(surface,(20,54,70),(p[0]-11*sc,p[1]-5*sc,22*sc,10*sc))
    pygame.draw.line(surface,(56,112,129),(p[0],p[1]),(p[0],p[1]-20*sc),max(2,int(3*sc)))
    pygame.draw.line(surface,(56,112,129),(p[0]-8*sc,p[1]-20*sc),(p[0]+8*sc,p[1]-20*sc),max(2,int(3*sc)))

def draw_instructor_desk(surface,x,y,cx,cy,sc):
    poly3(surface,[(x-50,y-20,35),(x+50,y-20,35),(x+50,y+20,35),(x-50,y+20,35)],(41,81,96),0,cx,cy,sc)
    p=iso(x,y-18,38,cx,cy,sc)
    pygame.draw.rect(surface,(5,20,31),(p[0]-20*sc,p[1]-13*sc,40*sc,24*sc),border_radius=2)
    pygame.draw.rect(surface,(16,131,164),(p[0]-17*sc,p[1]-10*sc,34*sc,17*sc),1)

def draw_left(surface, x, y, w, h, t):
    panel(surface,(x,y,w,h),"设备统计","DEVICE STATUS")
    # KPI cards
    cards=[("设备总数","07","台"),("在线设备","06","台"),("运行率","85.7","%"),("今日实训","128","人次")]
    cw=(w-42)//2
    for i,(lab,val,unit) in enumerate(cards):
        xx=x+14+(i%2)*(cw+10); yy=y+58+(i//2)*72
        pygame.draw.rect(surface,(7,42,59),(xx,yy,cw,60),1,border_radius=3)
        txt(surface,lab,xx+10,yy+8,11,MUTED)
        txt(surface,val,xx+10,yy+27,22,TEXT,True)
        txt(surface,unit,xx+cw-10,yy+37,10,CYAN_SOFT,False,"topright")
    txt(surface,"实训设备列表",x+16,y+214,12,CYAN,True)
    names=["HPY-RS03 实训台 01","HPY-RS03 实训台 02","HPY-RS03 实训台 03","HPY-RS03 实训台 04","HPY-RS03 实训台 05"]
    for i,n in enumerate(names):
        yy=y+239+i*37
        pygame.draw.rect(surface,(5,34,50),(x+13,yy,w-26,30),1,border_radius=2)
        glow_dot(surface,x+25,yy+15,GREEN if i!=3 else YELLOW,3)
        txt(surface,n,x+37,yy+8,10,TEXT)
        txt(surface,"运行中" if i!=3 else "待检查",x+w-22,yy+8,9,GREEN if i!=3 else YELLOW,False,"topright")
    txt(surface,"设备运行概况",x+16,y+h-83,11,CYAN,True)
    for i,(lab,v) in enumerate([("主轴负载",68),("加工进度",82),("网络状态",96)]):
        yy=y+h-60+i*17
        txt(surface,lab,x+16,yy,9,MUTED)
        pygame.draw.rect(surface,(23,63,77),(x+87,yy+2,w-128,6),border_radius=3)
        pygame.draw.rect(surface,CYAN,(x+87,yy+2,(w-128)*v/100,6),border_radius=3)
        txt(surface,f"{v}%",x+w-15,yy-2,9,CYAN_SOFT,False,"topright")

def draw_line_chart(surface, rect, t):
    x,y,w,h=rect
    panel(surface,rect,"实训负荷趋势","TRAINING LOAD")
    gx=x+35; gy=y+66; gw=w-55; gh=h-100
    for i in range(4):
        yy=gy+i*gh/3
        line(surface,(19,67,83),(gx,yy),(gx+gw,yy),1)
        txt(surface,str(100-i*25),x+8,yy-6,8,MUTED)
    pts=[]
    for i in range(28):
        v=52+18*math.sin(i*.42+t*.25)+8*math.sin(i*.91)
        pts.append((gx+i*gw/27,gy+gh*(1-v/100)))
    pygame.draw.lines(surface,CYAN,False,pts,2)
    for px,py in pts[::4]:
        pygame.draw.circle(surface,(139,247,255),(int(px),int(py)),3)
    for i,l in enumerate(["08:00","10:00","12:00","14:00","16:00"]):
        txt(surface,l,gx+i*gw/4,gy+gh+10,8,MUTED,False,"midtop")
    txt(surface,"当前负荷  72%",x+w-14,y+52,10,GREEN,True,"topright")

def draw_bar_chart(surface, rect, t):
    x,y,w,h=rect
    panel(surface,rect,"实训数据对比","DATA COMPARISON")
    gx=x+30; gy=y+70; gh=h-108; base=gy+gh
    vals=[72,86,64,93,78]
    labels=["工位01","工位02","工位03","工位04","工位05"]
    for i,v in enumerate(vals):
        bx=gx+20+i* ((w-70)/5)
        bh=gh*v/100
        pygame.draw.rect(surface,(13,59,80),(bx,base-bh,25,bh),border_radius=3)
        pygame.draw.rect(surface,CYAN,(bx,base-bh,25,3),border_radius=2)
        txt(surface,str(v),bx+12,base-bh-17,9,TEXT,True,"midtop")
        txt(surface,labels[i],bx+12,base+8,8,MUTED,False,"midtop")
    for j in range(3):
        yy=gy+j*gh/2
        line(surface,(18,61,78),(gx,yy),(x+w-13,yy),1)

def draw_video(surface, rect, t):
    x,y,w,h=rect
    panel(surface,rect,"视频监控","LIVE CAMERA 01")
    vx=x+12; vy=y+54; vw=w-24; vh=h-68
    pygame.draw.rect(surface,(3,12,20),(vx,vy,vw,vh))
    # stylized live camera view
    for i in range(7):
        xx=vx+i*vw/6
        line(surface,(14,47,61),(xx,vy),(xx,vy+vh),1)
    for i in range(4):
        yy=vy+i*vh/3
        line(surface,(14,47,61),(vx,yy),(vx+vw,yy),1)
    pygame.draw.polygon(surface,(15,42,54),[(vx+vw*.12,vy+vh*.72),(vx+vw*.88,vy+vh*.72),(vx+vw*.98,vy+vh),(vx+vw*.02,vy+vh)])
    # tiny console silhouettes
    for i in range(3):
        bx=vx+vw*(.2+i*.28); by=vy+vh*.55
        pygame.draw.rect(surface,(37,78,92),(bx,by, vw*.16,vh*.25))
        pygame.draw.rect(surface,(7,24,34),(bx+vw*.02,by+vh*.04,vw*.12,vh*.1))
    pygame.draw.circle(surface,RED,(vx+13,vy+13),4)
    txt(surface,"REC  00:18:32",vx+25,vy+7,9,(255,130,135))
    txt(surface,"CAM-01  实训区全景",vx+8,vy+vh-17,9,TEXT)

def draw_alerts(surface, rect, alerts, t):
    x,y,w,h=rect
    panel(surface,rect,"告警预警列表","ALARM CENTER")
    rows=[
        ("10:12:08","工位04 急停状态待确认",YELLOW),
        ("09:48:21","工位02 实训任务完成",GREEN),
        ("09:32:06","网络连接状态正常",GREEN),
        ("09:15:43","巡检任务已完成",CYAN_SOFT),
    ]
    if alerts:
        rows.insert(0,("实时告警","工位04 设备状态异常",RED))
    for i,(tm,msg,col) in enumerate(rows[:5]):
        yy=y+55+i*31
        glow_dot(surface,x+19,yy+10,col,3)
        txt(surface,tm,x+30,yy+2,9,MUTED)
        txt(surface,msg,x+91,yy+2,9,TEXT)
        if i==0 and alerts:
            pygame.draw.rect(surface,(94,28,36),(x+w-48,yy-2,37,17),border_radius=3)
            txt(surface,"告警",x+w-29,yy,8,(255,191,193),True,"midtop")

def draw_bottom(surface,w,h,buttons,toast,t):
    y=h-91
    # footer metric strip
    metrics=[("当前实训任务","智能制造基础实训  /  TASK-028"),("在线工位","06 / 07 台"),("今日实训人数","128 人次"),("设备综合健康度","96.8 %")]
    boxw=(w-48-3*9)/4
    for i,(a,b) in enumerate(metrics):
        x=18+i*(boxw+9)
        pygame.draw.rect(surface,(4,28,46),(x,y,boxw,43),1,border_radius=3)
        txt(surface,a,x+10,y+5,9,MUTED)
        txt(surface,b,x+10,y+21,12,CYAN if i==3 else TEXT,True)
    by=h-39
    labels=["设备告警","一键巡检","视角复位","实训任务下发"]
    bw=145; gap=12
    start=w-(bw*4+gap*3)-22
    for i,label in enumerate(labels):
        r=pygame.Rect(start+i*(bw+gap),by,bw,29)
        active=(i==0 and buttons["alert"]) or (i==1 and buttons["patrol"])
        pygame.draw.rect(surface,(9,66,91) if active else (5,37,57),r,border_radius=3)
        pygame.draw.rect(surface,CYAN if active else (19,113,139),r,1,border_radius=3)
        txt(surface,label,r.centerx,r.centery,11,TEXT,True,"center")
    if toast:
        tw=font(12).size(toast)[0]+28
        pygame.draw.rect(surface,(6,47,65),(w//2-tw//2,h-132,tw,28),border_radius=4)
        pygame.draw.rect(surface,CYAN,(w//2-tw//2,h-132,tw,28),1,border_radius=4)
        txt(surface,toast,w//2,h-126,11,TEXT,False,"midtop")

def main():
    global SCREEN
    t0=time.time()
    buttons={"alert":False,"patrol":False}
    toast="系统已连接：HPY-RS03 实训设备数据同步正常"
    toast_until=time.time()+3
    camera_shift=0
    last_patrol=0
    running=True
    while running:
        dt=CLOCK.tick(FPS)/1000
        t=time.time()-t0
        w,h=SCREEN.get_size()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            elif event.type==pygame.VIDEORESIZE:
                SCREEN=pygame.display.set_mode((max(1100,event.w),max(680,event.h)),pygame.RESIZABLE)
            elif event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                mx,my=event.pos
                by=h-39; bw=145; gap=12; start=w-(bw*4+gap*3)-22
                for i in range(4):
                    r=pygame.Rect(start+i*(bw+gap),by,bw,29)
                    if r.collidepoint(mx,my):
                        if i==0:
                            buttons["alert"]=not buttons["alert"]
                            toast="设备告警：已展开实时告警信息" if buttons["alert"] else "设备告警：告警面板恢复常态"
                        elif i==1:
                            buttons["patrol"]=True
                            last_patrol=time.time()
                            toast="一键巡检已启动：正在检查 7 个实训工位"
                        elif i==2:
                            camera_shift=0
                            toast="视角已复位：恢复实训室全景"
                        elif i==3:
                            toast="实训任务已下发：智能制造基础实训 TASK-029"
                        toast_until=time.time()+3.2
            elif event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                running=False
        if buttons["patrol"] and time.time()-last_patrol>4:
            buttons["patrol"]=False
        SCREEN.fill(BG)
        # subtle background grid
        for xx in range(0,w,40):
            line(SCREEN,(5,27,42),(xx,95),(xx,h),1)
        draw_header(SCREEN,w)
        draw_room(SCREEN,t,buttons["patrol"],camera_shift)
        left_x,left_w=16,248
        right_w=248
        right_x=w-right_w-16
        # Side panels sit over 3D viewport
        draw_left(SCREEN,left_x,112,left_w,int(h*.57),t)
        draw_line_chart(SCREEN,(left_x, h-274,left_w,156),t)
        draw_bar_chart(SCREEN,(right_x,112,right_w,205),t)
        draw_video(SCREEN,(right_x,328,right_w,190),t)
        draw_alerts(SCREEN,(right_x,528,right_w, min(205,h-640)),buttons["alert"],t)
        # central viewport title and subtle bottom vignette
        pygame.draw.rect(SCREEN,(4,20,33),(282,96,w-564,22))
        txt(SCREEN,"智能制造实训室三维场景",w//2,101,11,CYAN_SOFT,True,"midtop")
        draw_bottom(SCREEN,w,h,buttons,toast if time.time()<toast_until else "",t)
        pygame.display.flip()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
