from scipy.integrate import ode
from matplotlib import pyplot as plt
import numpy as np
from math import sin, cos, pi

M = 1.0
t_final = 5
dt = 0.001

latency_time = 0.1         # desired latency in seconds
latency_steps = int(round(latency_time / dt))

kp = 20
kd = 2*(kp*M)**0.5
ki = 0

# basic mass / force simulation

def euler_update(x, xdot, F):

    xddot = F/M
    xdot_new = xdot + xddot * dt
    x_new = x + xdot * dt

    return x_new, xdot_new


def control_law(e, edot, kp, kd, ki):

    if not hasattr(control_law, "accum"):
            control_law.accum = 0  # initialize only once

    control_law.accum += e * dt

    return e*kp + edot*kd + control_law.accum * ki


if __name__ == "__main__":

    # ——— define your three xdesired profiles ———
    profiles = {
        'Step (at t>1s)' :    lambda t: np.where(t > 1.0, 1.0, 0.0),
        'Linear (0→10)' :     lambda t: (t / t[-1]) * 10.0,
        'Sine (amp=10)' :      lambda t: np.sin(t*2*pi*2) * 10.0,
    }

    # time vector
    t = np.arange(0, t_final + dt, dt)

    # storage for results
    results = {}

    for name, profile in profiles.items():
        xdes = profile(t)
        xdotdes = np.zeros_like(t)
        xact    = np.zeros_like(t)
        xdotact = np.zeros_like(t)

        # reset integrator
        control_law.accum = 0.0

        # simulate no–latency run
        for i in range(1, len(t)):
            e    = xdes[i-1]    - xact[i-1]
            edot = xdotdes[i-1] - xdotact[i-1]
            F    = control_law(e, edot, kp, kd, ki)
            xact[i], xdotact[i] = euler_update(xact[i-1], xdotact[i-1], F)

        # simulate with latency
        control_law.accum = 0.0
        xact_lat    = np.zeros_like(t)
        xdotact_lat = np.zeros_like(t)
        for i in range(latency_steps, len(t)):
            e    = xdes[i-latency_steps]    - xact_lat[i-1]
            edot = xdotdes[i-latency_steps] - xdotact_lat[i-1]
            F    = control_law(e, edot, kp, kd, ki)
            xact_lat[i], xdotact_lat[i] = euler_update(xact_lat[i-1], xdotact_lat[i-1], F)

        results[name] = (xdes, xact, xact_lat)

    # ——— Plotting in 3×1 subplots ———
    fig, axes = plt.subplots(3, 1, figsize=(8, 10), sharex=True)

    for ax, (name, (xdes, xact, xact_lat)) in zip(axes, results.items()):
        ax.plot(t,    xdes,     label='xdesired')
        ax.plot(t,    xact,     label='xactual_zero_latency')
        ax.plot(t,    xact_lat, label='xactual_with_latency')
        ax.set_title(name)
        ax.legend(loc='upper right')
        ax.grid(True)

    axes[-1].set_xlabel('Time [s]')
    plt.tight_layout()
    plt.show()
