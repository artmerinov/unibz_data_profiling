import numpy as np
from scipy.stats import multivariate_normal
import matplotlib.pyplot as plt


def plot_contingency_table(table, meta):

    xticks = meta['xticks']
    yticks = meta['yticks']

    plt.figure(figsize=(8, 6))
    plt.imshow(table.T, interpolation='nearest', cmap='coolwarm')
    plt.xticks(ticks=np.arange(len(xticks)), labels=xticks, rotation='vertical', fontsize=8)
    plt.yticks(ticks=np.arange(len(yticks)), labels=yticks, fontsize=8)
    
    # Create grid lines between blocks
    for x in range(1, len(xticks)):
        plt.axvline(x - 0.5, color='white', linewidth=1)
    for y in range(1, len(yticks)):
        plt.axhline(y - 0.5, color='white', linewidth=1)

    # Annotate cells with values
    for i in range(len(xticks)):
        for j in range(len(yticks)):
            plt.text(i, j, str(table[i, j]), ha='center', va='center', color='black', fontsize=10, weight='bold')

    plt.title('Contingency Table', weight='bold', size=18, loc='left', pad=10)
    plt.xlabel(meta['xlabel'])
    plt.ylabel(meta['ylabel'])
    plt.show()


def plot_binorm_distr_3d(rho):

    x, y, pdf = generate_binorm_distr(rho=rho)

    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, pdf, cmap='coolwarm')
    ax.set_title(f'Bivariate Normal with rho={rho}')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('PDF')
    plt.show()


def plot_binorm_distr_2d(rho, grid=None):

    x, y, pdf = generate_binorm_distr(rho=rho)

    plt.figure(figsize=(5,5))
    plt.contourf(x, y, pdf, levels=10, cmap='coolwarm')
    plt.title(f'Bivariate Normal with rho={rho}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim((-3,3))
    plt.ylim((-3,3))
    if grid:
        for cell in grid:
            lower, upper = cell
            x_rect = [lower[0], upper[0], upper[0], lower[0], lower[0]]
            y_rect = [lower[1], lower[1], upper[1], upper[1], lower[1]]
            plt.plot(x_rect, y_rect, 'k-', lw=0.3)
    plt.show()


def generate_binorm_distr(rho):
    """
    Generate data for a bivariate normal distribution 
    with a specified correlation coefficient (rho).
    """
    # gererate a grid
    x, y = np.mgrid[-5:5:0.01, -5:5:0.01]
    pos = np.dstack((x, y))

    mu = np.array([0.0, 0.0])
    sigma = np.array([[1.0, rho], [rho, 1.0]])
    pdf = multivariate_normal(mean=mu, cov=sigma, seed=0).pdf(pos)

    return x, y, pdf