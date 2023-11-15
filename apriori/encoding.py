
from collections import Counter
import heapq


def create_huffman_prefix_mapping(transactions):
    """
    Creates a mapping of items to its prefix codes.

    Huffman coding builds a prefix tree where the most frequently 
    used items have the shortest encoding. The prefix tree ensures 
    that the code for any item is never a prefix of the code for 
    any other item.

    Using this prefix mapping, we will be able encode transaction 
    by concatinatig codes of single items within the transaction, 
    as well as uniquely decode it back.
    """
    # find overall frequency of each item
    item_freq_cntr = Counter(item for transaction in transactions for item in transaction)
    
    # craete min-heap structure 
    # (the smallest element is always at the root of the heap) 
    heap = [[freq, [item, '']] for item, freq in item_freq_cntr.items()]
    heapq.heapify(heap)

    while len(heap) > 1:

        # pop the two lowest frequency nodes from the list, 
        # the sum of their frequencies will be the frequency 
        # of their parent node

        l = heapq.heappop(heap)
        r = heapq.heappop(heap)

        for pair in l[1:]:
            pair[1] = '0' + pair[1] 

        for pair in r[1:]: 
            pair[1] = '1' + pair[1]
        
        heapq.heappush(heap, [l[0] + r[0]] + l[1:] + r[1:])
    
    huffman_tree = heap[0][1:]
    item2code_mapping = {item: code for item, code in huffman_tree}

    return item2code_mapping


def encode_transaction(transaction, item2code_mapping):
    """
    Encodes transaction into code name.
    """
    transaction_code = ''.join(item2code_mapping[item] for item in transaction)
    return transaction_code


def decode_transaction(transaction_code, item2code_mapping):
    """
    Decode transaction into item names.
    """
    decoded_items = []

    while transaction_code:
        max_match_length = 0
        matched_item = None

        for item, code in item2code_mapping.items():
            if transaction_code.startswith(code) and len(code) > max_match_length:
                max_match_length = len(code)
                matched_item = item

        if matched_item is not None:
            decoded_items.append(matched_item)
            transaction_code = transaction_code[max_match_length:]
        else:
            # If no match is found, break the loop
            break

    return decoded_items