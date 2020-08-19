import threading

def sum(low, high):
    total = 0
    for i in range(low, high):
        total += i
    print("Subthread", total)

t = threading.Thread(target=sum, args=(1, 100000000))
t.start()
t.join()
if t.is_alive():
    print("is alive")
else:
    print("is dead")

print("Main Thread")