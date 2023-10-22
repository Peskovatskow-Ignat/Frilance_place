s = ['1', '4', '5', '7', '9']
for i in range(1, len(s), 2):

    s[i - 1], s[i] = s[i], s[i - 1]

print(*s)