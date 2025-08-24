# Created with reference from https://www.learndatasci.com/solutions/python-timer/

# Import required packages
from time import perf_counter
from contextlib import contextmanager

def timer_wrapper(function):
    """
    =======
    PURPOSE
    =======
    This function is used as a decorator on top of another defined function.

    ======
    INPUTS
    ======
    None. Use this as a decorator on top of another defined function.

    =======
    OUTPUTS
    =======
    Printout of time taken for defined function.

    =======
    EXAMPLE
    =======
    from common_functions.timer import timer_wrapper
    
    @timer_wrapper
    def sample_function(x):
        x = x + 1

    sample_function(1)

    >>> Run 1 of sample_function took {time_taken} seconds.
    >>> Total run time: {time_taken} seconds. Average run time: {time_taken} seconds. 
    """

    # Initiate total time and run variables
    total_time, runs = 0, 0

    # Define timer function to be executed for each run of function within timer wrapper
    def timer(*args, **kwargs):
        
        # Initiate timer
        start_time = perf_counter()

        # Run the function
        result = function(*args, **kwargs)

        # End timer
        end_time =  perf_counter()

        # Calculate time_taken for 1 run
        time_taken = end_time - start_time

        # Bring variables in timer_wrapper into timer function
        nonlocal total_time, runs

        # Add 1 to run since run has just completed, also add time_taken
        runs += 1
        total_time += time_taken

        print(f"Run {runs} of {function.__name__} took {time_taken:0.4f} seconds.")
        print(f"Total run time: {total_time:0.4f} seconds. Average run time: {(total_time /  runs):0.4f} seconds. \n")

        return result
    return timer

# The timer function is implemented as a context manager using the @context manager decorator
@contextmanager
def print_time():
    """
    =======
    PURPOSE
    =======
    This function is used as a WITH statement to measure the time of any function(s) within the WITH statement.
    Time measured in seconds with 4 decimal places.

    ======
    INPUTS
    ======
    Any function can be timed within the WITH statement, even if the function fails

    =======
    OUTPUTS
    =======
    Printout of time taken for function or operation.
    Returns the time taken for storage.

    =======
    EXAMPLE
    =======
    with print_time():
        {insert function here}

    >>> Time taken: {time_taken} seconds.
    """
    # Initiate the timer
    start_time = perf_counter()
    
    # a yield was added inside a try-finally code block to ensure that the context manager can still calculate end time even if framed code throws error
    try:
        yield
        
    finally:
        # End the timer
        end_time = perf_counter()
        
        # Calculate time taken, then print out time taken
        time_taken = end_time - start_time
        print(f"Time taken: {time_taken:0.4f} seconds.")