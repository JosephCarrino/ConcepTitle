# Goal: Reduce the *_simils.json files to get smaller files to process into visualizer.
# This script is based on "Timeslot" day and its number

import json

timeslot_day = '2024-03-23'
timeslot_number = -1 #Se -1 allora il ts_number viene ignorato e viene confrontato solo il timeslot_day

edition_simils_in = 'editions_simils.json'
flow_simils_in = 'flows_simils_2.json'
edition_simils_out = 'editions_simils_out.json'
flow_simils_out = 'flows_simils_out.json'



def main():
    f = open("./" + edition_simils_in, "r+")
    ed_news = json.load(f)
    f.close()
    f = open("./" + flow_simils_in, "r+")
    flow_news = json.load(f)
    f.close()
    ed_news = filter(ed_news, timeslot_day, timeslot_number)
    flow_news = filter(flow_news, timeslot_day, timeslot_number)
    with open(edition_simils_out, "w") as f:
        json.dump(ed_news, f, ensure_ascii=False, indent=4)
        f.write("\n")
        f.close()
    with open(flow_simils_out, "w") as f:
        json.dump(flow_news, f, ensure_ascii=False, indent=4)
        f.write("\n")
        f.close()


def filter(compared: list, ts_day: str, ts_number: int) -> list:
    filtered = []
    for c in compared:
        news = c['news']
        all_news_timeslot = True
        for new in news:
            if "timeslot_day" not in new.keys() or "timeslot_number" not in new.keys():
                all_news_timeslot = False
            elif new["timeslot_day"] != ts_day or (new["timeslot_number"] != ts_number and ts_number != -1):
                all_news_timeslot = False

        if all_news_timeslot:
            filtered.append(c)
    return filtered


if __name__ == "__main__":
    main()
