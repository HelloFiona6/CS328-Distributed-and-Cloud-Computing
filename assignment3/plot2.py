import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("r5.csv")

df["start_time"] = pd.to_datetime(df["start_time"])

# Remove '%' and convert to float
df["percentage_value"] = df["percentage"].str.replace("%", "").astype(float)


sections = df["section"].unique()[:3]

print("Plotting sections:", sections)


# plt.rc("font",family='MicroSoft YaHei',weight="bold")
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False
# plt.rcParams['font.family'] = 'WenQuanYi Zen Hei'

import matplotlib.font_manager as fm
font_path = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
font_prop = fm.FontProperties(fname=font_path)

plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['font.sans-serif'] = [font_prop.get_name()]
plt.rcParams['axes.unicode_minus'] = False



for sec in sections:
    sub = df[df["section"] == sec]
    daily = sub.resample("D", on="start_time")["percentage_value"].mean()
    plt.plot(daily.index, daily.values, label=f"{sec}(grouped daily)")

plt.xlabel("Time")
plt.ylabel("In-use Berthage Percentage (%)")
plt.title("Hourly Berthage Usage Percentage for Selected Sections")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig("section_usage_trend.png", dpi=300)
print("Saved figure to section_usage_daily_trend.png")
