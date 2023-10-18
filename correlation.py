import numpy as np


def pearson_correlation(x, y):
    """
    # Calculate the Pearson correlation coefficient (r).
    """
    mu_x = np.mean(x)
    mu_y = np.mean(y)

    cov_xy = np.sum((x - mu_x) * (y - mu_y))
    sd_x = np.sqrt(np.sum((x - mu_x) ** 2))
    sd_y = np.sqrt(np.sum((y - mu_y) ** 2))

    r = cov_xy / (sd_x * sd_y)
    
    return r


def rank(arr):
    """
    Assigns ranks to the elements of an array in ascending order.
    """
    sorted_ids = np.argsort(arr)

    ranks = np.zeros(len(arr))
    ranks[sorted_ids] = np.arange(1, len(arr) + 1)

    return ranks


def spearman_correlation(x, y):
    """
    Calculate the Spearman correlation coefficient (rho).
    """
    # calculate the differences between ranks
    d = rank(x) - rank(y)
    n = len(x)

    rho = 1 - 6 * np.sum(d**2) / (n * (n**2 - 1))

    return rho


def create_buckets(arr, bins=10, mode='uniform'):
    """
    Assigns values in an array to buckets based on specified binning criteria.
    """
    if mode == 'uniform':
        bin_edges = np.linspace(arr.min(), arr.max(), bins + 1)
    elif mode == 'quntile':
        quantiles = np.linspace(0, 100, bins + 1)
        bin_edges = np.percentile(a=arr, q=quantiles)
    else:
        raise ValueError("Invalid mode")
    
    bin_indices = np.digitize(x=arr, bins=bin_edges)
    bin_indices_str = [str(i) for i in bin_indices]

    return bin_indices_str


def contingency_table(x, y):
    """
    Create a contingency table from paired variables (x, y).

    The input variables can be a mix of categorical and numerical data. 
    If the input variable is numerical, is is automatically divided into buckets.
    """
    assert len(x) == len(y), "Input variables must be the same length!"

    if all(isinstance(xi, (int, float, np.int64)) for xi in x):
        x = create_buckets(x)

    if all(isinstance(yi, (int, float, np.int64)) for yi in y):
        y = create_buckets(y)

    categories_x = list(np.unique(x))
    categories_y = list(np.unique(y))

    table = np.zeros((len(categories_x), len(categories_y)), dtype='int64')
    
    for xi, yi in zip(x, y):
        x_index = categories_x.index(xi)
        y_index = categories_y.index(yi)
        table[x_index, y_index] += 1
    
    return table


def chi_squared_statistic(table):
    """
    Calculate the chi-squared statistic for a given contingency table.
    """
    row_sums = np.sum(table, axis=1)
    col_sums = np.sum(table, axis=0)
    total_sum = np.sum(table)
    
    chi_squared = 0
    for i in range(table.shape[0]):
        for j in range(table.shape[1]):
            expected = (row_sums[i] * col_sums[j]) / total_sum
            chi_squared += (table[i, j] - expected) ** 2 / expected
    
    return chi_squared


def phi_k_correlation(x, y):
    """
    Calculate the Phi-K correlation coefficient.
    """
    table = contingency_table(x, y)
    chi_squared = chi_squared_statistic(table)
    
    n = len(x)
    k = table.shape[0]
    r = table.shape[1]
    
    phi_k = np.sqrt(chi_squared / (n * min(k - 1, r - 1)))

    return phi_k