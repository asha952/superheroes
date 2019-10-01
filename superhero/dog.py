# dog.py
class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def bark(self):
        return("Woof!")


my_dog = Dog("Rex", "SuperDog")
print(my_dog.bark())
