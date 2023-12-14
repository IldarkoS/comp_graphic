import numpy as np
import matplotlib.pyplot as plt

def parametric_equation(phi, a):
    p_squared = a**2 * np.cos(2 * phi)
    return np.sqrt(p_squared)

def plot_polar_curve(a):
    phi = np.linspace(0, 2 * np.pi, 1000)
    p = parametric_equation(phi, a)

    plt.polar(phi, p, label=r'$p^2 = a^2 \cos(2\phi)$')
    plt.title('$p^2 = a^2 \cos(2\phi)$')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    a = 5.0
    plot_polar_curve(a)
