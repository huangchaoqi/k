import json
import os
from pathlib import Path

import akshare as ak
import pandas as pd


START = "2011-01-01"
END = os.environ.get("END_MONTH")
CITIES = ["上海", "南京", "成都", "昆明", "珠海", "广州", "深圳"]


def city_rows(df, city: str) -> list[dict]:
    city_df = df[df["城市"] == city].copy()
    city_df["日期"] = city_df["日期"].astype(str)
    city_df = city_df[city_df["日期"] >= START]
    if END:
        city_df = city_df[city_df["日期"] <= END]
    city_df = city_df.sort_values("日期")

    rows = []
    previous_close = None
    for _, row in city_df.iterrows():
        date = str(row["日期"])[:7]
        mom = float(row["二手住宅价格指数-环比"])
        fixed = row["二手住宅价格指数-定基"]
        fixed_value = None if fixed != fixed else float(fixed)

        if previous_close is None:
            close = fixed_value if fixed_value is not None else 100.0 * mom / 100.0
            open_value = close / (mom / 100.0)
        else:
            open_value = previous_close
            close = open_value * mom / 100.0

        previous_close = close
        rows.append(
            {
                "date": date,
                "mom": round(mom, 3),
                "open": round(open_value, 4),
                "high": round(max(open_value, close), 4),
                "low": round(min(open_value, close), 4),
                "close": round(close, 4),
                "fixed": None if fixed_value is None else round(fixed_value, 3),
            }
        )
    return rows


def main() -> None:
    frames = []
    for index in range(0, len(CITIES), 2):
        first = CITIES[index]
        second = CITIES[index + 1] if index + 1 < len(CITIES) else CITIES[0]
        frames.append(ak.macro_china_new_house_price(city_first=first, city_second=second))

    df = pd.concat(frames, ignore_index=True)
    df = df.drop_duplicates(subset=["日期", "城市"])

    data = {}
    for city in CITIES:
        rows = city_rows(df, city)
        if not rows:
            print(f"{city}: no same-source index data found, skipped")
            continue
        data[city] = rows
        print(f"{city}: {len(rows)} rows, {rows[0]['date']} to {rows[-1]['date']}")

    output = "window.HOUSE_PRICE_DATA = "
    output += json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    output += ";\n"
    Path("shanghai-house-price-data.js").write_text(output, encoding="utf-8")
    print("Wrote shanghai-house-price-data.js")


if __name__ == "__main__":
    main()
