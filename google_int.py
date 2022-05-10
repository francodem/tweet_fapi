list1 = ['a', 'b', 'c', 'd']
list2 = ['h', 'i', 'j', 'e']
sum = 0 
for letter_1 in list1:
    for letter_2 in list2:
        if letter_1 == letter_2:
            sum += 1

if sum > 0:
    print("True!")
else:
    print("False")