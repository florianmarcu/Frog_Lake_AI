# Problema Broscoceilor

import time
start_time = time.time()

"""
Input:
    nume_folder_intrare
    nume_folder_iesire
    numarul de solutii dorit
    timpul de timeout
"""

############################################  9) Afisarea in fisierele de output   ################################################

output = open("out.txt", "w")

# informatii despre un nod din arborele de parcurgere (nu din graful initial)
class NodParcurgere:
    graf = None  # static

    # Fiecare v[i] pentru vectorii de mai jos repr informatia coresp broscutei 'i' la pasul respectiv
    def __init__(self, id, info, info_frunze, parinte, cost, h):
        self.id = id  # indicele din vectorul de noduri
        self.stare_broscute = info # Vector de info despre fiecare broscuta
        self.stare_frunze = info_frunze # Vector ce contine nr de insecte de pe fiecare frunza in starea curenta
        self.lista_succesori = []
        self.parinte = parinte  # Parintele din arborele de parcurgere
        self.g = cost  # Distanta totala parcursa de toate broscutele pana aceasta pozitie
        self.h = h  # Euristica nodului curent
        self.f = self.g + self.h

    # list
    def obtineDrum(self):
        l = [self.info]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte.info)
            nod = nod.parinte
        return l

    # void
    def afisDrum(self):  # returneaza si lungimea drumului
        l = self.obtineDrum()
        print(("->").join(l))
        print("Cost: ", self.g)
        return len(l)

    # bool
    def contineInDrum(self, infoNodNou, indexBr):
        nodDrum = self
        while nodDrum is not None:
            if (infoNodNou == nodDrum.info[indexBr]):
                return True
            nodDrum = nodDrum.parinte

        return False

    # toString
    def __repr__(self):
        sir = ""
        for i in range(len(self.stare_frunze)):
            # afiseaza in format (nume nod, starea insectelor de pe nod, greutatea nodului)
            sir += self.graf.noduri[i][0] + ": " + str(self.stare_frunze[i]) + "," + str(self.graf.noduri[i][4]) + "\t"
        return (sir)


