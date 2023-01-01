from div import sep

def main(p_): # div.sep()で変形しておく
    p = sep(p_)
    sha = 6
    for i in range(len(p)):
        for ia in range(2, 5):
            sha -= p[i].count(ia)
    return sha

if __name__ == "__main__":
    print(main(["1m", "1m", "2m", "2m", "3m", "3m", "4m", "4m", "5m", "5m", "6m", "6m", "7m", "7m"]))