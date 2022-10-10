"""
CustomList game project. Main file
Copyright 2022 by Artem Ustsov
"""

from list.custom_list import CustomList

if __name__ == "__main__":
    cust_list = CustomList([-5, -4, -3, -2, -1])
    main_list = [5, 6, 7]
    result_list_1 = cust_list - main_list
    result_list_2 = main_list - cust_list
    result_list_3 = cust_list + main_list
    result_list_4 = main_list + cust_list
    result_list_5 = CustomList()
    result_list_5 += cust_list

    print(f"{cust_list}")
    print(f"{main_list}\n")
    print(
        f"{result_list_1}\n"
        f"{result_list_2}\n"
        f"{result_list_3}\n"
        f"{result_list_3}\n"
        f"{result_list_5}\n",
    )
