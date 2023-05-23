import sys

file1_path = sys.argv[1]
file2_path = sys.argv[2]

try:
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        content1 = file1.read()
        content2 = file2.read()

        if len(content1) != len(content2):
            print("nok no tienen el mismo len")
        else:
            i = 0
            for char1, char2 in zip(content1, content2):
                if char1 != char2:
                    print("nok")
                    print(char1, char2)
                    print(i)
                    break
                i+=1
            else:
                print("ok")

except FileNotFoundError:
    print("Uno o más archivos no se encuentran")
