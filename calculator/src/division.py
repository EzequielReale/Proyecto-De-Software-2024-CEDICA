def division(a,b):
    try :
        return a / b
    except ZeroDivisionError :
        print('Error : division por cero')
        return 0
    
#if __name__ == "__main__":
    #print(division(1, 0))