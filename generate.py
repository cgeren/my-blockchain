from pathlib import Path
import random
import string


def main():
    file_length = input("Enter file length: ")

    with open("in.txt", 'w') as f:
        for i in range(int(file_length)):
            f.write(get_random_address() + " " + str(get_random_balance()) + '\0' + '\n')
        #f.write("\0")


def get_random_address():
    letters = string.hexdigits
    result_str = ''.join(random.choice(letters) for i in range(40))
    return result_str


def get_random_balance():
    return random.randint(1000, 10000)


if __name__ == "__main__":
    main()
