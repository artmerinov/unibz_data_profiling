from collections import defaultdict


def generate_pli(column):
    """
    PLI from single attributes.
    """
    pli = defaultdict(list)
    
    # create group of indexes for each common value
    for index, value in enumerate(column):
        pli[value].append(index)

    pli = {i+1: v for i, (k, v) in enumerate(pli.items())}
    
    # remove singletons
    pli = {k: v for k, v in pli.items() if len(v) > 1}

    return pli


def pli_intersection(pli1, pli2):
    intersection = {}

    for i, group1 in pli1.items():
        for j, group2 in pli2.items():
            common_indices = set(group1) & set(group2)
            
            # remove singletons
            if len(common_indices) > 1:  
                intersection[(i, j)] = sorted(list(common_indices))

    return intersection


def create_probing_table(pli):
    """
    Creates mapping bewtween index and group number.
    """
    probing_table = {}

    for gr_index, group in pli.items():
        for index in group:
            probing_table[index] = gr_index

    return probing_table


def pli_intersection_optimized(pli1, pli2):
    intersection = defaultdict(list)

    # create a probing table for pli1
    pt1 = create_probing_table(pli1)
    
    # check for common indices in pli2 using the probing table of pli1
    for gr2_index, gr2_values in pli2.items():
        for v in gr2_values:
            if v in pt1:
                gr1_index = pt1[v]
                intersection[(gr1_index, gr2_index)].append(v)

    # remove singletons
    intersection = {k: v for k, v in intersection.items() if len(v) > 1}
                
    return intersection