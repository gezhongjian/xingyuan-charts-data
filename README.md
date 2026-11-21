# Xingyuan Charts · public chart data (China's 9 music platforms)

Twice-daily, machine-readable snapshots of the **public charts** on nine Chinese music
platforms — NetEase Cloud Music, QQ Music, Kugou, Kuwo, Qishui, Douyin, Weibo, Bilibili
and Apple Music. Nineteen charts per snapshot: hot/rising boards, new-song boards, and the
Douyin challenge board.

This repository is the data mirror of <https://xingyuan.beer/charts.json>. It is updated
after each collection run (09:40 and 21:40 Asia/Shanghai, twice a day).

<!-- LATEST:BEGIN -->
| field | value |
|---|---|
| captured_at | `2026-11-21T09:40:05+08:00` |
| boards | 19 |
| rows | 1745 |
| cross-platform songs | 12 |
| key_version | `1` |

Download: [`data/latest.json`](data/latest.json) · [`data/latest.csv`](data/latest.csv)
<!-- LATEST:END -->

## This week (2026-11-14 → 2026-11-21)

Eighteen boards were live on both days (nineteen now; QQ Music's Douyin Hot Songs came online on
11-17 and is left out below). Read at the depth both days had, they held 1,128 distinct tracks a
week ago and 1,121 today: 525 arrived, 532 left. Bilibili kept every row and Apple Music 95%; the
fast boards turned over almost completely — Kugou's 6666 board kept 1%, Qishui's new-song board 2%.

The largest same-board climb was 《牡丹亭》 by 浅影阿, Kuwo Hot Songs #98 → #13 (+85). The widest
runner was "time machine" by mj apanay and aren park — one board a week ago, four now — tied with
队长's 《哪里都是你》. Weibo's board went from 73 to 100 ranks mid-week; every count above stops at
the depth both days read, so the extra rows never turn into "arrivals".

Live view: <https://xingyuan.beer/trends?src=github> · weekly report: <https://xingyuan.beer/reports?src=github>

## Files

| path | what |
|---|---|
| `data/latest.json` | the newest snapshot, same schema as `/charts.json` |
| `data/latest.csv` | flat table, one row per chart position |
| `data/<YYYY-MM-DD>/<HHMM>.json` | per-run archive (kept, never rewritten) |

## Schema (`data/latest.json`)

| field | meaning |
|---|---|
| `captured_at` | when the chart pages were read (Asia/Shanghai). Every number in the file refers to this moment. |
| `boards[]` | one object per chart: `platform`, `board`, `board_name`, `kind` (`base` / `rise`), `total`, `tracks[]` |
| `tracks[].rank` | position on that chart (platform's own numbering) |
| `tracks[].rank_delta` | `> 0` moved up, `< 0` moved down, `0` unchanged, `null` no previous run |
| `tracks[].is_new` | first appearance on that chart |
| `tracks[].streak` | consecutive runs on the chart |
| `tracks[].dedupe_key` | cross-platform identity key (title + lead artist, normalised). Same key = same song on different platforms. |
| `cross[]` | songs charting on two or more platforms in this run |
| `citation` | the preferred citation line for this snapshot |
| `limits` | what the snapshot does and does not contain. Files committed before 2026-11-19 carry an older sentence that denied bulk/history access; archives are never rewritten, so those files keep it verbatim. `data/latest.json`/`latest.csv` and every later archive state that bulk and per-run history live here. |

Chart depth is what we mirror from the site snapshot, capped at 100 rows per board: the
11-13 09:40 run carries 100 rows on NetEase, QQ, Kugou, Kuwo and Apple; 97 on Bilibili,
60 on Weibo, 50 on Qishui and Douyin. We never pad a chart to a round number.

## What this is not

- No play counts, no revenue, no estimates — only published positions.
- No audio, no lyrics, no cover-art mirroring.
- No user data. Ever.

## Using it

```bash
curl -sL https://raw.githubusercontent.com/gezhongjian/xingyuan-charts-data/main/data/latest.json | jq '.boards | length'
```

If you quote this data, cite **Xingyuan Charts (星愿榜单)** with the `captured_at` value,
and link <https://xingyuan.beer/?src=github>.

## Update cadence

Two runs per day. A missing run means the platforms blocked that collection — the archive
keeps the previous snapshot intact rather than writing a partial one.

## License

Data: CC BY 4.0 (attribution as above). The build scripts live in the site repository.