class Graph:  # graful problemei
    def __init__(self, noduri, broscute, matriceAdiacenta, matricePonderi, start, destinatii, lista_h, radius):
        self.noduri = noduri
        self.broscute = broscute
        self.matriceAdiacenta = matriceAdiacenta
        self.matricePonderi = matricePonderi
        self.nrNoduri = len(matricePonderi)
        self.start = start
        self.destinatii = destinatii
        self.lista_h = lista_h
        self.radius = radius

    ############################################  10) Testam daca pb are sau nu solutii   ################################################

    def poate_avea_solutii(self):
        max = self.broscute[0][1]
        for i in range(1,len(self.broscute)):
            if self.broscute[i][1] > max:
                max = self.broscute[i][1]
        s = 0
        for b in self.noduri:
            s += b[3]
        if (max+s)/3 < self.radius:
            return False
        return True

    def indiceNod(self, n):

        if len(n) == 4:
            return int(n[2:4])
        else:
            return int(n[2])

    ############################################  5) Testarea ajungerii in starea scop   ################################################
    def testeaza_destinatie(self, nodCurent):
        for b in nodCurent.stare_broscute:
            if b[0] is not None:
                return False
        return True

    # functie ajutatoare pentru calcularea sumei greutatilor broscutelor de pe frunza 'j'
    def sumaGreutatilorDePeFrunza(self, stare_broscute, j):
        s = 0
        for b in stare_broscute:
            i = self.indiceNod(b)
            if i == j:
                s += b[1]
        return s

    def poateIesi(self, broscuta, w):
        if broscuta[0] is not None:
            i = self.indiceNod(broscuta[0])
            dist = self.lista_h[i]
            print(dist)
            if dist <= (broscuta[1] + w)/3:
                return True
        return False
    # functie ajutatoare pentru calcularea distantei dintre noduri
    def poateSari(self, broscuta, j, w, stare_broscute):
        if broscuta[0] is not None:
            i = self.indiceNod(broscuta[0])
            ga = self.sumaGreutatilorDePeFrunza(stare_broscute, j)
            # verificam daca broscuta poate sari in pana la frunza 'i' si daca are greutatea <= greutate maxima a frunzei
            if mp[i][j] <= (broscuta[1] + w)/3 and self.noduri[j][4] - ga >= broscuta[1] + w:
                return True
        return False

    # functie ajutatoare pentru generarea succesorilor
    def backt(self, k, stare_broscute, stare_frunze, nodCurent):
        print("pas", k)
        if k < len(stare_broscute):
            print(k, stare_broscute[k][0])
            for i in range(len(stare_frunze)):
                print(k)
                if stare_broscute[k][0] is not None:
                    id_frunza_curenta = self.indiceNod(stare_broscute[k][0])
                    for w in range(stare_frunze[id_frunza_curenta]+1):
                        # verificam daca poate iesi direct
                        if i != id_frunza_curenta:
                            print(k, " incearca sa iasa")
                            if self.poateIesi(stare_broscute[k], w):
                                print("iese ", k)
                                # stare_broscute[k][0] = None
                                # stare_broscute[k][1] += w
                                # stare_broscute[k][2] += self.lista_h[id_frunza_curenta]
                                stare_frunze_copy = stare_frunze.copy()
                                stare_frunze_copy[id_frunza_curenta] -= w
                                stare_broscute_copy = stare_broscute.copy()
                                stare_broscute_copy[k][0] = None
                                stare_broscute_copy[k][1] += w
                                stare_broscute_copy[k][2] += self.lista_h[id_frunza_curenta]
                                #print(stare_broscute)
                                self.backt(k+1, stare_broscute_copy, stare_frunze_copy, nodCurent)
                            elif self.poateSari(stare_broscute[k], i, w, stare_broscute):
                                output.writelines("sare"+ "\n")
                                # stare_frunze_copy = stare_frunze.copy()
                                # stare_frunze_copy[id_frunza_curenta] -= w
                                # stare_broscute_copy = stare_broscute.copy()
                                # stare_broscute_copy[k][1] += w
                                # stare_broscute_copy[k][2] += mp[id_frunza_curenta][i]
                                stare_frunze[id_frunza_curenta] -= w
                                stare_broscute[k][0] = "id"+str(i)
                                stare_broscute[k][1] += w
                                stare_broscute[k][2] += mp[id_frunza_curenta][i]
                                self.backt(k+1, stare_broscute, stare_frunze, nodCurent)
                                stare_frunze[id_frunza_curenta] += w
                                # stare_broscute[k][0] = "id"+str(i)
                                stare_broscute[k][1] -= w
                                stare_broscute[k][2] -= mp[id_frunza_curenta][i]
                            else:
                                self.backt(k + 1, stare_broscute, stare_frunze, nodCurent)
                else:
                    self.backt(k + 1, stare_broscute, stare_frunze, nodCurent)

        else:
            print("nod nou")
            ############################################  4) Calcularea costului unei mutari   ################################################
            g = 0
            for b in stare_broscute:
                g += b[2]
            h = self.calculeaza_h(stare_broscute)
            f = g + h
            nod_nou = NodParcurgere(
                0, # id?
                stare_broscute, #starea broscutelor
                stare_frunze, #starea frunzelor
                nodCurent, #parintele nodului
                g, #costul nodului
                h
            )
            nodCurent.lista_succesori.append(nod_nou)

    ############################################  3) Functia de generare a succesorilor   ################################################
    # generam prin backtracking toti succesorii posibili
    def genereazaSuccesori(self, nodCurent):
        nodCurent.lista_succesori.clear()
        stare_broscute_copy = nodCurent.stare_broscute.copy()
        stare_frunze_copy = nodCurent.stare_frunze.copy()
        self.backt(0, stare_broscute_copy, stare_frunze_copy, nodCurent)
        return nodCurent.lista_succesori

    # TODO
    # eurisitica admisibila evalueaza h-ul unui nod calculand suma distantelor broscutelor fata de marginea lacului
    def calculeaza_h(self, stare_broscute):
        #print(self.lista_h)
        sum = 0
        for b in stare_broscute:
            if b[0] != None:
                punct = b[0]
                if len(punct) == 4:
                    index = int(punct[2:4])
                else:
                    index = int(punct[2])
                sum += self.lista_h[index]
        print("suma= ", sum)
        return sum

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return (sir)

