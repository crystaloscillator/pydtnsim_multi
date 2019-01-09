uniq_count = 2
log = "init"
while(log):
    log = input().split()
    time = log[0]
    if len(log) == 5:
        uniq_count += 1
        print(time, uniq_count)
