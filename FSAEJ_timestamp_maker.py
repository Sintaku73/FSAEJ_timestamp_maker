# %%
import math
import os
import re

import pandas as pd

# %%
url = "http://jsae-res.com/result/listup/?race_id=3"
df = pd.read_html(url, match="Car#")[0]
df.head()

# %%
print("N/A list")
display(df[df["hh:mm:ss"] == "--:--:--"])
df = df[df["hh:mm:ss"] != "--:--:--"]

# %%
skidpad_factor = 2.5
if df["TIME"].dtype == "float64":
    df["TIME"] = pd.to_timedelta(df["TIME"], unit="s")
elif re.search(r"R:.+L:.+", df["TIME"][0]) is not None:
    df["TIME"] = pd.to_timedelta(
        df["TIME"].map(lambda x: float(re.search(r"^\d+.\d{3}", x).group()))
        * skidpad_factor,
        unit="s",
    )
else:
    df["TIME"] = pd.to_datetime(df["TIME"], format='%M"%S.%f') - pd.to_datetime(
        "00:00:00", format="%X"
    )

df["hh:mm:ss"] = pd.to_datetime(df["hh:mm:ss"], format="%X")

# %%
# format> hh:mm:ss
live_delay = "00:00:08"
datum_timestamp = "00:00:00"
datum_time = "07:50:41"

live_delay = pd.to_datetime(live_delay, format="%X") - pd.to_datetime(
    "00:00:00", format="%X"
)
datum_timestamp = pd.to_datetime(datum_timestamp, format="%X") - pd.to_datetime(
    "00:00:00", format="%X"
)
datum_time = pd.to_datetime(datum_time, format="%X")

# %%
df["DELTA"] = df["hh:mm:ss"] - datum_time + datum_timestamp + live_delay - df["TIME"]
df.head()

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
df.head()

# %%
df.sort_values(["Name", "hh:mm:ss"], inplace=True)
df.head()

# %%
l_team = df["Name"].unique()


# %%
def sec2timestamp(sec):
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    return f"{int(h):02d}:{int(m):02d}:{math.floor(s):02d}"


# %%
l_text = []
for team in l_team:
    df_temp = df[df["Name"] == team]
    stamp_temp = []
    for _, s in df_temp.iterrows():
        sec_temp = s["DELTA"].total_seconds()
        stamp_temp.append(sec2timestamp(sec_temp))
    l_text.append(team + " " + " ".join(stamp_temp))

# %%
out_dir = "./out"
savename_head = "timestamp"
savename_tail = "race_id_" + url[-1]
path_save = f"{out_dir}/{savename_head}_{savename_tail}.txt"

os.makedirs(out_dir, exist_ok=True)

with open(path_save, mode="w") as f:
    f.write("\n".join(l_text))