############################################  7) Crearea fisierelor   ################################################
############################################  2) Parsarea fisierului   ################################################
def citire():
    # input = open("in.txt")
    input = open("input/in2.txt")
    global radius, G, noduri, broscute, start, mp, lista_h
    broscute = []
    start = []
    noduri = []
    mp = []
    radius = int(input.readline())
    line = input.readline().split()
    for i in range(0, len(line), 3):
        broscute.append([line[i], int(line[i + 1]), line[i + 2]])
        start.append(line[i + 2])
    #print(broscute)

    line = input.readline().split()
    while line != []:
        noduri.append([line[0], int(line[1]), int(line[2]), int(line[3]), int(line[4])])
        line = input.readline().split()
    # initializare cu 0 a matricei ponderilor 'mp'
    for i in range(len(noduri)):
        mp.append([])
        for j in range(len(noduri)):
            mp[i].append(0)
    # calcularea distantelor dintre frunze
    for i in range(len(noduri)):
        x1 = noduri[i][1]
        y1 = noduri[i][2]
        for j in range(len(noduri)):
            x2 = noduri[j][1]
            y2 = noduri[j][2]
            mp[i][j] = round(((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1 / 2), 2)
    #print("matricea de ponderi:")
    # for i in range(len(mp)):
    #     print(mp[i])
    ############################################  6) Euristica admisibila   ################################################
    # creearea euristicii pe baza distantei fata de origine
    lista_h = []
    for i in range(len(noduri)):
        x = noduri[i][1]
        y = noduri[i][2]
        lista_h.append(radius - ((x**2+y**2)**(1/2)))
    G = Graph(noduri, broscute, [], mp, start, [], lista_h, radius)
    NodParcurgere.graf = G
    # print(noduri, "\n")
    if not G.poate_avea_solutii():
        exit

def a_star(G, nrSolutiiCautate):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    stare_broscute = []
    for i in range(len(G.broscute)):
        stare_broscuta_i = [G.broscute[i][2], G.broscute[i][1], 0]
        stare_broscute.append(stare_broscuta_i)
    #print(stare_broscute)
    stare_frunze = []
    for nod in G.noduri:
        stare_frunze.append(nod[3])
    c = [NodParcurgere(
        0, #G.indiceNod(G.start),
        stare_broscute,  #starea broscutelor
        stare_frunze, # starea frunzelor
        None,  #parintele nodului
        0,  #costul curent
        G.calculeaza_h(stare_broscute)
                    )]
    # print("c=",c[0].stare_broscute)
    #output.writelines("\n\n\n\n\n")
    while len(c) > 0:
        output.writelines("Lungimea cozii actuale: " + str(len(c)) + "\n")
        nodCurent = c.pop(0)
        if G.testeaza_destinatie(nodCurent):
            output.writelines("Solutie de cost: " + str(nodCurent.f) + "\n")
            output.writelines("--- %s seconds ---" % round((time.time() - start_time),2))
            #input()
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = G.genereazaSuccesori(nodCurent)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # diferenta fata de UCS e ca ordonez dupa f
                if c[i].f >= s.f:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)

def ucs(G, nrSolutiiCautate):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    stare_broscute = []
    for i in range(len(G.broscute)):
        stare_broscuta_i = [G.broscute[i][2], G.broscute[i][1], 0]
        stare_broscute.append(stare_broscuta_i)
    # print(stare_broscute)
    stare_frunze = []
    for nod in G.noduri:
        stare_frunze.append(nod[3])
    c = [NodParcurgere(
        0,  # G.indiceNod(G.start),
        stare_broscute,  # starea broscutelor
        stare_frunze,  # starea frunzelor
        None,  # parintele nodului
        0,  # costul curent
        G.calculeaza_h(stare_broscute)
    )]
    # print("c=",c[0].stare_broscute)
    #output.writelines("\n\n\n\n\n")
    while len(c) > 0:
        output.writelines("Lungimea cozii actuale: " + str(len(c)) + "\n")
        nodCurent = c.pop(0)
        if G.testeaza_destinatie(nodCurent):
            output.writelines("Solutie de cost: " + str(nodCurent.f) + "\n")
            output.writelines("--- %s seconds ---" % round((time.time() - start_time),2))

            # input()
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = G.genereazaSuccesori(nodCurent)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # diferenta fata de UCS e ca ordonez dupa f
                if c[i].g >= s.g:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)


