arr = [1, 2, 1, 4, 5]

def countingSort(arr):
    # Write your code here
   
    zeros = [0]*len(arr)
    for i in arr:
        zeros[i-1] += 1 
    
    return zeros 

print(countingSort(arr))