import numpy as np
from scipy.stats import multivariate_normal


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


def create_buckets(arr, bins=10):
    """
    Assigns values in an array to buckets.

    Returns bucket number for each value and 
    mapping from bucket id to interval range.
    """
    max = np.max(arr)
    min = np.min(arr)

    # for each value in array assign a bucket
    bucket_size = (max - min) / bins
    bin_edges = np.arange(min, max, bucket_size)
    buckets = np.digitize(x=arr, bins=bin_edges, right=False)

    # create mapping bucket2interval (for visualisation)
    intervals = []
    for i in range(len(bin_edges) - 1):
        intervals.append(f"{bin_edges[i]:.3f} - {bin_edges[i + 1]:.3f}")
    intervals.append(f"{bin_edges[i + 1]:.3f} - {max:.3f}")
    bucket2interval = {i + 1: interval for i, interval in enumerate(intervals)}
    
    return buckets, bucket2interval


def calc_contingency_table(x, y, xbins=10, ybins=10, xlabel=None, ylabel=None):
    """
    Create a contingency table from paired variables (x, y).

    The input variables can be a mix of categorical and numerical data. 
    If the input variable is numerical, it will be automatically divided into buckets.
    """
    x_bucket2interval = None
    y_bucket2interval = None
    
    if all(isinstance(xi, (int, float, np.int64)) for xi in x):
        x, x_bucket2interval = create_buckets(x, bins=xbins)

    if all(isinstance(yi, (int, float, np.int64)) for yi in y):
        y, y_bucket2interval = create_buckets(y, bins=ybins)

    categories_x = list(np.unique(x))
    categories_y = list(np.unique(y))

    nx = len(categories_x)
    ny = len(categories_y)

    table = np.zeros((nx, ny), dtype='int64')
    for xi, yi in zip(x, y):
        x_index = categories_x.index(xi)
        y_index = categories_y.index(yi)
        table[x_index, y_index] += 1

    # save useful artifacts for visualisation
    meta = {}
    meta['xticks'] = [x_bucket2interval[i] for i in categories_x] if x_bucket2interval else categories_x
    meta['yticks'] = [y_bucket2interval[i] for i in categories_y] if y_bucket2interval else categories_y
    meta['xlabel'] = xlabel
    meta['ylabel'] = ylabel
    
    return table, meta


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
            observed = table[i, j]
            chi_squared += (observed - expected) ** 2 / expected
    
    return chi_squared


def phi_c_correlation(x, y):
    """
    Calculate the Cramer's correlation coefficient.
    """
    table, meta = calc_contingency_table(x, y)
    chi_squared = chi_squared_statistic(table)

    n = len(x)
    k = table.shape[0]
    r = table.shape[1]

    phi_k = np.sqrt(chi_squared / (n * min(k - 1, r - 1)))
    return phi_k


