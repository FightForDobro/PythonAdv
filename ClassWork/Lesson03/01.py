import time
from math import factorial


def decorator(times=1):
    def actual_decorator(func):

        def wrapper(*args, **kwargs):
            time_list = []

            for i in range(times):

                full_time = time.time()
                result = func(*args, **kwargs)
                time_list.append(time.time() - full_time)

            return result, func.__name__, time.process_time(), time_list

        return wrapper

    return actual_decorator


@decorator(1)
def calculate_numbers_count_in_factorial(x):
    return len(str(factorial(x)))


result = calculate_numbers_count_in_factorial(52000)

print(f'Your result is: {result[0]}\nFunction name is: {result[1]}\nFull time is: {result[2]} seconds')

for i, j in enumerate(result[3]):
    print(f'{i + 1}: {j} seconds')
