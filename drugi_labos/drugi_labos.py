from pyglet.graphics import *
from pyglet.window import *
from random import uniform
from pyglet.gl import *

window = Window(width=640, height=480, caption='Sustav cestica')
window.set_location(150, 100)
glBlendFunc(GL_SRC_ALPHA, GL_ONE)
glEnable(GL_BLEND)
tex = pyglet.image.load('explosion.bmp').get_texture()

ociste = [10, 10, 0]
glediste = [0, 0, 0]
kut = 0.0
cestice = []
gravitacija = -200
max_cestica = 1000
r = 1.0
g = 0.5
b = 0.0

class Cestica:
    def __init__(self):
        ''' PROCES STVARANJA NOVIH CESTICA -- odredivanje pocetnih vrijednosti atributa cestice:
                                               - x koordinata
                                               - y koordinata
                                               - pomak x koordinate (dx)
                                               - pomak y koordinate (dy)
                                               - pomak z koordinate (dz) - nula
                                               - velicina cestice
                                               - vrijeme zivota
                                               - zastavica za zivot
        '''
        self.x = window.width / 2
        self.y = window.height / 3
        self.z = 0.0
        self.dx = window.width/2 - uniform(20.0, 45.0)*10
        self.dy = uniform(10.0, window.height-150.0)
        self.dz = 0.0
        self.size_tex = 6
        self.size_point = 4
        self.lifespan = uniform(0, 1)
        self.alive = True

    # 3. PRORACUN NOVOG STANJA -- za ovu cesticu (za proteklo vrijeme dt)
    def update_cestica(self, dt):
        self.lifespan -= 0.004          # na pocetku proracuna novog stanja, povecaj starost
        self.size_tex -= 0.02
        if self.size_point > 0.02:
            self.size_point -= 0.02
        # pomakni cesticu na novi polozaj
        self.dy += gravitacija * dt         # y pomak povecavam s obzirom na gravitaciju jer ona vuce prema dolje (nema utjecaja na dx)
        #self.dx += 100 * dt                # daje opciju izgleda puhanja vjetra s lijeva na desno
        self.x += self.dx * dt
        self.y += self.dy * dt
        self.z += self.dz * dt

        # provjeri je li ziva
        # ili joj je gotov zivot ili je ispala s ekrana
        if self.lifespan <= 0.0 or self.x <= 0.0 or self.x >= window.width or \
                self.y <= 0.0 or self.y >= window.height:
            self.alive = False

    def is_dead(self):
        if self.alive:
            return False
        else:
            return True

# 5. PROCES STVARANJA NOVIH CESTICA
def dodaj_cesticu():
    cestica = Cestica()
    cestice.append(cestica)

def update_all(dt):
    global cestice

    # 2. PRORACUN NOVOG STANJA -- za svaku posebno (za proteklo vrijeme dt)
    for cestica in cestice:
        cestica.update_cestica(dt)

    # odredi cestice cija je starost veca od njihovog vremena zivota i ugasi ih (obrisi)
    cestice_pom = [cestica for cestica in cestice if not cestica.is_dead()]
    num_deleted = len(cestice) - len(cestice_pom)
    cestice = cestice_pom

    # za pocetak
    if num_deleted == 0:
        return 1
    else:
        # tako da znam dodati jednako tocaka koliko ih je obrisano s ekrana
        return num_deleted

# 7. CRTANJE SUSTAVA -- nacrtaj sustav cestica
def crtaj_sustav_cestica(type):
    global cestice, r, g, b
    if type == 'tekstura':
        glEnable(tex.target)
        glBindTexture(tex.target, tex.id)

        glBegin(GL_QUADS)
        for cestica in cestice:
            glColor4f(r, g, b, cestica.lifespan)
            glTexCoord2f(0, 0)
            glVertex3f(cestica.x-cestica.size_tex, cestica.y-cestica.size_tex, cestica.z)
            glTexCoord2f(1, 0)
            glVertex3f(cestica.x+cestica.size_tex, cestica.y-cestica.size_tex, cestica.z)
            glTexCoord2f(1, 1)
            glVertex3f(cestica.x+cestica.size_tex, cestica.y+cestica.size_tex, cestica.z)
            glTexCoord2f(0, 1)
            glVertex3f(cestica.x-cestica.size_tex, cestica.y+cestica.size_tex, cestica.z)
        glEnd()
        glDisable(tex.target)
    else:
        for cestica in cestice:
            glPointSize(cestica.size_point)
            glBegin(GL_POINTS)
            glColor4f(r, g, b, cestica.lifespan)
            glVertex3f(cestica.x, cestica.y, cestica.z)
            glEnd()

def crtaj_postolje():
    glColor3f(0.7, 1.0, 1.0)
    glBegin(GL_QUADS)
    glVertex3f(window.width/2 - 10.0, window.height/3 - 80.0, 0.0)
    glVertex3f(window.width/2 - 10.0, window.height/3, 0.0)
    glVertex3f(window.width/2 + 10.0, window.height/3, 0.0)
    glVertex3f(window.width/2 + 10.0, window.height/3 - 80.0, 0.0)
    glEnd()

#------------------------------------------------------------------------------------#

@window.event
def on_draw():
    global r, g, b

    window.clear()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # izmjena boja
    if r > 0.0:
        r -= 0.0002
    else:
        r = 0.0
    if b < 1.0:
        b += 0.005
    else:
        b = 1.0
        if g > 0.0:
            g -= 0.005
        else:
            g = 0.0

    # nacrtaj pravokutnik
    crtaj_postolje()

    # 6. CRTANJE SUSTAVA -- nacrtaj sustav cestica
    crtaj_sustav_cestica('tocke')

    glFlush()

def update_frame(dt):   # dt = koliko je sekunda proslo od zadnji put kad se zvala ova metoda - zove ju svakih cca 0.01 sekundu
    # 1. PRORACUN NOVOG STANJA -- sve cestice (za proteklo vrijeme dt)
    deleted = update_all(dt)

    # 4. PROCES STVARANJA NOVIH CESTICA
    for i in range(min(deleted*2, max_cestica - len(cestice))):
        dodaj_cesticu()

pyglet.clock.schedule(update_frame)
pyglet.app.run()
