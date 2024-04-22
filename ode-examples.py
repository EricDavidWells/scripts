from scipy.integrate import ode
from matplotlib import pyplot as plt


# generic mass spring damper simulation
def mass_spring_damper_example():
    k = 3
    c = 2
    m = 1

    wn = (k/m)**0.5
    eta = c/(2*m*wn)

    y0 = [1, 0]
    t0 = 0
    t1 = 5
    dt = 0.1

    def f (t, y):
        dydt = []
        dydt = [y[1], -2*eta*wn*y[1] - wn*wn*y[0]]
        return dydt


    r = ode(f).set_integrator('vode', method='bdf')
    r.set_initial_value(y0, t0)

    t = []
    x = []
    dx = []

    while r.successful() and r.t < t1:
        y = r.integrate(r.t+dt)
        
        t.append(r.t)
        x.append(r.y[0])
        dx.append(r.y[1])
        print(y)

    plt.figure()
    plt.plot(t, x, label='x')
    plt.plot(t, dx, label='dx')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    mass_spring_damper_example()