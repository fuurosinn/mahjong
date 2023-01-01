from div import sep

def main(p_):
    a = [(0, 8), (0, 8), (0, 8), (0, 1, 2, 3, 4, 5, 6)]
    p = sep(p_)
    sha = 13
    flag = True
    for i in range(4):
        for ia in a[i]:
            x = p[i][ia]
            if x > 0:
                sha -= 1
                if flag and x > 1:
                    flag = False
                    sha -= 1
    return sha

if __name__ == "__main__":
    print(main(["1m", "9m", "1p", "9p", "1s", "9s", "1z", "2z", "3z", "4z", "5z", "6z", "7z", "7z"]))