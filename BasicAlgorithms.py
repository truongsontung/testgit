# Bài 01: Viết một chương trình Python in ra dãy số Fibonacci
# Gợi ý:
# Sử dụng đệ quy
# Không sử dụng đệ quy
def fibonacci_nonRecur(n):
    """
    ham tra ve list [] day so fibonacci f0,f1,f2,.....fn
    ham su dung vong lap for tinh va nap cac gia tri vao list []
    n<0 tra ve [-1]
    fibonacci_nonRecur(10) = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    """
    fib=[]
    if n <0:
        return [-1]
    if n == 0:
        return [0]
    elif n==1:
        return [0,1]
    else:
        fib=[0,1]
        for i in range(2,n+1):      
            fib.append(fib[i-1]+fib[i-2])
        return fib
def fibonacci_Recur(n):
    """
    ham tra ve list [] day so fibonacci f0,f1,f2,.....fn
    ham su dung de quy tinh va nap cac gia tri vao list []
    n<0 tra ve [-1]
    fibonacci_Recur(10) = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    """
    fib=[0,1]
    def __run_Recur(i):
        if n<0:
            return [-1]
        elif n==0:
            return [0]
        elif n==1:
            return [0,1]
        else:
            if i==n+1:
                return fib
            else:
                fib.append(fib[i-1]+fib[i-2])
                return __run_Recur(i+1)
    
    return __run_Recur(2)
if __name__=="__main__":
    print(fibonacci_nonRecur.__doc__)
    print(fibonacci_nonRecur(38))
    print(fibonacci_Recur.__doc__)
    print(fibonacci_Recur(38))
    #39088169