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
                self.initiate(mrna)
                self.elongate(mrna)

    def initiate(self, mrna):
        """
        Try to bind to a given MRNA. Binding probability corresponds to the ribosome count.

        @type mrna: MRNA
        """
        """
        # Ribo binds with certain chance
        # if not bound already and if ribosomes available


        # wenn anzahl der gebundenen ribosomen weniger sind als maximal gebunden werden können
        # kann ich noch ein ribosomen binden aber nur wenn auch position0 frei oder nur nach 2schritten vorbei
        if self.model.timestep%2 == 0:# es kann nur in jeden zweiten Zeitschritt ein neues Ribo binden
            if mrna.bindings == [] and self.model.states[Ribo].molecules['free ribos'] > 0:
                if random.random() < 0.8:
                    mrna.bindings.append('ribo')
                    self.model.states[Ribo].take('free ribos')
                    self.model.states[Ribo].add(Ribo('bound ribos'))
            #print (mrna.bindings)
            #print (mrna.sequence)
        """
        mrna.bindings = ([[0,0,[]]]*len(mrna.sequence))
        #print (mrna.bindings)
        print (mrna.sequence)

        for posi in range((len(mrna.bindings))-2):
            if mrna.sequence[posi] == 'A':
                if mrna.sequence[posi +1] == 'U':
                    if mrna.sequence[posi +2] == 'G':
                        mrna.bindings[posi]= [1,0,[]]
                        #mrna.bindings[posi+1]=1
                        #mrna.bindings[posi+2]=1
            elif mrna.sequence[posi] == 'G':
                if mrna.sequence[posi +1] == 'U':
                    if mrna.sequence[posi +2] == 'G':
                        mrna.bindings[posi]=[1,0,[]]
                        #mrna.bindings[posi+1]=1
                        #mrna.bindings[posi+2]=1
            elif mrna.sequence[posi] == 'U':
                if mrna.sequence[posi +1] == 'U':
                    if mrna.sequence[posi +2] == 'G':
                        mrna.bindings[posi]=[1,0,[]]
                        #mrna.bindings[posi+1]=1
                        #mrna.bindings[posi+2]=1
        # alles für erste Base
        #print (mrna.bindings[0][0])#listen eintrag  startposition?            
        #print (mrna.bindings[0][1])#listen eintrag  ribosomen gebunden?
        #print (mrna.bindings[0][2])#listen eintrag  liste des translationscodes

        # Ribosomen binden:
        if self.model.states[Ribo].molecules['free ribos'] > 0:
            for pos in range((len(mrna.bindings))-2):
                if mrna.bindings[pos][0]==1:# wenn pos eine Startposition
                    #belege 50% der Startstellen mit ribosomen
                    if random.random() < 0.5:
                        mrna.bindings[pos][1] = 1
                        self.model.states[Ribo].take('free ribos')
                        self.model.states[Ribo].add(Ribo('bound ribos'))


        # alles für erste Base
        #print (mrna.bindings[0][0])#listen eintrag  startposition?            
        #print (mrna.bindings[0][1])#listen eintrag  ribosomen gebunden?
        #print (mrna.bindings[0][2])#listen eintrag  liste des translationscodes
        print (mrna.bindings)#listen eintrag  startposition?            
        



    def elongate(self, mrna):
        """
        Elongate the new protein by the correct amino acid. Check if an
        MRNA is bound and if ribosome can move to next codon.
        Terminate if the ribosome reaches a STOP codon.
        """
        """
        if 'ribo' in mrna.bindings:
            #print (mrna.name)
            prot = Protein(mrna.name.lower().capitalize())  # protein names are like mRNA names, but only capitalized
            
            start = False

            for i in range(int(len(mrna.sequence) / 3)):  # go through codons

                codon = mrna.sequence[ i*3 : i*3+3 ]
                amino_acid = database.ModelData.codon_to_amino_acid[codon]
                #print(codon)
                #if amino_acid == 'M': # reached Start-Codon
                    #start = True
                if amino_acid != '*': #and start == True:  # if STOP codon
                    prot.add_monomer(amino_acid)#wenn kein stop-codon , dann appende AS an protein
                    #print(prot.sequence)

                elif amino_acid == '*':
                    self.model.states[ Protein ].add(prot)
                    mrna.bindings.remove('ribo')
                    self.model.states[ Ribo ].take('bound ribos')
                    self.model.states[ Ribo ].add(Ribo('free ribos'))

                    return prot
        """
        for _ in range(1):
            # Stop Fkt. noch nicht fertig und auch noch nicht in initialisierung

            #hier muss dann der mittelteil von elonge rein




            # lauf funktion

            for basenposi in range(len(mrna.bindings)-1,-1,-1): #laufe vom vorletzten bis ersten eintrag
                #print (basenposi)
                if mrna.bindings[basenposi][1] == 1:#wenn ein Ribo gebunden ist
                    #entferne alte Riboposition 
                    mrna.bindings[basenposi][1] = 0
                    #setze neue Ribosomenposition 
                    mrna.bindings[basenposi+1][1] = 1
                    #kopiere alten Sequenzteil in neuen
                    mrna.bindings[basenposi+1][2] = mrna.bindings[basenposi][2]
                    #lösche alten Sequenzteil aus alter Position
                    mrna.bindings[basenposi][2]=[]
                    #ergenze alte Sequenz an neuer Position mit vorhergehender Base
                    mrna.bindings[basenposi+1][2].append(mrna.sequence[basenposi])

            # alles für erste Base
        print (mrna.bindings)        
        



                    
    def terminate(self, mrna):
        """
        Splits the ribosome/MRNA complex and returns a protein.
        """
        pass
