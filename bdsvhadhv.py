
list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
odd = []
prime = []

list2 = []

answer = int(input("Enter a number: "))

for i in range(answer):
    list2.append(i)
print(list2)

for i in list:
    if i % 2 != 0:
        odd.append(i)
        
for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            break
    else:
        prime.append(n)
     
print(odd)
print(prime)

ClassMarks = [5, 13, 30, 50, 14, 17, 33, 23, 6, 90, 55, 12, 
              13, 33, 23, 6, 98, 13, 14, 76, 12, 45, 12]

print(min(ClassMarks))
print(max(ClassMarks))

mean = sum(ClassMarks) / len(ClassMarks)
print(f"{mean:.2f}")

something = set(ClassMarks)

print(something)
 
def fib(n):
    a, b = 0, 1
    while a <= n:
        print(a, end = " ")
        a, b = b, a + b
    print()

fib(2000)  
    