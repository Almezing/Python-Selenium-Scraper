def problem_41():
    # 4.1 Assign the value 7 to the variable guess_me. 
    # Then, write the conditional tests (if,else, and elif) 
    # to print the string 'too low' if guess_me is less than 7, 
    # 'too high' ifgreater than 7, and 'just right' if equal to 7.
    # 
    # 4.2 Assign the value 7 to the variable guess_me 
    # and the value 1 to the variable start. 
    # Write a while loop that compares start with guess_me. 
    # Print too low if start is lessthan  guess me.  
    # if  start  equals  guess_me,  print  'found it!'  
    # and  exit  the  loop.  Ifstart  is  greater  than  guess_me,  
    # print  'oops'  and  exit  the  loop.  Increment  start  atthe end of the loop.
    guess_me = 7
    start = 1

    while True:
        try:
            # guess_attempt = int(input("Guess the number:"))
            if start > guess_me:
                print(f"{start} how?")
            elif start < guess_me:
                print(f"{start} Too low")
            elif start == guess_me:
                print(f"{start} Is right")
                break
            else:
                print("Nice Try")
                break
        except ValueError:
            print("Whole numbers only")
            pass
        start = start + 1


def problem_43():
    # 4.3 Use a for loop to print the values of the list [3, 2, 1, 0].
    for member in list(range(3, -1, -1)):
        print(member)


def problem_44():
    # 4.4 Use a list comprehension to make a list of the even numbers in range(10)
    even_numbers = [number for number in range(10) if number % 2 == 0]
    print(even_numbers)


def problem_45():
    # 4.5 Use a dictionary comprehension to create the dictionary squares. 
    # Use range(10)to return the keys, and use the square of each key as its value.
    squares = {number: number * number for number in range(10)}
    print(squares)


def problem_46():
    # 4.6  Use  a  set  comprehension  to  create  the  set  odd  from  the  odd  numbers  inrange(10)
    odd = set(number for number in range(10) if number % 2 != 0)
    print(odd)


def problem_47():
    # 4.7 Use a generator comprehension to return the string 'Got ' 
    # and a number for thenumbers in range(10). Iterate through this by using a for loop
    got_generator = (number for number in range(10))
    for member in got_generator:
        print("Got ", member)


def problem_48():
    # 4.8  Define  a  function  called  good  that  returns  the  list  ['Harry',  'Ron',  'Hermione']
    def good():
        return ["Harry", "Ron", "Hermione"]

    print(good())


def problem_49():
    # Define  a  generator  function  called
    # get_odds  that  returns  the  odd
    # numbers from range(10). Use a for loop to
    # find and print the third value returned.
    def get_odds(first=0, last=10, step=1):
        number = first
        while number < last:
            if number % 2 != 0:
                yield number
            number += step

    odd_numbers = get_odds(1, 10)
    for member in odd_numbers:
        print(member)


def problem_410():
    #Decorators are weird
    # 4.10 Define a decorator called test that prints
    # 'start' when a function is called and'end' when it finishes

    def test(func):
        def inner_func(*args, **kwargs):
            print("Start")
            print(func.__name__)
            func(*args, **kwargs)
            print("End")
            # return bulge

        return inner_func

    # fast way to document a function
    # and can stack
    # other way:
    #####   var = document_it(func)
    #####   var()
    @test
    def some_func():
        print('Some funk')
        
    # some_func()

    # some_func_info = test(some_func)
    # some_func_info()

def problem_411():
    #  Define an exception called OopsException. 
    # Raise this exception to see what hap‐pens. 
    # Then write the code to catch this exception 
    # and print 'Caught an oops'

    class OopsException(Exception):
        pass

    try:
        raise OopsException('oopse')
    except OopsException as exc:
        print('Did an oopsie', exc)

def problem_412():
    titles =['Creature of Habit', 'Crewel Fate'] 
    plots = ['A nun turns into a monster', 'A haunted yarn shop']

    movies = {title:plot for title,plot in zip(titles,plots)}

    print(movies)

def main():
    # problem_41()
    # problem_43()
    # problem_44()
    # problem_45()
    # problem_46()
    # problem_47()
    # problem_48()
    # problem_49()
    # problem_410()
    # problem_411()
    problem_412()



if __name__ == "__main__":
    print(__name__)
    main()

