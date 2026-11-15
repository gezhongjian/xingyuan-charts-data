# Xingyuan Charts · public chart data (China's 9 music platforms)

Twice-daily, machine-readable snapshots of the **public charts** on nine Chinese music
platforms — NetEase Cloud Music, QQ Music, Kugou, Kuwo, Qishui, Douyin, Weibo, Bilibili
and Apple Music. Eighteen charts per snapshot: hot/rising boards plus new-song boards.

This repository is the data mirror of <https://xingyuan.beer/charts.json>. It is updated
after each collection run (09:40 and 21:40 Asia/Shanghai, twice a day).

<!-- LATEST:BEGIN -->
| field | value |
|---|---|
| captured_at | `2026-11-15T09:40:04+08:00` |
| boards | 18 |
| rows | 1619 |
| cross-platform songs | 12 |
| key_version | `1` |

Download: [`data/latest.json`](data/latest.json) · [`data/latest.csv`](data/latest.csv)
<!-- LATEST:END -->

## This week (2026-11-09 → 2026-11-15)

The 11-15 09:40 run holds 1,619 rows across 18 boards: 100 rows on the NetEase, QQ, Kugou,
Kuwo and Apple boards, 97 on Bilibili, 72 on Weibo, 50 on Qishui and Douyin. The cross block is
the top 12 songs by platform count, not a census: all 12 sit on at least five of the six
closed-screen platforms, and 9 sit on all six. Ten of the twelve are 2000s–2010s Chinese
catalog tracks — 孙燕姿's 《开始懂了》/《我不难过》/《我怀念的》, 梁静茹《情歌》, 陈奕迅《最佳损友》,
杨丞琳《雨爱》, 许嵩's 《幻听》 and 《天龙八部之宿敌》, 薛之谦《其实》, Suki 刘舒妤《失眠》 — the
exceptions are 李荣浩's 2024 《恋人》 and The Weeknd's 2026 *Hong Kong (feat. 王菲季候风)*.
The useful read is the spread inside one song, not the aggregate: 《我不难过》 is #1 on QQ and
#2 on NetEase and Apple but #25 on Kuwo, and 《开始懂了》 is #14 on Apple but #73 on Kuwo.
Within the week, *Hong Kong* cooled on NetEase from #1 to #7 while 《天龙八部之宿敌》 rose
from #9 to #4. Data note: the Kugou TOP500 was mirrored 50 deep until 11-12 21:40 and 100 deep
after, so platform counts that straddle that change are not comparable. Cross-platform identity
is rebuilt each run from title + lead artist; versions more than 20 seconds apart stay separate.
Live view: <https://xingyuan.beer/trends?src=github>.

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
