def get_basket(transactions):
    """
    Returns list of all unique items based on transactions 
    (in lexicographical order).
    """
    # basket = sorted(set(item for transaction in transactions for item in transaction))
    basket = set(item for transaction in transactions for item in transaction)
    return basket


def get_item_codes_dict(basket):
    """
    Creates mapping of items and its code names
    (keys are in lexicographical order).
    """
    item_codes_dict = {item: format(i, 'b') for i, item in enumerate(basket)}
    return item_codes_dict


def encode_transaction(transaction, item_codes_dict):
    """
    Encodes transaction into code name in lexicographical order.
    """
    # by defalut keys of our dictionary are sorted lexicographically
    transaction_code = ''.join(item_codes_dict[item] for item in transaction)
    return transaction_code


def decode_transaction(transaction_code, item_codes):
    decoded_items = []

    while transaction_code:
        max_match_length = 0
        matched_item = None

        for item, code in item_codes.items():
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