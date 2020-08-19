

def main():
    fd = open("./foo", "a", encoding="utf-8")

    fd.write("abc")
    return fd

fd = main()
fd.write("zzz")