class Place:
    def __init__(self, id):
        self.id = id
        self.tokens = 0

    def addToken(self, amount):
        self.tokens += amount

    def removeToken(self, amount):
        self.tokens -= amount

class Transition:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.inGoing = []
        self.outGoing = []

    def addOutGoingEdge(self, place):
        self.outGoing.append(place)

    def addInGoingEdge(self, place):
        self.inGoing.append(place)

    def isEnabled(self):
        isEnabled = True
        for p in self.inGoing:
            place: Place = p
            if not place.tokens >= 1:
                isEnabled = False
        return isEnabled

    def subtractFromInGoing(self):
        for p in self.inGoing:
            place: Place = p
            place.tokens -= 1

    def addToOutGoing(self):
        for p in self.outGoing:
            place: Place = p
            place.tokens += 1

    def fire(self):
        if self.isEnabled():
            self.subtractFromInGoing()
            self.addToOutGoing()


class PetriNet:
    def __init__(self):
        self.places = {}
        self.transitions = {}

    def add_place(self, id):
        self.places.update({id: Place(id)})

    def add_transition(self, name, id):
        self.transitions.update({id: Transition(name, id)})

    def add_edge(self, source, target):
        if source > 0:
            place: Place = self.places.get(source)
            transition: Transition = self.transitions.get(target)
            transition.addInGoingEdge(place)
            return self
        else:
            place: Place = self.places.get(target)
            transition: Transition = self.transitions.get(source)
            transition.addOutGoingEdge(place)
            return self

    def get_tokens(self, place):
        return self.places.get(place).tokens

    def is_enabled(self, transition):
        transition: Transition = self.transitions.get(transition)
        return transition.isEnabled()

    def add_marking(self, place):
        self.places.get(place).addToken(1)

    def fire_transition(self, t):
        if self.is_enabled(t):
            transition: Transition = self.transitions.get(t)
            transition.fire()


if __name__ == '__main__':
    p = PetriNet()

    p.add_place(1)  # add place with id 1
    p.add_place(2)
    p.add_place(3)
    p.add_place(4)
    p.add_transition("A", -1)  # add transition "A" with id -1
    p.add_transition("B", -2)
    p.add_transition("C", -3)
    p.add_transition("D", -4)

    p.add_edge(1, -1)
    p.add_edge(-1, 2)
    p.add_edge(2, -2).add_edge(-2, 3)
    p.add_edge(2, -3).add_edge(-3, 3)
    p.add_edge(3, -4)
    p.add_edge(-4, 4)

    print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

    p.add_marking(1)  # add one token to place id 1
    print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

    p.fire_transition(-1)  # fire transition A
    print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

    p.fire_transition(-3)  # fire transition C
    print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

    p.fire_transition(-4)  # fire transition D
    print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

    p.add_marking(2)  # add one token to place id 2
    print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

    p.fire_transition(-2)  # fire transition B
    print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

    p.fire_transition(-4)  # fire transition D
    print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

    # by the end of the execution there should be 2 tokens on the final place
    print(p.get_tokens(4))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

#False False False False
#True False False False
#False True True False
#False False False True
#False False False False
#False True True False
#False False False True
#False False False False
#2
