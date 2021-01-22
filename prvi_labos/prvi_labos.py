from pyglet.gl import *
from pyglet.window import *
import math

obj_v = []      # koordinate tocaka (x y z)
obj_f = []      # indeksi tocaka za trokut (poligone)

bspline_v = []  # tocke krivulje
centar = [0.0, 0.0, 0.0]    # varijabla za racunanje centra objekta

# za ucitavanje podataka za objekt
def read_obj(file):
    dat = open(file, "r")

    for line in dat:
        if line.startswith("f"):
            dijelovi = line.split()
            obj_f.append((int(dijelovi[1]) - 1, int(dijelovi[2]) - 1, int(dijelovi[3]) - 1))
            # clanovi se gledaju za jedan manje (isto kao i indexi)
        if line.startswith("v"):
            dijelovi = line.split()
            x_obj = float(dijelovi[1])
            y_obj = float(dijelovi[2])
            z_obj = float(dijelovi[3])
            obj_v.append((x_obj, y_obj, z_obj))
            # dodajemo za racunanje centra objekta
            centar[0] += x_obj
            centar[1] += y_obj
            centar[2] += z_obj

# za ucitavanje podataka za krivulju
def read_bspline():
    dat = open("bspline.txt", "r")
    for line in dat:
        dijelovi = line.split()
        bspline_v.append((float(dijelovi[1]), float(dijelovi[2]), float(dijelovi[3])))

#ucitavanje tocaka krivulje
read_bspline()

# ucitavanje objekta
fileName = "kocka.txt"
read_obj(fileName)
centar[0] /= len(obj_v)
centar[1] /= len(obj_v)
centar[2] /= len(obj_v)

# odredivanje SEGMENATA krivulje = broj tocaka-3 (svaki segment mora imati 4 tocke)
brSeg = len(bspline_v) - 3

# za svaki segment krivulje mijenjati parametar t od 0 do 1
bspline_segmenti = {}   # sve tocke krivulje
tangente = {}           # sve tangente (tj svi vektori smjera tangenti!)
tan_num = 0

tangente_za_crtanje = {}        # tangente koje ce se crtati
tan_za_crtanje_num = 0

for seg_num in range(brSeg):
    # uzimam 4 tocke za segment
    tocka_1 = bspline_v[seg_num]
    tocka_2 = bspline_v[seg_num+1]
    tocka_3 = bspline_v[seg_num+2]
    tocka_4 = bspline_v[seg_num+3]

    t = 0
    while t<1.0:
        # formula 1.2
        # [clan_1 clan_2 clan_3 clan_4]*1/6 * vektor_tocaka
        clan_1 = (-pow(t, 3.0) + 3*pow(t, 2.0) - 3*t + 1) / 6.0
        clan_2 = (3*pow(t, 3.0) - 6*pow(t, 2.0) + 0 + 4) / 6.0
        clan_3 = (-3*pow(t,3.0) + 3*pow(t, 2.0) + 3*t + 1) / 6.0
        clan_4 = (pow(t,3.0)) / 6.0

        # svaki segment prolazi kroz 100 t-ova (segment 1: tocke od 0-99)
        index = int(round(100*round(t,2)) + 100*seg_num)
        bspline_segmenti[index] = (clan_1*tocka_1[0] + clan_2*tocka_2[0] + clan_3*tocka_3[0] + clan_4*tocka_4[0],
                                   clan_1*tocka_1[1] + clan_2*tocka_2[1] + clan_3*tocka_3[1] + clan_4*tocka_4[1],
                                   clan_1*tocka_1[2] + clan_2*tocka_2[2] + clan_3*tocka_3[2] + clan_4*tocka_4[2])

        # racunam vektor smjera tangente za trenutni t
        #   tangenta je odredena onda gore prethodno dobivenom tockom te ovim vektorom smjera
        clan_1 = (-pow(t,2.0) + 2*t - 1) / 2.0
        clan_2 = (3*pow(t,2.0) - 4*t + 0) / 2.0
        clan_3 = (-3*pow(t,2.0) + 2*t + 1) / 2.0
        clan_4 = (pow(t,2.0)) / 2.0

        x = clan_1 * tocka_1[0] + clan_2 * tocka_2[0] + clan_3 * tocka_3[0] + clan_4 * tocka_4[0]
        y = clan_1 * tocka_1[1] + clan_2 * tocka_2[1] + clan_3 * tocka_3[1] + clan_4 * tocka_4[1]
        z = clan_1 * tocka_1[2] + clan_2 * tocka_2[2] + clan_3 * tocka_3[2] + clan_4 * tocka_4[2]

        # vektor smjera tangente
        tangente[int(tan_num)] = (x, y, z)
        tan_num+=1

        t+=0.01

    # racunanje tangenti - po dvije za jedan segment
    #   pocetna tocka tangente je tocka krivulje za taj t
    tangente_za_crtanje[tan_za_crtanje_num] = bspline_segmenti[100*seg_num+25]
    tan_za_crtanje_num+=1
    #   konacna tocka tangente je tocka krivulje u t + vektor smjera tangente za t * neki faktor
    x = bspline_segmenti[100 * seg_num + 25][0] + tangente[100 * seg_num + 25][0] * 1 / 2
    y = bspline_segmenti[100 * seg_num + 25][1] + tangente[100 * seg_num + 25][1] * 1 / 2
    z = bspline_segmenti[100 * seg_num + 25][2] + tangente[100 * seg_num + 25][2] * 1 / 2
    tangente_za_crtanje[tan_za_crtanje_num] = (x, y, z)
    tan_za_crtanje_num+=1
    
    tangente_za_crtanje[tan_za_crtanje_num] = bspline_segmenti[100*seg_num+75]
    tan_za_crtanje_num+=1
    x = bspline_segmenti[100 * seg_num + 75][0] + tangente[100 * seg_num + 75][0] * 1 / 2
    y = bspline_segmenti[100 * seg_num + 75][1] + tangente[100 * seg_num + 75][1] * 1 / 2
    z = bspline_segmenti[100 * seg_num + 75][2] + tangente[100 * seg_num + 75][2] * 1 / 2
    tangente_za_crtanje[tan_za_crtanje_num] = (x, y, z)
    tan_za_crtanje_num+=1

