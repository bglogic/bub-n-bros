from __future__ import generators
import os, math, random
import images, gamesrv
from images import ActiveSprite
from boards import CELL, HALFCELL, bget
from mnstrmap import GreenAndBlue, Ghost
from bonuses import Bonus

LocalDir = os.path.basename(os.path.dirname(__file__))


localmap = {
    ('pac-lg', -1,0) :  ('image1.ppm', ( 0,  0, 32, 32)),
    ('pac-sm', -1,0) :  ('image1.ppm', (32,  0, 32, 32)),
    ('pac-lg', 0,-1) :  ('image1.ppm', ( 0, 32, 32, 32)),
    ('pac-sm', 0,-1) :  ('image1.ppm', (32, 32, 32, 32)),
    ('pac-lg',  1,0) :  ('image1.ppm', ( 0, 64, 32, 32)),
    ('pac-sm',  1,0) :  ('image1.ppm', (32, 64, 32, 32)),
    ('pac-lg',  0,1) :  ('image1.ppm', ( 0, 96, 32, 32)),
    ('pac-sm',  0,1) :  ('image1.ppm', (32, 96, 32, 32)),
    'black'          :  ('image2.ppm', ( 0,  0, 32, 32)),
    'pac-dot'        :  ('image2.ppm', ( 0,  32, 8,  8)),
    }

music = gamesrv.getmusic(os.path.join(LocalDir, 'music.wav'))


