import numpy as np


def pearson_correlation(x, y):

    # Calculate the mean of x and y
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)

    # Calculate the differences from the mean for both variables
    diff_x = [xi - mean_x for xi in x]
    diff_y = [yi - mean_y for yi in y]

    # Calculate the sum of squared differences
    sum_squared_diff_x = sum([(xi - mean_x) ** 2 for xi in x])
    sum_squared_diff_y = sum([(yi - mean_y) ** 2 for yi in y])

    # Calculate the sum of the product of differences
    sum_product_diff = sum(diff_x[i] * diff_y[i] for i in range(len(x)))

    # Calculate the Pearson correlation coefficient (r)
    r = sum_product_diff / (pow(sum_squared_diff_x, 0.5) * pow(sum_squared_diff_y, 0.5))

    return r


def spearman_correlation(x, y):
    
    # Create ranked versions of x and y
    rank_x = [sorted(x).index(xi) + 1 for xi in x]
    rank_y = [sorted(y).index(yi) + 1 for yi in y]

    n = len(x)

    # Calculate the differences between ranks
    rank_diff = [rank_x[i] - rank_y[i] for i in range(n)]

    # Calculate the Spearman rank correlation coefficient (rho)
    numerator = 6 * sum([d ** 2 for d in rank_diff])
    denominator = n * (n ** 2 - 1)
    rho = 1 - numerator / denominator

    return rho


def create_buckets(data, bins=10, mode='uniform'):
    """
    Assigns a bucket for each value.
    """
    if mode == 'uniform':
        bin_edges = np.linspace(data.min(), data.max(), bins + 1)
    elif mode == 'quntile':
        quantiles = np.linspace(0, 100, bins + 1)
        bin_edges = np.percentile(a=data, q=quantiles)
    else:
        raise ValueError("Invalid mode")
    
    bin_indices = np.digitize(x=data, bins=bin_edges)
    bin_indices_str = [str(i) for i in bin_indices]
    
    return bin_indices_str


def contingency_table(x, y):
    """
    Creates contingency table out of (x,y) pairs.
    """
    assert len(x) == len(y), "Input must be the same length"

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
    table = contingency_table(x, y)
    chi_squared = chi_squared_statistic(table)
    
    n = len(x)
    k = table.shape[0]
    r = table.shape[1]
    
    phi_k = np.sqrt(chi_squared / (n * min(k - 1, r - 1)))
    return phi_k