# za crtanje krivulje i tangenti
def draw_bspline():
    # 9 segmenata - svaki segment ima 100 dijelova (100 t-ova)
    glBegin(GL_LINE_STRIP)
    for seg_num in range(0, 100*brSeg, 2):
        # crtam liniju izmedu dvije tocke
        glColor3f(0, 0, 0)
        glVertex3f(bspline_segmenti[seg_num][0], bspline_segmenti[seg_num][1], bspline_segmenti[seg_num][2])
        glVertex3f(bspline_segmenti[seg_num+1][0], bspline_segmenti[seg_num+1][1], bspline_segmenti[seg_num+1][2])
    glEnd()

    # nacrtaj tangente
    glBegin(GL_LINES)
    for i in range(0, 4*brSeg, 2):
        glColor3f(1, 0, 0)
        glVertex3f(tangente_za_crtanje[i][0], tangente_za_crtanje[i][1], tangente_za_crtanje[i][2])
        glVertex3f(tangente_za_crtanje[i+1][0], tangente_za_crtanje[i+1][1], tangente_za_crtanje[i+1][2])
    glEnd()

# za crtanje objekta
def draw_object():
    glBegin(GL_LINES)
    for i in range(len(obj_f)):
        polygon = obj_f[i]       # (tocka_1, tocka_2, tocka_3)
        point_one = obj_v[polygon[0]]
        point_two = obj_v[polygon[1]]
        point_three = obj_v[polygon[2]]
        
        glVertex3f(point_one[0], point_one[1],point_one[2])
        glVertex3f(point_two[0], point_two[1], point_two[2])

        glVertex3f(point_two[0], point_two[1], point_two[2])
        glVertex3f(point_three[0], point_three[1], point_three[2])

        glVertex3f(point_three[0], point_three[1],point_three[2])
        glVertex3f(point_one[0], point_one[1], point_one[2])
        
    glEnd()

#------------------------------------------------------------------------------------#
window = pyglet.window.Window(width=1000, height=600, caption='Animacija objekta - BSpline', resizable=True)
window.set_location(35, 35)
time = 0

@window.event
def on_draw():
    window.clear()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(-4.0, -3.0, -70.0)
    
    global time     # referiram se na globalnu varijablu time

    # nacrtaj krivulju
    draw_bspline()

    # translatiraj sve na nacrtanu krivulju
    glTranslatef(bspline_segmenti[time][0], bspline_segmenti[time][1], bspline_segmenti[time][2])

    # izracunaj dijelove za rotaciju objekta
    s = [0.0, 0.0, 1.0]
    os = []
    e = tangente[time]

    os.append(s[1] * e[2] - e[1] * s[2])
    os.append(s[2] * e[0] - e[2] * s[0])
    os.append(s[0] * e[1] - e[0] * s[1])

    aps_s = pow(pow(s[0], 2.0) + pow(s[1], 2.0) + pow(s[2], 2.0), 0.5)
    aps_e = pow(pow(e[0], 2.0) + pow(e[1], 2.0) + pow(e[2], 2.0), 0.5)
    se = s[0] * e[0] + s[1] * e[1] + s[2] * e[2]
    kut = math.acos(se / (aps_s * aps_e))
    kut = kut / (2 * math.pi) * 360

    # rotiraj i nacrtaj objekt
    glRotatef(kut, os[0], os[1], os[2])
    glTranslatef(-centar[0], -centar[1], -centar[2])    # namjestim srediste rotiranog objekta na krivulju
    glColor3f(0, 0, 1)
    draw_object()
    
    if time!=(100*brSeg-1):
        time += 1
    else:
        time = 0

    glFlush()

@window.event
def on_resize(new_width, new_height):
    glViewport(0, 0, new_width, new_height)
    glMatrixMode(gl.GL_PROJECTION)
    glLoadIdentity()
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    gluPerspective(45.0, float(new_width) / new_height, 0.5, 100.0)
    glColor3f(0, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    return pyglet.event.EVENT_HANDLED

def update_frame(x):
    pass

pyglet.clock.schedule_interval(update_frame, 1/30.0)
pyglet.app.run()
