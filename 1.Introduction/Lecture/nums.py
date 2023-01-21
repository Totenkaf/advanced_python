def evens(nums):
    return [x for x in nums if x % 2 == 0]


def check_evens_len(nums):
    if len(nums) > 2:
        return evens(nums)
    else:
        return []
