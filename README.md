# Xingyuan Charts · public chart data (China's 9 music platforms)

Twice-daily, machine-readable snapshots of the **public charts** on nine Chinese music
platforms — NetEase Cloud Music, QQ Music, Kugou, Kuwo, Qishui, Douyin, Weibo, Bilibili
and Apple Music. Eighteen charts per snapshot: hot/rising boards plus new-song boards.

This repository is the data mirror of <https://xingyuan.beer/charts.json>. It is updated
after each collection run (09:40 and 21:40 Asia/Shanghai, twice a day).

<!-- LATEST:BEGIN -->
| field | value |
|---|---|
| captured_at | `2026-11-19T18:06:26+08:00` |
| boards | 19 |
| rows | 1740 |
| cross-platform songs | 12 |
| key_version | `1` |

Download: [`data/latest.json`](data/latest.json) · [`data/latest.csv`](data/latest.csv)
<!-- LATEST:END -->

## This week (2026-11-09 → 2026-11-16)

Twelve boards were live on both days (of eighteen live now). They held 432 distinct tracks at
the start of the week and 428 at the end: 190 arrived, 194 left. Arrivals and departures are close
to balanced, so the interesting number is not the turnover but who moved where.

The largest single climb was 《烂奇迹（不小心惹了上帝）》 by 杨羊烊, Kugou Top 500 #34 → #4 (+30).
The Douyin audio carrying it is a 104-second edit, roughly three minutes shorter than the version
Kugou charts — the clip that spreads and the recording that earns are not the same file. The widest
runner was 《慌啥子嘛》: two platforms at the start, four now, with 赵本山's version at #1 on Kugou
Top 500 and 村口吴老二's original just behind at #2. 《5th》 by 石衍恺 added the most places without
gaining a platform (NetEase Rising #47 → #13, +34) — still a single-board story, not a run.

Board stickiness reads as clearly as the arrivals: Bilibili kept every compared row, NetEase Hot
Songs 92%, Apple Music 90%, while Douyin's challenge board kept 7 of 50 and Kugou Rising kept none.
Housekeeping note: ten boards got deeper during the week (Kuwo Hot Songs 20 → 100 ranks) and six
went live mid-week (all the new-song boards). Every count above stops at the depth both days read,
so extra coverage never becomes an arrival.

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
