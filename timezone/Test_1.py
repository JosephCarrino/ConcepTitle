# Given a newspaper what is the number of snapshots are into the given time window? (Time of newspaper)
# Just for start, not interesting

from utils import get_newspaper_time_articles

DAY = "2024-04-20"
START_TIME = "00:00:00"
END_TIME = "23:59:59"

BASE_DIR = "../Newscraping/collectedNews/flow"
NEWSPAPER_A = "EN/RioTimes"

def main():
    full_path = f"{BASE_DIR}/{NEWSPAPER_A}"
    articles = get_newspaper_time_articles(full_path, DAY, START_TIME, END_TIME)
    print(f"There are {len(articles)} unique articles")


if __name__ == '__main__':
    main()
