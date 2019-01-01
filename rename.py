import os
import sys
import glob

path = sys.argv[1]
files = glob.glob(path+"/*")


def countDigit(num, digit=1):
    if num < 10:
        return digit
    else:
        digit += 1
        return countDigit(num//10, digit=digit)


def main():
    names = []
    for i, f in enumerate(files, 1):
        _, extenion = os.path.splitext(f)
        old_name = os.path.basename(f)
        digit = "0"+str(countDigit(len(files)))+"d"
        new_name = format(i, digit)+"_img"+extenion
        names.append((f, os.path.join(path, new_name)))
        print(old_name+" => "+new_name)

    if input("agree ?: y or n") == "y":
        for before, after in names:
            os.rename(before, after)
        print("completed")


if __name__ == "__main__":
    main()
