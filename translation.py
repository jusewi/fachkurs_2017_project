import processes
import random
import database
from molecules import Ribo, Protein, MRNA, PopulationCollection, ParticleCollection


class Translation(processes.Process):
    """
    Translation is instantiated in the Cell to produce proteins.

    Defines Translation process. It iterates over all ribosomes and decides what
    they should do. They either bind to mRNA or elongate/terminate a protein if
    they are already bound.

    """

    def __init__(self, name, model):
        # call the constructor of the base class (processes.Process in this case)
        super().__init__(name, model)

    def __str__(self):
        # return string output of translation process 
        # todo: each process class should define this
        return "Translation process for mRNAs: {}".format(list(self.model.states['mRNA']))

    def update(self):
        """
        Update all mrnas and translate proteins.
        """
        for mrna_id in self.model.states[MRNA].molecules:
            for mrna in self.model.states[MRNA].molecules[mrna_id]:
                #self.initiate(mrna)
                self.elongate(mrna)

    def initiate(self, mrna):
        """
        Try to bind to a given MRNA. Binding probability corresponds to the ribosome count.

        @type mrna: MRNA
        """"""
        # if not bound already and if ribosomes available
        if mrna.bindings == [] and self.model.states[Ribo].molecules['free ribos'] > 0:
            mrna.bindings.append('ribo')
            self.model.states[Ribo].take('free ribos')
            self.model.states[Ribo].add(Ribo('bound ribos'))"""

        
        #mrna.bindings = ([[0,0,[]]]*len(mrna.sequence))

        for ooo in range(int(len(mrna.sequence)/3)):
            mrna.bindings.append([0,0,[]])


          
        #print(mrna.sequence)
        #print(len(mrna.sequence)) 

        for posi in range((len(mrna.bindings))-2):
            if mrna.sequence[posi] == 'A':
                if mrna.sequence[posi +1] == 'U':
                    if mrna.sequence[posi +2] == 'G':
                        mrna.bindings[posi][0] = 1
                        break

            elif mrna.sequence[posi] == 'G':
                if mrna.sequence[posi +1] == 'U':
                    if mrna.sequence[posi +2] == 'G':
                        mrna.bindings[posi][0] = 1
                        break

            elif mrna.sequence[posi] == 'U':
                if mrna.sequence[posi +1] == 'U':
                    if mrna.sequence[posi +2] == 'G':
                        mrna.bindings[posi][0] = 1
                        break

        #print(mrna.bindings)
                        

        









    def elongate(self, mrna):
        """
        Elongate the new protein by the correct amino acid. Check if an
        MRNA is bound and if ribosome can move to next codon.
        Terminate if the ribosome reaches a STOP codon.
        """ """
        if 'ribo' in mrna.bindings:
            prot = Protein(mrna.name.lower().capitalize())  # protein names are like mRNA names, but only capitalized
            for i in range(int(len(mrna.sequence) / 3)):  # go through codons
                codon = mrna.sequence[ i:i + 3 ]
                amino_acid = database.ModelData.codon_to_amino_acid[codon]
                if amino_acid != '*':  # if STOP codon
                    prot.add_monomer(amino_acid)
                else:
                    self.model.states[ Protein ].add(prot)
                    mrna.bindings.remove('ribo')
                    self.model.states[ Ribo ].take('bound ribos')
                    self.model.states[ Ribo ].add(Ribo('free ribos'))
                    return prot """




        for _ in range(10):

            # Ribosomen binden:        
            #print(mrna.bindings)
            for pos in range((len(mrna.bindings))):
                if mrna.bindings[pos][0]==1:# wenn pos eine Startposition
                    #belege 50% der Startstellen mit ribosomen
                    #print(self.model.states[Ribo].molecules['free ribos'])
                    if mrna.bindings[pos][1]==0:
                        bindungsw=self.model.states[Ribo].molecules['free ribos']/(self.model.states[Ribo].count())
                        #print(bindungsw)
                        if random.random() < 1:#bindungsw:
                            if self.model.states[Ribo].molecules['free ribos'] > 0:
                                mrna.bindings[pos][1] = 1
                                self.model.states[Ribo].take('free ribos')
                                self.model.states[Ribo].add(Ribo('bound ribos'))
                                #print(self.model.states[Ribo].molecules['free ribos']+self.model.states[Ribo].molecules['bound ribos'])
            print(mrna.bindings)

            # für den Fall, dass Ribosom das Ende erreicht hat und kei StoP codon

            if mrna.bindings[len(mrna.bindings)-1][1] == 1:
                print('a')
                #entferne alte Riboposition 
                mrna.bindings[len(mrna.bindings)-1][1] = 0
                #setze Ribo frei
                self.model.states[Ribo].take('bound ribos')
                self.model.states[Ribo].add(Ribo('free ribos'))
                #ergenze alte Sequenz  mit Stop Base
                print(len(mrna.bindings)*3-3)
                print(len(mrna.sequence))
                AS=database.ModelData.codon_to_amino_acid[mrna.sequence[len(mrna.bindings)*3-3:len(mrna.bindings)*3]]
                mrna.bindings[len(mrna.bindings)-1][2].append(AS)

                prot = Protein(mrna.name.lower().capitalize())
                self.model.states[ Protein ].add(prot)
                return prot
                #entferne neue Riboposition 
                mrna.bindings[basenposi+1][1] = 0
                #entferne sequnz
                mrna.bindings[basenposi+1][2] = []


                '''# baue protein aus sequenz

                for i in range(int(len(mrna.bindings[len(mrna.bindings)-1][2]) / 3)):  # go through codons
                    codon = mrna.sequence[ i * 3:i * 3 + 3 ]
                    amino_acid = database.ModelData.codon_to_amino_acid[codon]
                    prot = Protein(mrna.name.lower().capitalize())  # protein names are like mRNA names, but only capitalized
                    if amino_acid != '*':  # if STOP codon
                        prot.add_monomer(amino_acid)
                    else:
                        self.model.states[ Protein ].add(prot)
                        mrna.bindings.remove('ribo')
                        self.model.states[ Ribo ].take('bound ribos')
                        self.model.states[ Ribo ].add(Ribo('free ribos'))
                        return prot

                    #lösche alten Sequenzteil aus alter Position
                    mrna.bindings[len(mrna.bindings)-1][2]=[]'''
                

            # lauf funktion

            for basenposi in range(len(mrna.bindings)-2,-1,-1): #laufe vom vorletzten bis ersten eintrag
                #print (basenposi)
                if mrna.bindings[basenposi][1] == 1:#wenn ein Ribo gebunden ist
                    #entferne alte Riboposition 
                    mrna.bindings[basenposi][1] = 0
                    #setze neue Ribosomenposition 
                    mrna.bindings[basenposi+1][1] = 1
                    #kopiere alten Sequenzteil in neuen
                    mrna.bindings[basenposi+1][2] = (mrna.bindings[basenposi][2]).copy()
                    #lösche alten Sequenzteil aus alter Position
                    mrna.bindings[basenposi][2]=[]
                    #ergenze alte Sequenz an neuer Position mit vorhergehender Base wenn keine Stopsequenz
                    AS=database.ModelData.codon_to_amino_acid[mrna.sequence[basenposi*3:basenposi*3+3]]
                    #print(mrna.sequence[basenposi*3:basenposi*3+3])
                    if AS != '*':  # if STOP codon
                         mrna.bindings[basenposi+1][2].append(AS)
                    else:
                        prot = Protein(mrna.name.lower().capitalize())
                        self.model.states[ Protein ].add(prot)
                        self.model.states[ Ribo ].take('bound ribos')
                        self.model.states[ Ribo ].add(Ribo('free ribos'))
                        return prot
                        #entferne neue Riboposition 
                        mrna.bindings[basenposi+1][1] = 0
                        #entferne sequnz
                        mrna.bindings[basenposi+1][2] = []
                        

    def terminate(self, mrna):
        """
        Splits the ribosome/MRNA complex and returns a protein.
        """
        pass