def a_star_opt(gr):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    stare_broscute = []
    for i in range(len(G.broscute)):
        stare_broscuta_i = [G.broscute[i][2], G.broscute[i][1], 0]
        stare_broscute.append(stare_broscuta_i)
    # print(stare_broscute)
    stare_frunze = []
    for nod in G.noduri:
        stare_frunze.append(nod[3])
    l_open = [NodParcurgere(
        0,  # G.indiceNod(G.start),
        stare_broscute,  # starea broscutelor
        stare_frunze,  # starea frunzelor
        None,  # parintele nodului
        0,  # costul curent
        G.calculeaza_h(stare_broscute)
    )]
    l_closed = []
    # print("c=",c[0].stare_broscute)
    #output.writelines("\n\n\n\n\n")
    while len(l_open) > 0:
        output.writelines("Lungimea cozii actuale: " + str(len(l_open)) + "\n")
        nodCurent = l_open.pop(0)
        l_closed.append(nodCurent)
        if G.testeaza_destinatie(nodCurent):
            output.writelines("Solutie de cost: " + str(nodCurent.f) + "\n")
            output.writelines("--- %s seconds ---" % round((time.time() - start_time),2))

        lSuccesori = G.genereazaSuccesori(nodCurent)
        for s in lSuccesori:
            gasitC = False
            for nodC in l_open:
                if s.info == nodC.info:
                    gasitC = True
                    if s.f >= nodC.f:
                        lSuccesori.remove(s)
                    else:  # s.f<nodC.f
                        l_open.remove(nodC)
                    break
            if not gasitC:
                for nodC in l_closed:
                    if s.info == nodC.info:
                        if s.f >= nodC.f:
                            lSuccesori.remove(s)
                        else:  # s.f<nodC.f
                            l_closed.remove(nodC)
                        break
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(l_open)):
                # diferenta fata de UCS e ca ordonez dupa f
                if l_open[i].f >= s.f:
                    gasit_loc = True
                    break
            if gasit_loc:
                l_open.insert(i, s)
            else:
                l_open.append(s)

def ida_star(G, nrSolutiiCautate):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    stare_broscute = []
    for i in range(len(G.broscute)):
        stare_broscuta_i = [G.broscute[i][2], G.broscute[i][1], 0]
        stare_broscute.append(stare_broscuta_i)
    # print(stare_broscute)
    stare_frunze = []
    for nod in G.noduri:
        stare_frunze.append(nod[3])
    nodStart = NodParcurgere(
        0,  # G.indiceNod(G.start),
        stare_broscute,  # starea broscutelor
        stare_frunze,  # starea frunzelor
        None,  # parintele nodului
        0,  # costul curent
        G.calculeaza_h(stare_broscute)
    )
    limita = nodStart.f
    while True:
        nrSolutiiCautate, rez = construieste_drum(G, nodStart, limita, nrSolutiiCautate)
        if rez == "gata":
            break
        if rez == float('inf'):
            print("Nu exista solutii!")
            break
        limita = rez
        print(">>> Limita noua: ", limita)

def construieste_drum(gr, nodCurent, limita, nrSolutiiCautate):
    if nodCurent.f > limita:
        return nrSolutiiCautate, nodCurent.f
    if gr.testeaza_destinatie(nodCurent) and nodCurent.f == limita:
        output.writelines("Solutie de cost: " + str(nodCurent.f) + "\n")
        output.writelines("--- %s seconds ---" % round((time.time() - start_time), 2))

        #nodCurent.afisDrum()
        print(limita)
        print("\n----------------\n")
        input()
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            return
    lSuccesori = gr.genereazaSuccesori(nodCurent)
    minim = float('inf')
    for s in lSuccesori:
        nrSolutiiCautate, rez = construieste_drum(gr, s, limita, nrSolutiiCautate)
        if rez=="gata":
            return 0,"gata"
        print("Compara ", rez, " cu ", minim)
        if rez < minim:
            minim = rez
            print("Noul minim: ", minim)
    return nrSolutiiCautate, minim


def main():
    nume_folder_input = input()
    nr_solutii_cautate = int(input())
    citire()
    ############################################  8) Rezolvarea a NSOL   ################################################
    output.writelines("\nA* :\n")
    a_star(G, nrSolutiiCautate=nr_solutii_cautate)
    output.writelines("\nUCS* :\n")
    ucs(G, nrSolutiiCautate=nr_solutii_cautate)
    output.writelines("\nIDA* :\n")
    #ida_star(G, nrSolutiiCautate=nr_solutii_cautate)
    output.writelines("\nA* Opt :\n")
    #a_star_opt(G)

main()

