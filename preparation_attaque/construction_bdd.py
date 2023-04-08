import requests
import random
import sys
sys.path.append('libs')
url = "https://randomuser.me/api/"

names = []
salaries = []
pp = []
for i in range(5000):
    response = requests.get(url)
    data = response.json()["results"][0]["name"]
    name = data["first"]
    while name in names:
        response = requests.get(url)
        data = response.json()["results"][0]["name"]
        name = data["first"] + " " + data["last"]
    ranges = [(0, 1000), (1000, 2500), (2500, 4000), (4000, 6000), (6000, 10000), (10000, 20000)]
    weights = [10, 20, 25, 10, 20, 15]

    selected_range = random.choices(ranges, weights=weights, k=1)[0]
    salary = random.randint(selected_range[0], selected_range[1])
    salaries.append(salary)
    names.append(name)

    pp.append((name,salary))
    print((i/5000)*100," %")

with open("person.txt",'w') as f:
    f.write(str(pp))