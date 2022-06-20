text = ''
with open("usloviya.txt", 'r') as f:
    text = f.read()

links_1 = text.split()
print(links_1)
links = []
for i in range(len(links_1)):
    if len(links_1[i]) > 5:
        links.append(links_1[i])

print((links))
