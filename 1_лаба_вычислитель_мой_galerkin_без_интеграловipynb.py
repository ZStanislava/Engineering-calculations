# -*- coding: utf-8 -*-
"""1 лаба вычислитель МОЙ Galerkin-без интеграловipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1caMG2xDifn34Eml6xanGH0Cc30y8gsBT
"""

import matplotlib.pyplot as plt
import numpy as np
import math

a = (0.0, 0.3, 0.8, 1.20)
h = 0.1

A1 = 0
A2 = int((a[1] - a[0]) / h)
A3 = int((a[2] - a[0]) / h)
A4 = int((a[3] - a[0]) / h)

Ja = 0.7
Ub = 10.5
N = 10


def p(x):
    if x < a[1]:
        return 3.1
    elif x < a[2]:
        return 0.7
    else:
        return 2
    
def q(x):
    if x < a[1]:
        return 1
    elif x < a[2]:
        return 2
    else:
        return 1.5

def f1(x):
    return math.log(2+x)

def f2(x):
        return 20*math.log(2+x)

def f3(x):
    return math.log(1+x)

def f(x):
    if x < a[1]:
        return f1(x)
    elif x < a[2]:
        return f2(x)
    elif x < a[3]:
        return f3(x)

def ej(x,xi): #если ломается, то вместо зубчика пишем 1/2
    if x >= xi-h and x < xi:
        return (x-(xi-h))/(xi-(xi-h))
    elif x >= xi and x < xi +h:
        return ((xi+h) - x) / ((xi+h) - xi)
    else: return 0

def g1(f,x,xi):
    return f*ej(x,xi)

def g2(f,x, xi):
    return f*ej(x,xi)

def F(i,x): # x - это массив :)
    if i ==0:
        g11 = g1(f1((x[i] + x[i+1])/2),(x[i] + x[i+1])/2,x[i]) 
        return (g11)*h - Ja
    
    elif i < A4:
        return h/2*(f((x[i-1] + x[i])/2) + f((x[i] + x[i+1])/2)) 

    else:
        return Ub

def K(j, i, x):
    if( i == j):
        if j == 0:
            return p((x[0] + x[1]) / 2)/(x[1] - x[0])
        elif (j == (N+1)):
            return p((x[N] + x[N+1])/2)/(x[N+1] - x[N])
        return p((x[j-1] + x[j]) / 2) / (x[j] - x[j-1]) + p((x[j] + x[j+1]) /2) / (x[j+1] - x[j])
    elif i == j-1:
            return p((x[j] + x[j-1]) / 2) / (x[j-1] - x[j])
    else:
        return p((x[j] + x[j+1]) / 2) / (x[j] - x[j+1])

def M(j, i, x):
    if i == j:
        if j ==0:
            return 1/3 * q((x[0] + x[1]) / 2) * (x[1] - x[0])
        elif j == N+1:
            return 1/3 + q((x[N] + x[N+1])/2) * (x[N+1] - x[N])
        return 1/3*(q((x[j-1] + x[j])/2)*(x[j] - x[j-1]) + q((x[j+1] + x[j])/2)*(x[j+1] - x[j]))
    elif i == j -1:
        return q((x[j-1] + x[j]) / 2) * (x[j] - x[j-1]) / 6
    else:
        return q((x[j] + x[j+1]) / 2) * (x[j+1] - x[j]) / 6

def Solve():
    global A1,A2,A3,A4
    A1 = 0
    A2 = int((a[1] - a[0]) / h)
    A3 = int((a[2] - a[0]) / h)
    A4 = (a[3] - a[0]) / h
    global N
    if(h == 0.1):
      A4 = int((a[3] - a[0]) / h) + 1
    N = int(A4 - 1)
    x = [0]*int((N+2))
    for i in range(N+2):
        x[i] = a[0] + i*h
    _a = [0]*(N+2)
    _b = [0]*(N+2)
    _c = [0]*(N+2)
    for i in range(1,N+1):
        _a[i] = K(i,i-1, x) + M(i,i-1,x)
        _b[i] = K(i,i,x) + M(i,i,x)
        _c[i] = K(i,i+1,x) + M(i,i+1,x)
    
    _b[0] = K(0,0,x) + M(0,0,x)
    _c[0] = K(0, 1, x) + M(0,1,x)
    _a[N+1] = 0 
    _b[N+1] = 1 

    alpha = [0]*(N+2)
    betta  = [0]*(N+2)
    alpha[0] = -1*_c[0] / _b[0]
    betta[0] = F(0,x) / _b[0]  # F
    for i in range(1,N+1):
        alpha[i] = -1*_c[i] / (_a[i]*alpha[i-1] + _b[i])
        betta[i] = (F(i,x) - _a[i] * betta[i-1]) / (_a[i]*alpha[i-1] + _b[i])

    U = [0]*(N+2)
    U[N+1] = (F(N+1,x) - _a[N+1]*betta[N]) / (_a[N+1]* alpha[N] + _b[N+1])
    for i in range(N,-1,-1):
        U[i] = alpha[i] * U[i+1] + betta[i]
    return x, U

def make_dU(X, U, h):
    dU = np.array([])
    p = [3.1,0.7,2]
    for i in range(len(U)-1):
        if X[i] < a[1]:
            dU = np.append(dU, -p[0]*(U[i+1]-U[i])/h)
        elif (X[i] < a[2]):
            dU = np.append(dU, -p[1]*(U[i+1]-U[i])/h)
        else:
            dU = np.append(dU, -p[2]*(U[i+1]-U[i])/h)
    return dU


def compare_left_side(U, h):
    p=3.1
    Ja=0.7
    n = len(U)-2
    return abs(p*(U[1]-U[0])/h - Ja)     #p(a)u'(a)-J(a)=delta

def main():
    global h 
    x, U = Solve()

    fig, ax = plt.subplots(nrows=1, ncols=2)
    ax1, ax2 = ax.flatten()
    ax1.plot(x,U)
    ax1.grid()
    ax2.hlines(make_dU(x,U,h), [x[i] for i in range(len(x)-1)],[x[i]+h for i in range(len(x)-1)] , color = 'blue')
    delta1 = compare_left_side(U, h)

    h = 0.01
    x1, U1 = Solve()
    ax1.plot(x1,U1, color = 'red') #
    ax2.hlines(make_dU(x1,U1,h), [x1[i] for i in range(len(x1)-1)],[x1[i]+h for i in range(len(x1)-1)] , color = 'red')
    plt.show()
    
    delta2 = compare_left_side(U1, h)
    print(f"delta1= {delta1}")                
    print(f"delta2= {delta2}")
if __name__ == '__main__':
    main()