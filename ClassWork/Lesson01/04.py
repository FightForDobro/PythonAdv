def bank(sum_of_deposit, age_of_deposit, percentage):

    for i in range(1, age_of_deposit + 1):
        sum_of_deposit += (sum_of_deposit/100) * percentage

    return sum_of_deposit


print(bank(100, 10, 10))