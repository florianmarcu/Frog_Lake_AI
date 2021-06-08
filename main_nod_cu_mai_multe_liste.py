# Problema Broscoceilor - Rezolvare AStar

"""
Input:
    nume_folder_intrare
    nume_folder_iesire
    numarul de solutii dorit
    timpul de timeout
"""


# informatii despre un nod din arborele de parcurgere (nu din graful initial)
class NodParcurgere:
    graf = None  # static

    # Fiecare v[i] pentru vectorii de mai jos repr informatia coresp broscutei 'i' la pasul respectiv
    def __init__(self, id, info, parinte, cost, h):
        self.id = id  # Vector de indici din vectorul initial de noduri
        self.info = info # Vector de info despre noduri
        self.parinte = parinte  # Parintele din arborele de parcurgere
        self.g = cost  # Vector de costuri de la radacina la nodul curent
        self.h = h  # Vector al valorii euristicii pentru nodul
        self.f = self.g + self.h

    # list
    def obtineDrum(self):
        l = [self.info];
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
        sir += self.info + "("
        sir += "id = {}, ".format(self.id)
        sir += "drum="
        drum = self.obtineDrum()
        sir += ("->").join(drum)
        sir += " g:{}".format(self.g)
        sir += " h:{}".format(self.h)
        sir += " f:{})".format(self.f)
        return (sir)


class Graph:  # graful problemei
    def __init__(self, noduri, broscute, matriceAdiacenta, matricePonderi, start, destinatii, lista_h):
        self.noduri = noduri
        self.broscute = broscute
        self.matriceAdiacenta = matriceAdiacenta
        self.matricePonderi = matricePonderi
        self.nrNoduri = len(matricePonderi)
        self.start = start
        self.destinatii = destinatii
        self.lista_h = lista_h

    def indiceNod(self, n):
        return self.noduri.index(n)

    # TODO
    def testeaza_destinatie(self, nodCurent):
        for i in range(len(nodCurent.info)):
            #if nodCurent.info[i]
                #return True
            return False
    def poateSari(self, nodCurent, indexBr, j):
        #x = self.matricePonderi[nodCurent.id[indexBr]][j]
        x1 = self.noduri[nodCurent.id[indexBr]][1]
        y1 = self.noduri[nodCurent.id[indexBr]][2]
        x2 = self.noduri[j][1]
        y2 = self.noduri[j][2]
        dist = ((x1-x2)**2+(y1-y2)**2)**(1/2)
        if dist <= self.broscute[indexBr][1]/3:
            return True
        return False

    # va genera succesorii sub forma de noduri in arborele de parcurgere
    # TODO
    # iteram pe linia lui 'nodCurent' din mp si adaugam doar daca mp[i][j] <= g[broscuta]/3
    def genereazaSuccesori(self, nodCurent, indexBr):
        listaSuccesori = []
        # inca un for pentru a itera fiecare broscuta
        for b in range(len(self.broscute)):
            # pentru broscuta b
            for i in range(self.nrNoduri):
                if self.poateSari(nodCurent, indexBr, i) and not nodCurent.contineInDrum(self.noduri[i], indexBr):
                    nodNou = NodParcurgere(
                        i,
                        self.noduri[i],
                        nodCurent,
                        nodCurent.g + self.matricePonderi[nodCurent.id][i],
                        self.calculeaza_h(self.noduri[i])
                    )
                    listaSuccesori.append(nodNou)
        return listaSuccesori

    # TODO
    def calculeaza_h(self, infoNod):
        return self.lista_h[self.indiceNod(infoNod)]

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return (sir)


def citire():
    input = open("input/in.txt")
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
    print(broscute)

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
    print("matricea de ponderi:")
    for i in range(len(mp)):
        print(mp[i])
    # creearea euristicii pe baza distantei fata de origine
    lista_h = []
    for i in range(len(noduri)):
        x = noduri[i][1]
        y = noduri[i][2]
        lista_h.append(radius - ((x**2+y**2)**(1/2)))
    G = Graph(noduri, broscute, [], mp, start, [], lista_h)
    NodParcurgere.graf = G
    print(noduri)

def a_star(gr, nrSolutiiCautate):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    # c = [NodParcurgere(gr.indiceNod(gr.start), gr.start, None, 0, gr.calculeaza_h(gr.start))]
    c = []
    cozi = []
    for i in range(len(start)):
        cozi.append([NodParcurgere(gr.indiceNod(gr.start[i]), gr.start[i], None, 0, gr.calculeaza_h(gr.start[i]))])
    while len(c) > 0:
        print("Coada actuala: " + str(c))
        input()
        nodCurent = c.pop(0)

        if gr.testeaza_destinatie(nodCurent):
            print("Solutie: ")
            nodCurent.afisDrum()
            print("\n----------------\n")
            input()
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # diferenta fata de UCS e ca ordonez dupa f
                if c[i].f >= s.f:
                    gasit_loc = True
                    break;
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)


citire()
# a_star(gr, nrSolutiiCautate=3)