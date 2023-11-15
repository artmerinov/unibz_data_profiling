from scipy.stats import mvn, multivariate_normal
import numpy as np

def calc_integral_between(lower, upper, mu, S):
    """
    Calculate the Multivariate Normal Cumulative Distribution Function (CDF) 
    for the region defined between 'lower' and 'upper' limits 
    for a multivariate normal distribution with mean 'mu' and covariance matrix 'S'.

    """
    integral = mvn.mvnun(lower, upper, mu, S)[0]
    return integral


def calc_integral_between_monte_carlo(lower, upper, mu, cov, n_samples=10000):
    """
    Estimate the probability of a Multivariate Normal random variable 
    falling within a region defined between 'lower' and 'upper' limits 
    using Monte Carlo simulation.
    """
    dim = len(mu)
    samples = multivariate_normal(mu, cov).rvs(size=n_samples)
    inside_count = 0

    for sample in samples:
        if all(lower[i] <= sample[i] <= upper[i] for i in range(dim)):
            inside_count += 1

    probability = inside_count / n_samples
    return probability