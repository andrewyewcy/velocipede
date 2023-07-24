def print_list(input_list):
    """
    =======
    PURPOSE
    =======
    This functions takes a list and iterates over it to print out the contents of the list up to a max of 20 items.
    The limit of 20 is set to avoid notebook display overflow.

    ======
    INPUTS
    ======
    list: a Python list object.

    =======
    OUTPUTS
    =======
    A print out of list contents with a number index for display.

    =======
    EXAMPLE
    =======
    from common_functions.notebook_functions.print import print_list

    sample_list = ["a","b","c"]
    print_list(sample_list)
    
    >>> Item 1 of 3: a
    >>> Item 2 of 3: b
    >>> Item 3 of 3: c
    """

    # Assertion statements to prevent function failure
    assert isinstance(input_list,list), "Passed item is not a list"
    assert len(input_list) != 0, "Passed list is empty."

    for index, item in enumerate(input_list):
        if index <= 19:
            print(f"Item {index + 1:02} / {len(input_list)}: {item}")