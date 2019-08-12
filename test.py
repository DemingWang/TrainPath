# num = 3
# years = [1,1,1]
num=int(input())
years=list(map(int,input().split()))
salary = []

for year in years:
    salary.append([year,100])

print(salary)
salary_dict = dict(zip(range(num),salary))
print(salary_dict)

currentID = 0

while(currentID < num):
    if currentID == 0:
        if salary_dict[currentID][0] > salary_dict[currentID+1][0]:
            salary_dict[currentID][1] = salary_dict[currentID+1][1] + 100
    elif currentID == num -1:
        if salary_dict[currentID][0] > salary_dict[currentID-1][0]:
            salary_dict[currentID][1] = salary_dict[currentID-1][1] + 100
    else:
        if salary_dict[currentID][0] > salary_dict[currentID-1][0]:
            salary_dict[currentID][1] = salary_dict[currentID-1][1] + 100
        if salary_dict[currentID][0] > salary_dict[currentID+1][0]:
            salary_dict[currentID][1] = salary_dict[currentID+1][1] + 100
    
    currentID = currentID + 1

sum = 0
for p in salary_dict:
    sum = sum + salary_dict[p][1]

print(salary_dict)
print(sum)