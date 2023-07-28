from math import floor


def print_progress(step_name: str,
                   current_offset: int,
                   last_printed_percent: int,
                   total: int):
    """Print progress to the terminal

    Args:
        step_name (str): Name of the step to print
        current_offset (int): Current offset in the step
        last_printed_percent (int): Last printed percent
        total (int): Total amount of progress to make

    Returns:
        int: The current percent
    """
    current_percent = floor(current_offset / total * 100)
    if (current_percent - last_printed_percent) >= 10:
        print(f"{step_name}: {current_percent:d}%")

    return current_percent
