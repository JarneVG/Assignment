from casadi import *
import matplotlib.pyplot as plt

x = MX.sym('x', 5, 1) # Symbolic
y = MX(2, 1) # Y should be an expression to not make it free

y[0] = x[0] + x[1] * x[2]
y[1] = sumsqr(x[2:])

f = Function('f', [x], [y])
print(f)
print(f([1, 2, 3, 4, 5]))

# Once f is made, mofifying y has no effect on f
y[0] = 0
print(f([1, 2, 3, 4, 5]))


# Algorithmic differentiation
J = Function('J', [x], [jacobian(f(x), x)])
print(J)
print(J([1, 2, 3, 4, 5]))
print(J([0, 0, 0, 0, 0])) # 00 is different from 0

H = Function('H', [x], [hessian(transpose(f(x)) @ f(x), x)[0]])
print(H)
print(H([1, 2, 3, 4, 5]))





## Opti hides these gradients etc and just does optimzation for you
opti = Opti()

x = opti.variable(1, 1)
y = opti.variable(1, 1)
p = opti.parameter(1, 1)

opti.subject_to( x**2 + y**2 == 1 )
opti.subject_to( y >= p )
opti.subject_to( y>= 2*x )

opti.minimize( (1-x)**2 + (y-x**2)**2)
opti.solver("ipopt")

opti.callback(lambda i, v: print(f"Iteration {i}"))

sol = opti.solve()


