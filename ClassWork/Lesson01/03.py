def fizz_buzz(num):
    """
    Function return Fizz if num divided by 3 or buzz if num divided by 5 else whenever num multiple by 15
    :param num: num
    :type num: int
    :return: changed num
    """

    return 'Fizz'*(num % 3 == 0) + 'Buzz'*(num % 5 == 0) or num


for i in range(1, 101): print(fizz_buzz(i))
