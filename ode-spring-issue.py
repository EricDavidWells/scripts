import numpy as np
import matplotlib.pyplot as plt

# System parameters
m = 1.0   # Mass (kg)
k = 10.0  # Spring constant (N/m)
b = 2.0   # Damping coefficient (Ns/m)

# Simulation parameters
dt_sim = 0.0001  # Simulation timestep (1 ms)
dt_ctrl = 0.01  # Control update timestep (10 ms)
t_final = 50.0   # Total simulation time

# PD Controller gains
Kp = 100.0  # Proportional gain
Kd = 0.0     # Derivative gain

# Initial conditions
x0 = 1.0   
xdot0 = 1.0  

# Control update times
control_update_times = np.arange(0, t_final + dt_ctrl, dt_ctrl)
current_control_index = 0  
last_force = (-Kp * x0 - Kd * xdot0)  # Initially computed control force
control_values = {}  

def get_control_input(t, x, xdot):
    """
    Update the restoring force only at discrete control times.
    """
    global last_force, current_control_index

    if current_control_index < len(control_update_times) - 1:
        next_control_time = control_update_times[current_control_index + 1]
        if t >= next_control_time:
            # predict where x will be in half a sample of time
            # do I have to assume a mass for that? seems like yes

            # f1 = last_force/m
            # rk_xdot = xdot + f1*dt_sim/2
            # rk_x = x + rk_xdot * dt_sim/2
            # f2 = get_control_input(t+dt_sim/2, rk_x, rk_xdot)

            # xdot += f2 * dt_sim
            # x += xdot * dt_sim

            f1 = last_force/m # use estimated acceleration here? this would be super noisy
            rk_xdot_predicted_in_half_step = xdot + f1*dt_ctrl/2
            rk_x = x + rk_xdot_predicted_in_half_step * dt_ctrl/2
            f2 = -Kp * rk_x - Kd * rk_xdot_predicted_in_half_step
            xdot_pred = xdot + f2 * dt_ctrl
            x_pred = x + xdot_pred * dt_ctrl

            # Compute restoring force at control update time
            # last_force = -Kp * x - Kd * xdot
            last_force = -Kp * x_pred - Kd * xdot_pred

            current_control_index += 1  # Move to next update step
            control_values[next_control_time] = last_force  # Store history

    return last_force

# Euler Integration to solve the system
def euler_integration():
    # Initial conditions
    t = 0.0  # Start time
    x = x0   # Initial position
    xdot = xdot0  # Initial velocity

    # Arrays to store results
    time_vals = [t]
    x_vals = [x]
    xdot_vals = [xdot]
    
    # Perform Euler integration
    while t < t_final:
        u = get_control_input(t, x, xdot)  # Get control force
        
        # System dynamics: m * xddot = -kx - b*xdot + u        
        # update using runge kutta 2
        f1 = u/m
        rk_xdot = xdot + f1*dt_sim/2
        rk_x = x + rk_xdot * dt_sim/2
        f2 = get_control_input(t+dt_sim/2, rk_x, rk_xdot)

        xdot += f2 * dt_sim
        x += xdot * dt_sim
        
        # Update time
        t += dt_sim
        
        # Store results for plotting
        time_vals.append(t)
        x_vals.append(x)
        xdot_vals.append(xdot)
    
    return np.array(time_vals), np.array(x_vals), np.array(xdot_vals)

# Run Euler Integration
t_vals, x_vals, xdot_vals = euler_integration()

# Extract control values for plotting (sorted by time)
control_times, u_vals = zip(*sorted(control_values.items()))

# Plot results
plt.figure(figsize=(10, 5))

# Plot Position and Velocity
plt.subplot(2, 1, 1)
plt.plot(t_vals, x_vals, label="Position (x)")
plt.plot(t_vals, xdot_vals, label="Velocity (xdot)", linestyle="--")
plt.legend()
plt.ylabel("State")
plt.title("Mass-Spring-Damper System with Sampled Control")

# Plot Control Force
plt.subplot(2, 1, 2)
plt.step(control_times, u_vals, label="Control Force (u)", color="r", where="post")
plt.legend()
plt.xlabel("Time (s)")
plt.ylabel("Control Input")

plt.show()
