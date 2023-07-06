from glob import glob
from pathlib import Path


def main():
    target = input("target keyword: ")
    candidates = glob("azure-sdk-for-python/sdk/*/azure-mgmt-*/azure/mgmt/**/*.py", recursive=True)
    for candidate in candidates:
        with open(str(candidate), "r") as reader:
            content = reader.readlines()
            for idx in range(len(content)):
                if target in content[idx]:
                    print(f"{Path(candidate).absolute()}:{idx+1}")
                    return

if __name__ == "__main__":
    main()
