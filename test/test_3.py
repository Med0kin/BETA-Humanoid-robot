def my_deccorator(func):
    def wrapper():
        print('wrapper of decorator')
        func()
    return wrapper

def my_dec2(func):
    def wrapper():
        print('wrapper of decorator 2')
        func()
    return wrapper

@my_dec2
@my_deccorator
def myfunc():
    print('myfunc')

if __name__ == "__main__":

    myfunc()
