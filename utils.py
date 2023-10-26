import numpy as np
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