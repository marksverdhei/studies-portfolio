import random

with open("generated_temps.csv", "w+", encoding="UTF8") as f:
    nums = ((random.randint(0, 23), random.randint(0, 59), random.randint(0, 9)) for i in range(20))
    seq = sorted(nums, key=lambda x: 60*x[0] + x[1])
    string = "\n".join(
        "{0:0=2d}:{1:0=2d}  {2}0.{3}".format(h, m, random.choice((" ", "-")), t) for h, m, t in seq
    )
    print(string)
    f.write(string)