class PacSprite(ActiveSprite):

    def __init__(self, ico, x, y):
        import boards
        if y < -2*CELL:
            y = -2*CELL
        elif y > boards.bheight:
            y = boards.bheight
        x = (x+HALFCELL) & -CELL
        y = (y+HALFCELL) & -CELL
        ActiveSprite.__init__(self, ico, x, y)
        self.wannadx = self.wannady = 0

    def moving(self):
        import boards
        dx = dy = 0
        was_clear = 0
        while 1:
            if self.wannadx != dx or self.wannady != dy:
                if ((self.wannadx and not (self.y % CELL)) or
                    (self.wannady and not (self.x % CELL))):
                    dx = self.wannadx
                    dy = self.wannady
                    self.resetimages(dx, dy)

            frontx = self.x+CELL+dx*(CELL+1)
            fronty = self.y+CELL+dy*(CELL+1)
            clear = (bget((frontx+dy)//CELL, (fronty-dx)//CELL) == ' ' and
                     bget((frontx-dy)//CELL, (fronty+dx)//CELL) == ' ')
            if clear:
                blocked = 0
            else:
                blocked = (was_clear or (self.x<=2*CELL and dx<0) or
                           (self.x>=boards.bwidth-4*CELL and dx>0))
            if blocked:
                self.lastmove = None
            else:
                self.lastmove = dx, dy
                self.step(2*dx, 2*dy)
                self.vertical_warp()
                was_clear = clear
            yield None


class Pac(PacSprite):

    def __init__(self, pacman, bubber, x, y):
        ico = GreenAndBlue.normal_bubbles[bubber.pn][1]
        PacSprite.__init__(self, images.sprget(('eyes', 0, 0)), x, y)
        self.bubble = ActiveSprite(images.sprget(ico), x, y)
        self.bubber = bubber
        self.pacman = pacman
        self.ready = 0
        self.gen.append(self.playing())
        self.pacman.pacs.append(self)

    def resetimages(self, dx, dy):
        self.ready = 1
        self.setimages(self.cyclic([('pac-lg', dx, dy),
                                    'black',
                                    ('pac-sm', dx, dy)], 5))
    
    def to_front(self):
        self.bubble.to_front()
        ActiveSprite.to_front(self)

    def kill(self):
        from bubbles import Bubble
        self.play(images.Snd.Pop)
        self.bubble.gen = [self.bubble.die(Bubble.exploding_bubbles)]
        try:
            self.bubber.dragons.remove(self)
        except ValueError:
            pass
        try:
            self.pacman.pacs.remove(self)
        except ValueError:
            pass
        ActiveSprite.kill(self)

    def playing(self):
        bubber = self.bubber
        for t in self.moving():
            if self.pacman.ready:
                d = [(bubber.key_left, -1, 0),
                     (bubber.key_right, 1, 0),
                     (bubber.key_jump,  0,-1),
                     (bubber.key_fire,  0, 1)]
                d.sort()
                if d[-1][0] > d[-2][0]:
                    self.wannadx, self.wannady = d[-1][1:]

            self.bubble.move(self.x, self.y)
            yield None

            if self.ready:
                touching = images.touching(self.x+CELL-3, self.y+CELL-3, 6, 6)
                touching.reverse()
                for s in touching:
                    if isinstance(s, Bonus):
                        s.touched(self)
                    elif isinstance(s, PacGhost):
                        self.kill()
                        return


class PacGhost(PacSprite):
    
    def __init__(self, pacman, x, y):
        left = random.random() < 0.5
        if left:
            ico = Ghost.left[0]
        else:
            ico = Ghost.right[0]
        PacSprite.__init__(self, images.sprget(ico), x, y)
        self.pacman = pacman
        self.gen.append(self.waiting())
        if left:
            self.wannadx = -1
        else:
            self.wannadx = 1
        self.resetimages(self.wannadx, self.wannady)

    def resetimages(self, dx, dy):
        if dx > 0:
            self.setimages(self.cyclic(Ghost.right, 3))
        elif dx < 0:
            self.setimages(self.cyclic(Ghost.left, 3))
        #else: don't change image

    def waiting(self, delay=45):
        while not self.pacman.ready:
            yield None
        for i in range(delay):
            yield None
        self.gen.append(self.walking())

    def walking(self):
        round = 0
        self.touchable = 1
        lastmove_x = 0
        for t in self.moving():
            if random.random() < 0.1:
                lastmove_x = self.wannadx
            if self.lastmove is None and random.random() < 0.75:
                round = 0  # try to move again immediately
            if self.lastmove is None or random.random() < 0.01:
                dragons = self.pacman.pacs or images.ActiveSprites
                distances = [(abs(dragon.x-self.x)+abs(dragon.y-self.y),
                              dragon) for dragon in dragons]
                distance, dragon = min(distances)
                if lastmove_x:
                    self.wannadx = 0
                    if (dragon.y < self.y) ^ (random.random() < 0.3):
                        self.wannady = -1
                    else:
                        self.wannady = 1
                else:
                    self.wannady = 0
                    if (dragon.x < self.x) ^ (random.random() < 0.3):
                        self.wannadx = -1
                    else:
                        self.wannadx = 1
            else:
                lastmove_x = self.lastmove[0]
##                    for i in range(10):
##                        dragon = random.choice(dragons)
##                        dx = dragon.x - self.x
##                        dy = dragon.y - self.y
##                        if dx or dy:
##                            dist = math.sqrt(dx*dx+dy*dy)
##                            dx /= dist
##                            dy /= dist
##                        wx, wy = random.choice([(-1,0), (1,0), (0,-1), (0,1)])
##                        ex = wx-dx
##                        ey = wy-dy
##                        if ex*ex + ey*ey < random.random()*3.14:
##                            break
##                    self.wannadx = wx
##                    self.wannady = wy
            if round == 0:    # go just a bit faster than the players
                round = 6
            else:
                round -= 1
                yield None


class FruitBonus(Bonus):
    pass


class Pacman:
    
    def bgen(self, limittime = 20.1): # 0:20
        import boards
        from player import BubPlayer

        self.ready = 0
        monsters = BubPlayer.MonsterList[:]
        random.shuffle(monsters)
        keep = len([p for p in BubPlayer.PlayerList if p.isplaying()])
        monsters = monsters[:2 + keep//2]
        for d in monsters:
            PacGhost(self, d.x, d.y)

        for t in boards.exit_board(0, music=[music]*3):
            yield t
        for t in curboard.clean_gen_state():
            yield t

        tc = boards.TimeCounter(limittime)
        self.dots = []
        self.joined = {}
        self.pacs = []
        finish = 0
        for t in self.frame():
            t = boards.normal_frame()
            self.build_pacs()
            yield t
            if len(self.pacs) == 0:
                finish += 1
                if finish == 20:
                    break
            else:
                finish = 0
            tc.update(t)
            if tc.time == 0.0:
                break

        tc.restore()
        self.ready = 0
        results = {}
        for b in self.dots:
            for d in b.taken_by:
                bubber = d.bubber
                results[bubber] = results.get(bubber, 0) + 1
        for t in boards.result_ranking(results, len(self.dots)):
            self.remove_pacs()
            yield t
        for s in images.ActiveSprites[:]:
            if isinstance(s, Bonus):
                s.kill()

    def frame(self):
        import boards
        from bonuses import Fruits
        for t in self.digwalls():
            yield t

        def anywall(x1,y1,x2,y2):
            for tx in range(x1, x2):
                for ty in range(y1, y2):
                    if bget(tx, ty) == '#':
                        return 1
            return 0

        dots = self.dots
        ico = images.sprget('pac-dot')
        for x in range(boards.width):
            for y in range(boards.height):
                if not anywall(x, y, x+2, y+2):
                    if anywall(x-1, y-1, x+3, y+3):
                        b = Bonus((x+1)*CELL - ico.w//2,
                                  (y+1)*CELL - ico.h//2,
                                  'pac-dot', points=-100, falling=0)
                        b.sound = 'Extra'
                        b.timeout = 0
                        dots.append(b)
            
            for s in images.ActiveSprites:
                if isinstance(s, PacGhost):
                    s.to_front()
            yield None

        self.ready = 1

        for i in range(len([s for s in images.ActiveSprites
                              if isinstance(s, PacGhost)])):
            for j in range(32):
                yield None
            for j in range(100):
                x = random.randrange(4, boards.width-6)
                y = random.randrange(3, boards.height-5)
                if not anywall(x-2, y-2, x+4, y+4):
                    nimage, points = random.choice(Fruits.Fruits)
                    points += 650   # boost to the range 750-1000
                    b = FruitBonus(x*CELL, y*CELL,
                                   nimage, points, falling=0)
                    b.timeout = 0
                    break
        
        while dots:
            dots = [b for b in dots if b.alive]
            yield None

    def build_pacs(self):
        from player import BubPlayer
        for p in BubPlayer.PlayerList:
            dragons = [d for d in p.dragons if not isinstance(d, Pac)]
            if (dragons and len(p.dragons) == len(dragons) and
                p not in self.joined):
                dragon = random.choice(dragons)
                pac = Pac(self, p, dragon.x, dragon.y)
                p.dragons.append(pac)
                p.emotic(dragon, 4)
                self.joined[p] = 1
            for d in dragons:
                d.kill()

    def remove_pacs(self):
        from player import Dragon
        killclasses = (Pac, FruitBonus, Dragon)
        for s in images.ActiveSprites[:]:
            if isinstance(s, killclasses):
                s.kill()

    def digwalls(self):
        import boards
        holes = {}
        for x in range(2, boards.width-2):
            y = boards.height-1
            if bget(x, 0) == '#' or bget(x, y) == '#':
                if bget(x, 0) == ' ': curboard.putwall(x, 0)
                if bget(x, y) == ' ': curboard.putwall(x, y)
            curboard.reorder_walls()
            for y in range(1, boards.height-1):
                if bget(x, y) == ' ':
                    holes[x, y] = 0
            if x % 7 == 0:
                yield None

        def rdig(x1,y1,x2,y2, holes=holes):
            for x in range(x1,x2):
                for y in range(y1,y2):
                    if bget(x, y) == '#':
                        curboard.killwall(x, y)
                    holes.setdefault((x, y), 0)
            fill = []
            for x in range(x1,x2-1):
                for y in range(y1,y2-1):
                    fill.append((x, y))
            for x, y in fill:
                if ((x, y) in holes and
                    (x, y+1) in holes and
                    (x+1, y) in holes and
                    (x+1, y+1) in holes):
                    if (holes[x, y] == 0 or
                        holes[x, y+1] == 0 or
                        holes[x+1, y] == 0 or
                        holes[x+1, y+1] == 0):
                        
                        holes[x, y] = 1
                        holes[x, y+1] = 1
                        holes[x+1, y] = 1
                        holes[x+1, y+1] = 1
                        fill.append((x+1,y))
                        fill.append((x-1,y))
                        fill.append((x,y+1))
                        fill.append((x,y-1))

        def kcount(x1,y1,x2,y2):
            total = 0
            for x in range(x1,x2):
                for y in range(y1,y2):
                    if bget(x, y) == '#':
                        total += 1
            return total

        def joined(x1,y1,x2,y2, holes=holes, boards=boards):
            if x1<2 or y1<1 or x2>boards.width-2 or y2>boards.height-1:
                return -1
            accum1 = accum2 = 0
            for x in range(x1,x2):
                if holes.get((x,y1-1)):
                    accum1 += 1
                    if accum1 == 2:
                        return 1
                else:
                    accum1 = 0
                if holes.get((x,y2)):
                    accum2 += 1
                    if accum2 == 2:
                        return 1
                else:
                    accum2 = 0
            accum1 = accum2 = 0
            for y in range(y1,y2):
                if holes.get((x1-1,y)):
                    accum1 += 1
                    if accum1 == 2:
                        return 1
                else:
                    accum1 = 0
                if holes.get((x2,y)):
                    accum2 += 1
                    if accum2 == 2:
                        return 1
                else:
                    accum2 = 0
            return 0

        startx = random.randrange(2, boards.width-4)
        starty = random.randrange(0, boards.height-2)
        rdig(startx, starty, startx+2, starty+1)
        yield None

        holeslist = holes.keys()
        random.shuffle(holeslist)
        dlist = [
            (0,0,1,0, 0,-1),   (0,0,1,0, 0,0),   # right
            (0,0,0,1, -1,0),   (0,0,0,1, 0,0),   # bottom
            (-1,0,0,0, -1,-1), (-1,0,0,0, -1,0), # left
            (0,-1,0,0, -1,-1), (0,-1,0,0, 0,-1), # top
            ]
        for x, y in holeslist:
            if holes[x, y] != 0:
                continue
            choices = []
            for dx1, dy1, dx2, dy2, dx, dy in dlist:
                x1 = x + dx
                y1 = y + dy
                x2 = x1 + 2
                y2 = y1 + 2
                count = 999999
                while 1:
                    result = joined(x1,y1,x2,y2)
                    if result == 1:
                        count = kcount(x1,y1,x2,y2)
                        break
                    if result == -1:
                        x1 -= dx1
                        y1 -= dy1
                        x2 -= dx2
                        y2 -= dy2
                        break
                    x1 += dx1
                    y1 += dy1
                    x2 += dx2
                    y2 += dy2
                    count += 1
                if count != 999999:
                    choices.append((count, x1,y1,x2,y2))
            count, x1,y1,x2,y2 = min(choices)
            rdig(x1,y1,x2,y2)
            yield None


def run():
    global curboard
    import boards
    from boards import curboard
    
    for key, (filename, rect) in localmap.items():
        filename = os.path.join(LocalDir, filename)
        images.sprmap[key] = (filename, rect)

    boards.replace_boardgen(Pacman().bgen())