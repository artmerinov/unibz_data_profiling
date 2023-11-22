from pli import generate_pli, pli_intersection_optimized


def prepare_Fk(df):
    """
    Trasform df into the format
    Fk = [(f1, pli1), (f2, pli2), ..., (fk, plik)]
    """
    Fk = []

    for col in df.columns:
        pli = generate_pli(df[col])
        Fk.append((col, pli))

    return Fk


def generate_candidates(Fk):
    """
    Generates candidates for UCC (unique column combination) 
    discovery in Apriori algorithm.

    Input: Fk = [(f1, pli1), (f2, pli2), ..., (fk, plik)]
    Output: Candidates for the next level in the same format as Fk.
    """
    E = []

    schema = [f[0] for f in Fk]
    # print('schema:', schema)
    # print(set(schema))

    # traverse all pairs of non-unique column combinations 
    # (if column is unique, than all generated supersets or childs will be also unique!)
    # that share the same maximal prefix (they are in lexicographic order) 
    # and differ only in one last attribute

    for f1, pli1 in Fk:
        for f2, pli2 in Fk:

            # use lexicographic order
            if f1 < f2:

                # check if f1 and f2 share the same maximal prefix 
                # and differ only in the last attribute
                if f1[:-1] == f2[:-1]:

                    # make new CC with k+1 attributes 
                    # using a union of f1 and f2
                    f = f1 + f2[-1]

                    # print(f1, 'u', f2, '-->', f)

                    # and make an intersection of PLIs
                    pli = pli_intersection_optimized(pli1, pli2)
                    
                    # for i in f:
                    #     subset = ''.join(sorted(set(f) - set(i)))
                    #     if subset in schema:
                    #         print(f'subset {subset} in schema')
                    #     else:
                    #         print(subset)
                

                    # if all subsets with k attributes are non-unique
                    if all(''.join(sorted(set(f) - set(i))) in schema for i in f):
                        E.append((''.join(f), pli))             
                               
    return E