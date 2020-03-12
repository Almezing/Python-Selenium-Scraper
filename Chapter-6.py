"""
Chapter 6: Objects and Classes
    Everything is an object. Objects contains both data (varables called attributes) and code (functions called methods)

    __init__
        Python object initialization method that initiales an individual object from its class definition. 
    self
        An argument that specifies that it referes to the individual object itself
    Inheritance
        Create a new class from an existing class but with some addtions or changes. The existing class is know as a parent, superclass, or a base class. The new class created is know as a child, subclass, or derived class. These subclasses are specilized verions of the superclass

    Override a Method
        Subclasses can change the the methods derived the superclass.

    Add A Method
        Subclasess can add into themselves methods not found in their superclasses

    super()
        Ensure the parent class methods/attributes are passed to the child

    Getter and Setter values and Properties
        All attributes and methods are public

    @Decorators can be used intead of getter/setter methods

    Can use ( __ ) in front of property name to have them semi-private

    Method types 
        Instance method: methds that are normally used when creating classes
        Class method: method that affect a class as a whole and its objects
            this method is preceded by the decorator " @classmethod "
            and the first paremeter for the method is " cls " (stands for class)
        Static method: method that does not affect the class nor its objects. " @staticmethod ". Good for testing

    Duck Typing
        Loose implemenation of polymorphism; apply the same operations to different objects regardless of their class

    Special Methods (magic methods) : __( something )__ 
        Like __init__
        
    Aggregation and Composition
        Both mean the same thing; a structure that adds to an existing strucutre. Duck class with seperate Bill and Tail classes. 
        Used to express relationship, but the classes independent

    Use for simplicity
    Primitive data types > Modules > Classes

    Named Tuples ( form collections )
        Subclass of tuples that are accessible by name (.name accessor) and by position ( with [offset] )
"""


"""
* Loops up the definition of the Person class
* Instantiates (creates) a new object in the memory
* Calls the object's __init__ methd, passing this newly-created object as self and the other argmuent ("Person's Name") as name
* Stores the value of name in the object
* Returns the new object
* Attaches the name hunter to the object
"""

class Person():
    def __init__(self, name):
        self.name = name

# Inheritance example
# Worker is subclass of the Person class
# 
# Worker class overroad the Person __init__ method
# but super() explicitly calls the parent class and uses the parants __init__ method to handle the child name argument

class Worker(Person):
    def __init__(self, name, id):
        super().__init__(name)
        self.id = id
    pass

employee = Worker("Ken", 22)
# print(employee.name, employee.id)


class Cat():
    def __init__(self, input_name):
        self.hidden_name = input_name

    def get_name(self):
        print('getter method')
        return self.hidden_name
    #if set_name() is explicitly called, it returns None
    def set_name(self, input_name):
        print('setter method')
        self.hidden_name = input_name

    name = property(get_name, set_name)

tabby = Cat('Ted')
print(tabby.name)
print(tabby.set_name("Teddy"))
print(tabby.get_name())
tabby.name = "Mel"
print(tabby.name)

# Define Properties with the use of @decorators
class Dog():
    def __init__(self, input_name):
        self.hidden_name = input_name
    @property
    def name(self):
        print('getter method')
        return self.hidden_name
    #if set_name() is explicitly called, it returns None
    @name.setter
    def name(self, input_name):
        print('setter method')
        self.hidden_name = input_name

good_boy = Dog("Loki")

print(good_boy.name)
good_boy.name = "Tom"
print(good_boy.name)


#Computed value property

class Circle():
    def __init__(self, radius):
        self.radius = radius
    @property
    def diameter(self):
        return 2 * self.radius

c = Circle(3)
print(c.diameter)

# Making class attributes almost-private using "__" (double underscore) at the beginning of the name

class Bird:
    def __init__(self, input_name):
        self.__name = input_name

    @property
    def name(self):
        print('getter method')
        return self.__name

    @name.setter 
    def name (self, input_name):
        print('setter method')
        self.__name = input_name

bird1 = Bird("Street Rat")

print(bird1.name)
print(bird1._Bird__name)

# Class Method
class A():
    count = 0
    def __init__(self):
        A.count += 1

    def exclaim(self):
        print("I'm an A")

    @classmethod
    def kids(cls):
        print(f"A has {cls.count} objects")

one_a = A()
two_a = A()
three_a = A()
A.kids()
# print(A.count)

# Static method
class StaticBoi():
    @staticmethod
    def method():
        print("Printed from a Static Method")
# Access the method directly without creating an instance of StaticBoi
StaticBoi.method() 

# Duck typing - loose polymorphism

class Quote():
    def __init__(self, person, words):
        self.person = person
        self.words = words
    def who(self):
        return self.person
    def says(self):
        return self.words + '.'

