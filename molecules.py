from copy import copy
from database import ModelData


class Molecule:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.name == other.name


class Polymer(Molecule):
    def __init__(self, name, sequence, mass_of_monomers):
        super().__init__(name)
        self.mass_of_monomers = mass_of_monomers
        self.sequence = ''
        self.bindings = []
        for monomer in sequence:
            self.add_monomer(monomer)

    def __eq__(self, other):
        return super().__eq__(other) and self.sequence == other.sequence

    def __len__(self):
        return len(self.sequence)

    def add_monomer(self, monomer):
        if monomer not in self.mass_of_monomers:
            raise ValueError('Invalid monomer {}'.format(monomer))
        self.sequence += monomer

    def calc_mass(self):
        return sum(self.mass_of_monomers[monomer] for monomer in self.sequence)


class Ribo(Molecule):
    pass


class Protein(Polymer):

    amino_acid_weights = ModelData.amino_acid_weights

    def __init__(self, name, sequence=''):
        super().__init__(name, sequence, self.amino_acid_weights)


class MRNA(Polymer):

    nucleic_acid_weights = ModelData.nucleic_acid_weights

    def __init__(self, name,sequence=''):

        super().__init__(name, sequence, self.nucleic_acid_weights)
        self.busu()

    def busu(self):
        for ooo in range(int(len(self.sequence)/3)):
            self.bindings.append([0,0,[]])


          
        #print(self.sequence)
        #print(len(self.sequence)) 

        for posi in range((len(self.bindings))-2):
            if self.sequence[posi] == 'A':
                if self.sequence[posi +1] == 'U':
                    if self.sequence[posi +2] == 'G':
                        self.bindings[posi][0] = 1
                        break

            elif self.sequence[posi] == 'G':
                if self.sequence[posi +1] == 'U':
                    if self.sequence[posi +2] == 'G':
                        self.bindings[posi][0] = 1
                        break

            elif self.sequence[posi] == 'U':
                if self.sequence[posi +1] == 'U':
                    if self.sequence[posi +2] == 'G':
                        self.bindings[posi][0] = 1
                        break



class MoleculeCollection:
    def __init__(self, molecule_type):
        self.molecule_type = molecule_type
        self.molecules = None

    def add(self, molecule):
        if not isinstance(molecule, self.molecule_type):
            raise ValueError('Expected object of type {}, received of type {}'
                             .format(self.molecule_type, type(molecule)))

    def take(self, name, number):
        pass

    def count(self, name):
        pass

    def populate(self, name, number):
        for _ in range(number):
            self.add(self.molecule_type(name))


class PopulationCollection(MoleculeCollection):
    def __init__(self, molecule_type):
        super().__init__(molecule_type)
        self.molecules = dict()

    def add(self, molecule):
        super().add(molecule)
        if molecule.name in self.molecules.keys():
            self.molecules[molecule.name] += 1
        else:
            self.molecules[molecule.name] = 1

    def take(self, name, number=1):
        assert self.molecules[name] >= number
        self.molecules[name] -= number

    def count(self, name=None):
        if name is None:
            return sum([self.molecules[name] for name in self.molecules])
        return self.molecules[name]


class ParticleCollection(MoleculeCollection):
    def __init__(self, molecule_type):
        super().__init__(molecule_type)
        self.molecules = dict()

    def add(self, molecule):
        super().add(molecule)
        if molecule.name in self.molecules.keys():
            self.molecules[molecule.name].append(copy(molecule))
        else:
            self.molecules[molecule.name] = [copy(molecule)]

    def take(self, name, number=1):
        result = []
        for _ in range(number):
            if len(self.molecules[name]) > 0:
                molecule = self.molecules[name].pop()
                result.append(molecule)

        assert number == len(result)

        return result

    def count(self, name=None):
        if name is None:
            return sum([len([x for x in self.molecules[molname]]) for molname in self.molecules])
        return len([x for x in self.molecules[name]])

    def get_molecules(self, name=None):
        if not name:
            return [molecule for molecules in self.molecules.values() for molecule in molecules]
        else:
            return self.molecules[name]
