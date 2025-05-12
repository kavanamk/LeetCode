#Kavana Manvi Krishnamurthy
#Depaul ID 2158984
import sys

def mergesort(A, start, end):
    if start < end:
        m = (start + end) // 2

        mergesort(A, start, m)
        mergesort(A, m + 1, end)
        
        merge(A, start, m, end)

def merge(A, start, m, end):
    i = start
    j = m + 1
    B = [0] * (end - start + 1)  

    for k in range(start, end + 1):
        if j > end:
            B[k - start] = A[i]  
            i += 1
        elif i > m:
            B[k - start] = A[j]  
            j += 1
        elif A[i] < A[j]:
            B[k - start] = A[i]  
            i += 1
        else:
            B[k - start] = A[j] 
            j += 1
        
    
    
    for k in range(start, end + 1):
        A[k] = B[k - start]

def main():
    print("Kavana Manvi Krishnamurthy")
    if len(sys.argv) != 2:
        print("Usage: python mergesort.py <name of input file>")
        sys.exit(1)

    input_file = sys.argv[1]
    try:
        with open(input_file, 'r') as file:
            integers = [int(x) for x in file.read().split()]
    except FileNotFoundError:
        print("File not found:", input_file)
        sys.exit(1)
    except ValueError:
        print("File contains non-integer values.")
        sys.exit(1)

    
    print(' '.join(map(str, integers)))

    mergesort(integers,0,len(integers)-1)

    print(' '.join(map(str, integers)))

if __name__ == "__main__":
    main()