class QuestionQuote(Quote):
    def says(self):
        return self.words + '?'
class ExclamationQuote(Quote):
    def says(self):
        return self.words + '!'

amazon_bald_guy = Quote("Jeff Bezos", "I want spaceships now")
amazon_worker = QuestionQuote("Liam", "Can I pee")
amazon_manager = ExclamationQuote("Tom", "No")

print(amazon_bald_guy.who(), "says:" ,amazon_bald_guy.says())
print(amazon_worker.who(), "says:" ,amazon_worker.says())
print(amazon_manager.who(), "says:" ,amazon_manager.says())

class Babbler():
    def who(self):
        return 'Brook'
    def says(self):
        return 'Babble'
brook = Babbler()

def who_says(obj):
    print(obj.who(), 'says:', obj.says())

who_says(brook)
who_says(amazon_bald_guy)

# Special Methods

class Word():
    def __init__(self, text):
        self.text = text
    # using the special method __eq__
    # def equals(self, word2):
    def __eq__(self, word2):
        return self.text.lower() == word2.text.lower()
    def __str__(self):
        return self.text
    def __repr__(self):
        return f" Word(' {self.text} ')"

first_word = Word('ha')
second_word = Word('HA')
third_word = Word('ah')

# print(first.equals(second))
# print(first == second)
first_word

# Aggregation/Composition
class Rims():
    def __init__(self, description):
        self.description = description
class Spoiler():
    def __init__(self, spoiler_type):
        self.spoiler_type = spoiler_type

class Car():
    def __init__(self,rims,spoiler_type):
        self.rims = rims
        self.spoiler_type = spoiler_type

    def about(self):
        print(f"""
                This car has {self.rims.description} rims and a {self.spoiler_type.spoiler_type} spoiler
            """)

a_rims = Rims('fancy')
a_spoiler = Spoiler('low')

my_car = Car(a_rims, a_spoiler)
my_car.about()

# Named Tuples
"""
Pros/Cons
It looks and acts like an immutbale object
It is more space- and time-efficient than objects
You can access attributes by using dot notation instead of dictionary-style square brackets
You can use it as a dictionary key
"""
from collections import namedtuple
Phoney_Class = namedtuple('Phone','Brand Color')
phone1 = Phoney_Class("Samsung","Black")
print(phone1)
# Named Tuples from a dict
parts = {'Brand':'Apple','Color': 'White'}
phone2 = Phoney_Class(**parts)
print(phone2)

"""
Excercises

"""

#6.1
class Thing():
    pass

example = Thing()

print(Thing)
print(example)

#6.2
class Thing2():
    def __init__(self, letters):
        self.letters = letters
        print(letters)

Thing2('abc')

# 6.3
class Thing3():
    def __init__(self,letters):
        self.letters = letters

thing3_object = Thing3('xyz')

print(thing3_object.letters)

# 6.4
class Element():
    def __init__(self, name, symbol,number):
        # self.name = name
        # self.symbol = symbol
        # self.number = number
        # for 6.8
        self.__name = name
        self.__symbol = symbol
        self.__number = number
    # for 6.6
    # def dump(self):
    #     print(f"{self.name} {self.symbol} {self.number}")
    # for 6.7
    # def __str__(self):
    #     return f"{self.name} {self.symbol} {self.number}"
    #  for 6.8
    def get_name(self):
        return self.__name
    def get_symbol(self):
        return self.__symbol
    def get_number(self):
        return self.__number

element1 = Element('Hydrogens','H',1)

# 6.5
proto_element = {'name': 'Hydrogen', 'symbol':'H', 'number':1}
hydrogen = Element(**proto_element)

# 6.6
# hydrogen.dump()

# 6.7
# print(hydrogen)

# 6.8
# print(hydrogen.get_name())
# print(hydrogen.get_symbol())
# print(hydrogen.get_number())

# 6.9
class Bear():
    def eats(self):
        return 'berries'

class Rabbit():
    def eats(self):
        return 'clover'

class Octothorpe():
    def eats(self):
        return "people"

def eats_what(obj):
    print(obj.eats())


good_bear = Bear()
good_rabbit = Rabbit()
uh_octo = Octothorpe()

eats_what(good_bear)
eats_what(good_rabbit)
eats_what(uh_octo)

# 6.10

class Laser():
    def does(self):
        return 'disintegrate'
class Claw():
    def does(self):
        return 'slash'
class Smartphone():
    def does(self):
        return 'ring'

class Robot():
    def __init__(self):
        self.laser = Laser()
        self.claw = Claw()
        self.smartphone = Smartphone()
    def does(self):
        print(f"{self.laser.does()} {self.claw.does()} {self.smartphone.does()}")

# robo = Robot(robo_laser,robo_claw,robo_phone)
robo = Robot()
robo.does()