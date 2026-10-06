import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))
key_dic = {pg.K_UP:(0,-5),pg.K_DOWN:(0,+5),pg.K_LEFT:(-5,0),pg.K_RIGHT:(+5,0)}


def check_bound(rect: pg.Rect) -> tuple[bool,bool]:
    """
    引数：こうかとんRectか爆弾Rect
    戻り値：タプル(横方向判定結果, 縦方向判定結果)
    画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True,True
    if rect.left < 0 or rect.right > WIDTH:
        yoko = False
    if rect.top < 0 or rect.bottom > HEIGHT:
        tate = False
    return yoko, tate


def gameover(screen: pg.surface) -> None:
    gameover_img = pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(gameover_img,(0,0,0), gameover_img.get_rect())
    gameover_img.set_alpha(200)
    screen.blit(gameover_img,[0,0])
    fonto = pg.font.Font(None, 100)
    txt = fonto.render("Game Over", True, (225,225,225))
    screen.blit(txt,[390,280])
    kk_img_sad = pg.image.load("fig/8.png")
    screen.blit(kk_img_sad,[300,280])
    kk_img_sad2 = pg.image.load("fig/8.png")
    screen.blit(kk_img_sad2,[800,280])
    
    pg.display.update()
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []
    bb_accs = [a for a in range(1,11)]
    for r in range(1,11):
        bb_img = pg.Surface((20*r,20*r))  #surfaceを作成
        pg.draw.circle(bb_img,(225,0,0),(10*r,10*r),10*r)
        #爆弾作成
        bb_imgs.append(bb_img)  #リストに入れる
    return bb_img, bb_accs

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")   
    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_accs, bb_imgs = init_bb_imgs()
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_img.set_colorkey((0,0,0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)

    vx = +5
    vy = +5
    clock = pg.time.Clock()
    tmr = 0
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):  #重なっていたら終わり
            print("game over")
            gameover(screen)
            return
        
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
            
        for key, move in key_dic.items():
            if key_lst[key]:
                sum_mv[0] += move[0]  #横方向移動量
                sum_mv[1] += move[1]  #縦方向移動量
        
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  #どっかはみ出てる
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  #先ほどの動きをキャンセルする
        screen.blit(kk_img, kk_rct)

        lst_index = min(tmr//500, 9)
        avx = vx*bb_accs[lst_index]
        avy = vy*bb_accs[lst_index]
        bb_img = bb_imgs[lst_index]

        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height
       
        bb_rct.move_ip(avx,avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:   #yoko == falseと意味は一緒
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
