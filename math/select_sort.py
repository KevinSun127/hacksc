def insert_sort(numbers):
    check = 0
    for i in range(1, len(numbers)+1):
        n = i%len(numbers)
        while n > 0:
            if numbers[n - 1] > numbers[n]:
                temp = numbers[n]
                numbers[n] = numbers[n-1]
                numbers[n-1] = temp
            else:
                break
            n-=1
            check += 1
            print(check, numbers)
    return numbers


def selection_sort(numbers):
    check = 0
    prev_check = 0
    for i in range(len(numbers)):
        min = numbers[i]
        location = i
        for j in range(i + 1, len(numbers)):
            if numbers[j] < min:
                min = numbers[j]
                location = j
            check += 1
        print("Compares with " + str(check - prev_check) + " other values, then exchanges " +
              str(numbers[i]) + " with " + str(min))
        if i != location:
            numbers = numbers[:i] + [min] + numbers[i+1:location] + \
                  [numbers[i]] + numbers[location + 1:]
        print(check, numbers)
        prev_check = check
    return numbers, check



selection_sort([13, 9, 6, 3, 15, 2, 21, 4, 16, 8, 11])