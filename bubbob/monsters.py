from __future__ import generators
import random
import gamesrv
import images
import boards
from boards import *
from images import ActiveSprite
from mnstrmap import GreenAndBlue, Bonuses, Ghost
from player import BubPlayer
import bonuses


class Monster(ActiveSprite):
    touchable = 1
    special_prob = 0.2
    shootcls = None
    vx = 2
    vy = 0
    vdir = -1
    is_ghost = 0

    def __init__(self, mnstrdef, x=None, y=None, dir=None, in_list=None):
        self.mdef = mnstrdef
        self.ptag = None
        if dir is None: dir = mnstrdef.dir
        if x is None: x = mnstrdef.x*CELL
        if y is None: y = mnstrdef.y*CELL
        self.dir = dir
        ActiveSprite.__init__(self, images.sprget(self.imgrange()[0]), x, y)
        self.gen.append(self.waiting())
        self.in_list = in_list or BubPlayer.MonsterList
        self.in_list.append(self)
        self.no_shoot_before = 0
        #images.ActiveSprites.remove(self)

    def unlist(self):
        try:
            self.in_list.remove(self)
            return 1
        except ValueError:
            return 0

    def kill(self):
        self.unlist()
        ActiveSprite.kill(self)

    def tagdragon(self):
        dragons = [d for d in BubPlayer.DragonList
                   if not d.dcap['ring'] and not d.dcap['shield']]
        if dragons:
            return random.choice(dragons)
        else:
            return None

    def imgrange(self):
        if self.is_ghost:
            if self.dir > 0:
                return Ghost.right
            else:
                return Ghost.left
        elif self.angry:
            if self.dir > 0:
                return self.mdef.right_angry
            else:
                return self.mdef.left_angry
        else:
            if self.dir > 0:
                return self.mdef.right
            else:
                return self.mdef.left

    def resetimages(self, is_ghost=0):
        self.is_ghost = is_ghost
        if self.gen:
            self.setimages(self.cyclic(self.imgrange(), 3))
        else:  # frozen monster
            self.seticon(images.sprget(self.imgrange()[0]))

    def blocked(self):
        if self.dir < 0:
            x0 = (self.x-1)//CELL
        else:
            x0 = (self.x+1)//CELL + 2
        y0 = self.y // CELL + 1
        y1 = (self.y + CELL - 1) // CELL + 1
        return bget(x0,y0) == '#' or bget(x0,y1) == '#'

    def waiting(self, delay=20):
        for i in range(delay):
            yield None
        self.resetimages()
        self.gen.append(self.default_mode())

    def overlapping(self, chance=0.2):
        if random.random() < chance:
            for s in BubPlayer.MonsterList:
                if (abs(s.x-self.x) <= 6 and abs(s.y-self.y) < 6 and
                    #s.dir == self.dir and s.vdir == self.vdir and
                    s.vx == self.vx and s.vy == self.vy and s.angry == self.angry):
                    return s is not self
        return 0

    def walking(self):
        while onground(self.x, self.y):
            yield None
            if self.overlapping():
                yield None
            x1 = self.x
            if self.dir > 0:
                x1 += self.vx
            if (x1 % CELL) < self.vx and random.random() < self.special_prob:
                self.move((x1//CELL) * CELL, self.y)
                if self.special():
                    return
            if self.blocked():
                self.dir = -self.dir
                self.resetimages()
                continue
            self.step(self.vx*self.dir, 0)
        if self.seedragon():
            self.gen.append(self.hjumping())
        else:
            self.gen.append(self.falling())

    def seedragon(self, p=None):
        p = p or self.tagdragon()
        return p and abs(p.y - self.y) < 16 and self.dir*(p.x-self.x) > 0

    def special(self):
        p = self.tagdragon()
        if p is None:
            return 0
        if self.seedragon(p) and self.shoot():
            return 1
        if p.y < self.y-CELL:#and abs(p.x-self.x) < 2*(self.y-p.y):
            for testy in range(self.y-2*CELL, self.y-6*CELL, -CELL):
                if onground(self.x, testy):
                    if random.random() < 0.5:
                        ndir = self.dir
                    elif p.x < self.x:
                        ndir = -1
                    else:
                        ndir = 1
                    self.gen.append(self.vjumping(testy, ndir))
                    return 1
        return 0

    def shooting(self, pause):
        for i in range(pause):
            yield None
        self.shootcls(self)
        yield None
        self.gen.append(self.default_mode())

    def shoot(self, pause=10):
        if (self.shootcls is None or
            self.no_shoot_before > BubPlayer.FrameCounter):
            return 0
        else:
            self.gen.append(self.shooting(pause))
            self.no_shoot_before = BubPlayer.FrameCounter + 29
            return 1

    def falling(self):
        while not onground(self.x, self.y):
            yield None
            ny = self.y + 3
            if (ny % CELL) > CELL-2:
                ny = (ny//CELL+1)*CELL
            elif (ny % CELL) < 3:
                ny = (ny//CELL)*CELL
            if ny >= boards.bheight:
                ny -= boards.bheightmod
            self.move(self.x, ny)
        if hasattr(self, 'bubber'):
            nextgen = self.playing_monster
        else:
            nextgen = self.walking
        self.gen.append(nextgen())

    def hjumping(self):
        y0 = self.y
        vspeed = -2.2
        ny = y0-1
        while ny <= y0 and not self.blocked():
            self.move(self.x+2*self.dir, int(ny))
            yield None
            vspeed += 0.19
            ny = self.y + vspeed
        self.gen.append(self.default_mode())

    def vjumping(self, limity, ndir, bubber=None):
        self.setimages(None)
        if not bubber:
            yield None
            self.dir = -self.dir
            self.seticon(images.sprget(self.imgrange()[0]))
            for i in range(9):
                yield None
            self.dir = -self.dir
            self.seticon(images.sprget(self.imgrange()[0]))
            for i in range(4):
                yield None
            self.dir = ndir
        self.seticon(images.sprget(self.imgrange()[1]))
        for ny in range(self.y-4, limity-4, -4):
            if ny < -2*CELL:
                ny += boards.bheightmod
            self.move(self.x, ny)
            yield None
        if bubber:
            if bubber.key_left and bubber.key_left > bubber.key_right:
                dx = -1
            elif bubber.key_right:
                dx = 1
            else:
                dx = 0
            if dx:
                self.dir = dx
                self.resetimages()
                self.gen.append(self.hjumping())
                return
        self.resetimages()
        self.gen.append(self.default_mode())

    def regular(self):
        return self.still_playing() and self.touchable and not self.is_ghost

    def still_playing(self):
        return (self.in_list is BubPlayer.MonsterList and
                self in self.in_list)

    def touched(self, dragon):
        if self.gen:
            dragon.die()
            if self.is_ghost:
                self.gen = [self.default_mode()]
                self.resetimages()
        else:
            self.argh(getattr(self, 'poplist', None))  # frozen monster

    def in_bubble(self, bubble):
        self.untouchable()
        self.angry = 0
        bubble.move(self.x, self.y)
        bubble.to_front()
        self.to_front()
        img = self.mdef.jailed
        self.gen = [self.bubbling(bubble)]
        self.setimages(self.cyclic([img[1], img[2], img[1], img[0]], 4))

    def bubbling(self, bubble):
        counter = 0
        while not hasattr(bubble, 'poplist'):
            self.move(bubble.x, bubble.y)
            yield None
            counter += 1
            if counter == 50 and hasattr(self, 'bubber'):
                bubble.setimages(bubble.bubble_red())
        if bubble.poplist is None:
            self.touchable = 1
            self.angry = 1
            self.resetimages()
            self.gen.append(self.default_mode())
        else:
            previous_len = len(BubPlayer.MonsterList)
            self.argh(bubble.poplist)
            dragon = bubble.poplist[0]
            if dragon is not None:
                if previous_len and not BubPlayer.MonsterList:
                    points = 990
                else:
                    points = 90
                dragon.bubber.givepoints(points)

    def argh(self, poplist=None, onplace=0):
        if self not in self.in_list:
            return
        if not poplist:
            poplist = [None]
        poplist.append(self)
        level = len(poplist) - 2
        bonuses.BonusMaker(self.x, self.y, self.mdef.dead, onplace=onplace,
                           outcome=(bonuses.MonsterBonus, level))
        self.kill()

    def freeze(self, poplist):
        if self.regular():
            self.gen = []
            self.poplist = poplist

    def flying(self):
        blocked = 0
        while 1:
            if self.overlapping():
                yield None
            nx = self.x + self.vx*self.dir
            ny = self.y + self.vy*self.vdir
            if ny >= boards.bheight:
                ny -= boards.bheightmod
            elif ny < -2*CELL:
                ny += boards.bheightmod
            if self.dir < 0:
                x0 = nx // CELL
            else:
                x0 = (nx+self.ico.w-1) // CELL
            for y in range(self.y // CELL, (self.y+self.ico.h-1) // CELL + 1):
                if bget(x0, y) == '#':
                    self.dir = -self.dir
                    nx = self.x
                    self.resetimages()
                    break
            if self.vdir < 0:
                y0 = ny // CELL
            else:
                y0 = (ny+self.ico.h-1) // CELL
            for x in range(nx // CELL, (nx+self.ico.w-1) // CELL + 1):
                if bget(x, y0) == '#':
                    self.vdir = -self.vdir
                    ny = self.y
                    self.resetimages()
                    break
            if nx == self.x and ny == self.y:
                if blocked:
                    # blocked! go up
                    ny -= abs(self.vdir)
                    if ny < -2*CELL:
                        ny += boards.bheightmod
                else:
                    blocked = 1
            else:
                blocked = 0
            self.move(nx, ny)
            yield None

    def becoming_monster(self, saved_caps):
        for i in range(5):
            ico = self.ico
            self.seticon(self.bubber.icons[11, self.dir])
            yield None
            yield None
            self.seticon(ico)
            yield None
            yield None
        self.resetimages()
        self.gen.append(self.playing_monster())
        self.gen.append(self.back_to_dragon(saved_caps))

    def back_to_dragon(self, saved_caps):
        for t in range(259):
            yield None
            if BubPlayer.DragonList:
                yield None
                yield None
                yield None
        from player import Dragon
        d = Dragon(self.bubber, self.x, self.y, self.dir, saved_caps)
        d.dcap['shield'] = 50
        self.bubber.dragons.append(d)
        self.kill()

    def playing_monster(self):
        bubber = self.bubber
        if self.vy:
            # flying monster
            while 1:
                if bubber.key_left and bubber.key_left > bubber.key_right:
                    dx = -1
                elif bubber.key_right:
                    dx = 1
                else:
                    dx = 0
                if dx and dx != self.dir:
                    self.dir = dx
                    self.resetimages()
                if bubber.key_jump and bubber.key_jump > bubber.key_fire:
                    dy = -1
                elif bubber.key_fire:
                    dy = 1
                else:
                    dy = 0
                saved_dxdy = dx, dy
                blocked = 0
                nx = (self.x // self.vx) * self.vx
                ny = (self.y // self.vy) * self.vy
                if ny >= boards.bheight:
                    ny -= boards.bheightmod
                elif ny < -2*CELL:
                    ny += boards.bheightmod
                if (nx % CELL) == 0:
                    if dx < 0:
                        x0 = nx // CELL - 1
                    else:
                        x0 = (nx+self.ico.w) // CELL
                    for y in range(self.y // CELL, (self.y+self.ico.h-1) // CELL + 1):
                        if bget(x0, y) == '#':
                            dx = 0
                            blocked += 1
                            break
                if (ny % CELL) == 0:
                    if dy < 0:
                        y0 = ny // CELL - 1
                    else:
                        y0 = (ny+self.ico.h) // CELL
                    for x in range(self.x // CELL, (self.x+self.ico.w-1) // CELL + 1):
                        if bget(x, y0) == '#':
                            dy = 0
                            blocked += 1
                            break
                if blocked == 2 and bget(self.x//CELL+1, self.y//CELL+1) == '#':
                    dx, dy = saved_dxdy
                self.move(nx + dx*self.vx, ny + dy*self.vy)
                yield None
        elif not isinstance(self, Springy):
            # walking monster
            imgsetter = self.imgsetter
            while onground(self.x, self.y):
                wannafire = bubber.key_fire
                wannajump = bubber.key_jump
                if bubber.key_left and bubber.key_left > bubber.key_right:
                    dx = -1
                elif bubber.key_right:
                    dx = 1
                else:
                    dx = 0
                if dx and dx != self.dir:
                    self.dir = dx
                    self.resetimages()
                    imgsetter = self.imgsetter
                if dx:
                    x1 = self.x
                    if dx > 0:
                        x1 += self.vx
                    if self.blocked():
                        dx = 0
                if dx:
                    self.step(self.vx*dx, 0)
                    self.setimages(imgsetter)
                else:
                    self.setimages(None)
                yield None
                if wannafire and self.shoot(1):
                    return
                if wannajump:
                    if dx:
                        self.gen.append(self.hjumping())
                        return
                    for testy in range(self.y-2*CELL, self.y-6*CELL, -CELL):
                        if onground(self.x, testy):
                            break
                    self.gen.append(self.vjumping(testy, self.dir, bubber))
                    return
            self.gen.append(self.falling())
        else:
            # springy
            if not onground(self.x, self.y):
                self.gen.append(self.falling())
                return
            walker = self.walking()
            while 1:
                if bubber.key_left and bubber.key_left > bubber.key_right:
                    dx = -1
                elif bubber.key_right:
                    dx = 1
                else:
                    dx = 0
                if dx and dx != self.dir:
                    self.dir = dx
                    self.resetimages()
                if dx:
                    self.vx = 2
                else:
                    self.vx = 0
                try:
                    yield walker.next()
                except StopIteration:
                    return

    def become_ghost(self):
        self.gen = [self.ghosting()]
        self.resetimages(is_ghost=1)

    def ghosting(self):
        counter = 0
        while counter < 5:
            for i in range(50):
                yield None
            d = self.tagdragon()
            if d is None:
                counter += 1
            else:
                counter = 0
                if abs(d.x-self.x) < abs(d.y-self.y):
                    dx = 0
                    if d.y > self.y:
                        dy = 1
                    else:
                        dy = -1
                else:
                    dy = 0
                    if d.x > self.x:
                        dx = 1
                    else:
                        dx = -1
                    self.dir = dx
                    self.resetimages(is_ghost=1)
                dx *= 10
                dy *= 9
                distance = 1E10
                while 1:
                    self.angry = 0
                    self.step(dx, dy)
                    yield None
                    dist1 = (d.x-self.x)*(d.x-self.x)+(d.y-self.y)*(d.y-self.y)
                    if dist1 > distance:
                        break
                    distance = dist1
        self.angry = 0
        self.gen = [self.default_mode()]
        self.resetimages()

    default_mode = falling


def argh_em_all():
    poplist = [None]
    for s in images.ActiveSprites[:]:
        if isinstance(s, Monster):
            s.argh(poplist)

def freeze_em_all():
    poplist = [None]
    for s in images.ActiveSprites:
        if isinstance(s, Monster):
            s.freeze(poplist)


class MonsterShot(ActiveSprite):
    speed = 6
    touchable = 1
    
    def __init__(self, owner, dx=CELL, dy=0):
        self.owner = owner
        self.speed = owner.dir * self.speed
        if owner.dir < 0:
            nimages = owner.mdef.left_weapon
        else:
            nimages = owner.mdef.right_weapon
        ActiveSprite.__init__(self, images.sprget(nimages[0]),
                              owner.x, owner.y + dy)
        self.step((owner.ico.w - self.ico.w) // 2,
                  (owner.ico.h - self.ico.h) // 2)
        if not self.blocked():
            self.step(dx*owner.dir, 0)
        if len(nimages) > 1:
            self.setimages(self.cyclic(nimages, 3))
        self.gen.append(self.moving())

    def blocked(self):
        if self.speed < 0:
            x0 = (self.x-self.speed-HALFCELL)//CELL
        else:
            x0 = (self.x+self.ico.w+self.speed-HALFCELL)//CELL
        y0 = (self.y+HALFCELL) // CELL + 1
        return not (' ' == bget(x0,y0) == bget(x0+1,y0))

    def moving(self):
        while not self.blocked():
            yield None
            self.step(self.speed, 0)
        self.hitwall()

    def hitwall(self):
        self.untouchable()
        self.gen.append(self.die(self.owner.mdef.decay_weapon, 2))

    def touched(self, dragon):
        dragon.die()


class BoomerangShot(MonsterShot):
    speed = 8
    
    def hitwall(self):
        self.gen.append(self.moveback())

    def moveback(self):
        owner = self.owner
        if self.speed > 0:
            nimages = owner.mdef.left_weapon
        else:
            nimages = owner.mdef.right_weapon
        self.setimages(self.cyclic(nimages, 3))
        while (owner.x-self.x) * self.speed < 0:
            yield None
            self.step(-self.speed, 0)
            if self.blocked():
                break
        self.kill()

class FastShot(MonsterShot):
    speed = 15


class DownShot(MonsterShot):

    def __init__(self, owner):
        MonsterShot.__init__(self, owner, 0, CELL)

    def moving(self):
        while self.y < boards.bheight:
            yield None
            self.step(0, 7)
        self.kill()


##class DragonShot(MonsterShot):
##    speed = 8

##    def __init__(self, owner):
##        MonsterShot.__init__(self, owner)
##        self.untouchable()
##        self.gen.append(self.touchdelay(4))

##    def touched(self, dragon):
##        if dragon is not self.owner:
##            if dragon.bubber.bonbons == 0:
##                dragon.die()
##            else:
##                from player import scoreboard
##                from bonuses import Sugar1, Sugar2
##                from bonuses import BonusMaker
##                if random.random() < 0.2345:
##                    start = 1
##                else:
##                    start = 0
##                loose = min(2, dragon.bubber.bonbons)
##                for i in range(start, loose):
##                    cls = random.choice([Sugar1, Sugar2])
##                    BonusMaker(self.x, self.y, [cls.nimage],
##                               outcome=(cls,))
##                dragon.bubber.bonbons -= loose
##                scoreboard()
##                dragon.dcap['shield'] = 25
##                self.owner.play(images.Snd.Yippee)
##                self.kill()

##    def blocked(self):
##        return self.x < -self.ico.w or self.x >= gamesrv.playfield.width
##        #return self.x < CELL or self.x >= boards.bwidth - 3*CELL


class Nasty(Monster):
    pass

class Monky(Monster):
    shootcls = MonsterShot

class Ghosty(Monster):
    default_mode = Monster.flying
    vy = 2

class Flappy(Monster):
    default_mode = Monster.flying
    vy = 1

class Springy(Monster):
    spring_down = 0
    def imgrange(self):
        if self.spring_down and not self.is_ghost:
            if self.angry:
                if self.dir > 0:
                    r = self.mdef.right_jump_angry
                else:
                    r = self.mdef.left_jump_angry
            else:
                if self.dir > 0:
                    r = self.mdef.right_jump
                else:
                    r = self.mdef.left_jump
            return [r[self.spring_down-1]]
        else:
            return Monster.imgrange(self)
    def walking(self):
        self.spring_down = 1
        self.resetimages()
        for t in range(2+self.overlapping(1.0)):
            yield None
        self.spring_down = 2
        self.resetimages()
        for t in range(4+2*self.overlapping(1.0)):
            yield None
        self.spring_down = 1
        self.resetimages()
        for t in range(2+self.overlapping(1.0)):
            yield None
        self.spring_down = 0
        self.resetimages()
        g = 10.0/43
        vy = -20*g
        yf = self.y
        for t in range(40):
            yf += vy
            vy += g
            if self.blocked():
                self.dir = -self.dir
                self.resetimages()
            nx = self.x + self.dir*self.vx
            if self.y//CELL < int(yf)//CELL:
                if onground(self.x, (self.y//CELL+1)*CELL):
                    break
                if onground(nx, (self.y//CELL+1)*CELL):
                    self.move(nx, self.y)
                    break
            if yf >= boards.bheight:
                yf -= boards.bheightmod
            elif yf < -2*CELL:
                yf += boards.bheightmod
            self.move(nx, int(yf))
            yield None
        self.gen.append(self.falling())

class Orcy(Monster):
    shootcls = FastShot

class Gramy(Monster):
    shootcls = BoomerangShot
    vx = 3

class Blitzy(Monster):
    shootcls = DownShot
    vx = 3

    def seedragon(self, p=None):
        return 0

    def special(self):
        if random.random() < 0.5:
            self.shootcls(self)
        return 0

    def shoot(self, pause=0):
        # no pause (only used when controlled by the player)
        if self.no_shoot_before > BubPlayer.FrameCounter:
            pass
        else:
            self.shootcls(self)
            self.no_shoot_before = BubPlayer.FrameCounter + 29
        return 0

MonsterClasses = [c for c in globals().values()
                  if type(c)==type(Monster) and issubclass(c, Monster)]
MonsterClasses.remove(Monster)