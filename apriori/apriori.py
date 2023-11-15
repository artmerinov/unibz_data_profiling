from itertools import combinations


# def generate_candidates(schema, k):
#     result = []
#     for comb in combinations(schema, k):
#         # ensure that elements are in lexicographic order
#         if all(comb[i] < comb[i + 1] for i in range(len(comb) - 1)):
#             result.append(''.join(comb))
#     return result


def generate_candidates(schema, k, frequent_items_prev):
    """
    Generate all possible candidates of size k based on the initial schema 
    (lexicographical order) and frequent items from the previous layer.

    Note, that we don't generate all possible combinations. 
    
    1. We use information about lexicographical order: each new item 
    will be added iff it is greater than the previous one. For example, 
    for schema {'a', 'b', 'c'} we will geneerage only {'ab', 'ac', 'bc'}

    2. We use inforamtion about frequent items from prevous layer. Since 
    specification of infrequent itemset will be also infrequent, 
    we generate candidates from parents that are frequent.
    """
    candidates = []
    stack = []
    
    i = 0
    while True:
        if len(stack) == k:
            candidate = ''.join(stack)
            if candidate[:-1] in frequent_items_prev:
                candidates.append(candidate)
            i += 1
        if len(stack) == k or i == len(schema):
            if not stack:
                break
            last_item = stack.pop()
            i = schema.index(last_item) + 1
        else:
            stack.append(schema[i])
            i += 1

        # print(f'i={i}, stack={stack}, candidates={candidates}')

    # # print lists of child elements for each parent
    # for parent in schema:
    #     child_list = [child for child in candidates if child.startswith(parent)]
    #     print(f'parent {parent}: {", ".join(child_list)}')

    return candidates


def is_frequent(candidate, transactions, support_threshold):
    """
    Checks wheether candidate is frequent or not.
    """
    accurances = 0
    for t in transactions:
        if set(candidate).issubset(set(t)):
            accurances += 1
    return accurances >= support_threshold


def apriori(transactions, support_thr):
    
    items = [item for transaction in transactions for item in transaction]
    schema = sorted(list(set(items)))

    # the first layer is frequent items from schema
    frequent_items = {1: [c for c in schema if is_frequent(c, transactions, support_thr)]}
    
    k = 1
    while frequent_items[k]: # while previous layer is not empty
        k += 1
        candidates_k = generate_candidates(schema=schema, k=k, frequent_items_prev=frequent_items[k-1])
        frequent_items[k] = [c for c in candidates_k if is_frequent(c, transactions, support_thr)]

    return frequent_items