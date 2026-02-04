list=[n for n in range(1,5)]
list_with_condition=[n*2 for n in range(1,5) if n%2==0]
list_with_comprehension=[f"{n} is even" if n%2==0 else f"{n} is odd" for n in range(1,5)]

# Equivalent code
# new_list=[]
# for n in range(1,5):
#     if n%2==0:
#         new_list.append(f"{n} is even")
#     else:
#         new_list.append(f"{n} is odd")

print("List:",list)
print("List with condition:",list_with_condition)
print("List with comprehension:",list_with_comprehension)