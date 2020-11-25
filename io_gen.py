import random

n = 50
S_max = 68.75
stresses = 0.25
happiness = 1

print(n)
print(S_max)

nums = list(range(0, n))
random.shuffle(nums)

pairings = [
            set(nums[:11]),
            set(nums[11:22]),
            set(nums[22:33]),
            set(nums[33:44]),
            set(nums[44:])
            ]


for i in range(n):
    for j in range(n):
        if i < j:
            both_in = False

            for p in pairings:
                if i in p and j in p:
                    both_in = True
                    break

            if both_in:
                print(i, j, happiness + 1, stresses)
            else:
                print(i, j, happiness, stresses)


for i in range(len(pairings)):
    for e in pairings[i]:
        print(e, i)

print(pairings)
