
def product_matrix(A,B):
    
    result = [[sum(a * b for a, b in zip(A_row, B_col))
                            for B_col in zip(*B)]
                                    for A_row in A]

    return result

def mydot(v1, v2):
     return sum([x*y for x,y in zip(v1, v2)])

def product_matrix_vector(G, v):
    return [mydot(r,v) for r in G]
