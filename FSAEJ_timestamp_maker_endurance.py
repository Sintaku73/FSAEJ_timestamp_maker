# %%
import math
import os
import re

import pandas as pd

# %%
url = "http://jsae-res.com/result/listup/?race_id=4&day=2"
df = pd.read_html(url, match="Car#")[0]
print(df.head())

# %%
print("N/A")
index_na = df["hh:mm:ss"] == "--:--:--"
print(df[index_na])
df = df[df["hh:mm:ss"] != "--:--:--"]

# df.loc[index_na, "hh:mm:ss"] = np.nan
# df[index_na]

# %%
df["TIME"] = pd.to_datetime(df["TIME"], format='%M"%S.%f') - pd.to_datetime(
    "00:00:00", format="%X"
)
df["hh:mm:ss"] = pd.to_datetime(df["hh:mm:ss"], format="%X")

# %%
# format> hh:mm:ss
live_delay = "00:00:09"
datum_timestamp = "00:00:00"
datum_time = "07:50:30"

# parameters for follow-up run
held_followup = False
starttime_followup = "16:00:00"

live_delay = pd.to_datetime(live_delay, format="%X") - pd.to_datetime(
    "00:00:00", format="%X"
)
datum_timestamp = pd.to_datetime(datum_timestamp, format="%X") - pd.to_datetime(
    "00:00:00", format="%X"
)
datum_time = pd.to_datetime(datum_time, format="%X")

starttime_followup = pd.to_datetime(starttime_followup, format="%X")

# %%
df["Follow-up"] = False
if held_followup:
    df["Follow-up"] = (df["hh:mm:ss"] - df["TIME"]) > starttime_followup
df["DELTA"] = df["hh:mm:ss"] - datum_time + datum_timestamp + live_delay - df["TIME"]
print(df.head())

# %%
df["Name"] = df["Car#"].map(
    lambda x: (
        "C"
        + str(int(re.search(r"\d+\s{1}", x).group())).zfill(2)
        + x[len(re.search(r"\d+\s{1}", x).group()) - 1 :]
        if x[0] != "E"
        else x
    )
)
print(df.head())

# %%
df.sort_values(["Follow-up", "Name", "hh:mm:ss"], inplace=True)
print(df.head())

# %%
l_team = df["Name"].unique()


# %%
def sec2timestamp(sec):
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    return f"{int(h):02d}:{int(m):02d}:{math.floor(s):02d}"


# %%
followuup_section = False
l_text = []
for team in l_team:
    df_temp = df[df["Name"] == team]
    lap_2ndDr = 11
    if df_temp["Follow-up"].all():
        if not followuup_section:
            l_text.append("")
            followuup_section = True
        lap_2ndDr = 6
    stamp_temp = []
    for _, s in df_temp.iterrows():
        sec_temp = s["DELTA"].total_seconds()
        stamp_temp.append(sec2timestamp(sec_temp))
    if len(stamp_temp) >= lap_2ndDr:
        stamp_selected = " ".join([stamp_temp[0], stamp_temp[lap_2ndDr]])
    else:
        stamp_selected = stamp_temp[0]
    l_text.append(team + " " + stamp_selected)

# %%
out_dir = "./out"
savename_head = "timestamp"
savename_tail = "race_id_" + url[-7] + "_day_" + url[-1]
path_save = f"{out_dir}/{savename_head}_{savename_tail}.txt"

os.makedirs(out_dir, exist_ok=True)

with open(path_save, mode="w") as f:
    f.write("\n".join(l_text))

# %%
# df[["Name", "Follow-up", "TIME"]].groupby(["Name", "Follow-up"]).count().sort_values(
#     "TIME"
# ).to_csv("./References/total_laps_endurance_day_1.csv")

# %%
