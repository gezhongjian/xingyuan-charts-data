#!/usr/bin/env python3
"""xingyuan — 星愿榜单命令行（给人和 agent 用，零依赖，只读公开数据）。

    python3 xingyuan.py charts --platform netease --limit 5
    python3 xingyuan.py risers --limit 5
    python3 xingyuan.py cross --min 3
    python3 xingyuan.py song "雨爱"
    python3 xingyuan.py ask "这周做什么能蹭流量"     # 需订阅 token（见 subscribe）

设计取舍：只用标准库（urllib/json），不引第三方包，方便 agent 直接跑；
默认输出 JSON（--table 给人看），错误只回结构化 JSON，不用异常栈。
"""
from __future__ import annotations

import argparse
import json
import os
import ssl
import sys
import urllib.error
import urllib.request

BASE = os.environ.get("XINGYUAN_BASE", "https://xingyuan.beer").rstrip("/")
UA = "xingyuan-cli/0.1 (+https://xingyuan.beer/agent.txt)"


def _ctx():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:  # noqa: BLE001
        return ssl.create_default_context()


def get(path: str, timeout: float = 25.0):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout, context=_ctx()) as resp:
        return json.loads(resp.read())


def post(path: str, payload: dict, timeout: float = 60.0):
    req = urllib.request.Request(BASE + path, data=json.dumps(payload).encode(), method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", UA)
    with urllib.request.urlopen(req, timeout=timeout, context=_ctx()) as resp:
        return json.loads(resp.read())


def _charts() -> dict:
    return get("/charts.json")


def cmd_charts(a) -> int:
    data = _charts()
    rows = []
    for b in data.get("boards") or []:
        if a.platform and b.get("platform") != a.platform:
            continue
        if a.board and a.board not in str(b.get("board") or ""):
            continue
        for t in (b.get("tracks") or [])[:a.limit]:
            rows.append({"platform": b.get("platform"), "board": b.get("board_name"),
                         "rank": t.get("rank"), "name": t.get("title"),
                         "artist": ",".join(t.get("artists") or []), "delta": t.get("rank_delta")})
    return _emit(rows, a, ("rank", "name", "artist", "board", "delta"))


def cmd_risers(a) -> int:
    data = _charts()
    rows = []
    for b in data.get("boards") or []:
        for t in b.get("tracks") or []:
            d = t.get("rank_delta") or 0
            if d > 0:
                rows.append({"name": t.get("title"), "artist": ",".join(t.get("artists") or []),
                             "delta": d, "platform": b.get("platform"),
                             "board": b.get("board_name"), "rank": t.get("rank")})
    rows.sort(key=lambda r: -r["delta"])
    return _emit(rows[:a.limit], a, ("delta", "name", "artist", "platform", "rank"))


def cmd_cross(a) -> int:
    data = _charts()
    seen: dict[str, dict] = {}
    for b in data.get("boards") or []:
        for t in b.get("tracks") or []:
            key = t.get("dedupe_key") or t.get("title")
            if not key:
                continue
            rec = seen.setdefault(key, {"name": t.get("title"), "artist": ",".join(t.get("artists") or []),
                                        "platforms": []})
            if b.get("platform") not in rec["platforms"]:
                rec["platforms"].append(b.get("platform"))
    rows = [{"name": r["name"], "artist": r["artist"], "platforms": len(r["platforms"]),
             "on": ",".join(r["platforms"])} for r in seen.values()
            if len(r["platforms"]) >= a.min]
    rows.sort(key=lambda r: -r["platforms"])
    return _emit(rows[:a.limit], a, ("platforms", "name", "artist", "on"))


def cmd_song(a) -> int:
    data = _charts()
    q = (a.query or "").strip().lower()
    hits = []
    for b in data.get("boards") or []:
        for t in b.get("tracks") or []:
            if q and q not in f"{t.get('title','')} {' '.join(t.get('artists') or [])}".lower():
                continue
            hits.append({"name": t.get("title"), "artist": ",".join(t.get("artists") or []),
                         "platform": b.get("platform"), "board": b.get("board_name"),
                         "rank": t.get("rank"), "delta": t.get("rank_delta")})
    return _emit(hits[:a.limit], a, ("name", "artist", "platform", "board", "rank"))


def cmd_ask(a) -> int:
    token = a.token or os.environ.get("XINGYUAN_TOKEN", "")
    if not token:
        print(json.dumps({"ok": False, "error": "need_token",
                          "hint": "订阅后你的订单 token 就是凭据；见 https://xingyuan.beer/subscribe?cat=smart"},
                         ensure_ascii=False))
        return 2
    try:
        out = post("/api/ask", {"token": token, "question": a.question,
                                "cli": "xingyuan/" + "0.1"})
    except urllib.error.HTTPError as exc:
        print(json.dumps({"ok": False, "status": exc.code,
                          "body": exc.read(300).decode("utf-8", "replace")}, ensure_ascii=False))
        return 1
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0



def cmd_subscribe(a) -> int:
    """下单：POST /api/order → 服务端把 6 位验证码发到这个邮箱。"""
    try:
        out = post("/api/order", {"email": a.email, "src": "cli"})
    except urllib.error.HTTPError as exc:
        print(json.dumps({"ok": False, "status": exc.code,
                          "body": exc.read(300).decode("utf-8", "replace")}, ensure_ascii=False))
        return 1
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out.get("ok") else 1


def cmd_verify(a) -> int:
    """验码：POST /api/verify → 拿订单页面（支付入口）。"""
    try:
        out = post("/api/verify", {"order_id": a.order_id, "code": a.code})
    except urllib.error.HTTPError as exc:
        print(json.dumps({"ok": False, "status": exc.code,
                          "body": exc.read(300).decode("utf-8", "replace")}, ensure_ascii=False))
        return 1
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out.get("ok") else 1


def _emit(rows: list[dict], a, cols: tuple[str, ...]) -> int:
    if a.table:
        widths = {c: max(len(c), *(len(str(r.get(c, ""))) for r in rows)) if rows else len(c)
                  for c in cols}
        print("  ".join(c.ljust(widths[c]) for c in cols))
        for r in rows:
            print("  ".join(str(r.get(c, "")).ljust(widths[c]) for c in cols))
        return 0
    print(json.dumps(rows, ensure_ascii=False, indent=2))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="xingyuan", description="星愿榜单 CLI（公开数据只读）")
    ap.add_argument("--base", default=BASE, help="服务地址（默认 https://xingyuan.beer）")
    ap.add_argument("--table", action="store_true", help="表格输出（默认 JSON）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("charts", help="按榜取前 N")
    p.add_argument("--platform")
    p.add_argument("--board")
    p.add_argument("--limit", type=int, default=10)
    p.set_defaults(func=cmd_charts)

    p = sub.add_parser("risers", help="涨得最快的")
    p.add_argument("--limit", type=int, default=10)
    p.set_defaults(func=cmd_risers)

    p = sub.add_parser("cross", help="跨平台同时在榜")
    p.add_argument("--min", type=int, default=3)
    p.add_argument("--limit", type=int, default=10)
    p.set_defaults(func=cmd_cross)

    p = sub.add_parser("song", help="查单曲在各榜的名次")
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=10)
    p.set_defaults(func=cmd_song)


    p = sub.add_parser("subscribe", help="下单：用你的邮箱订阅（会把验证码发到邮箱）")
    p.add_argument("--email", required=True)
    p.set_defaults(func=cmd_subscribe)

    p = sub.add_parser("verify", help="验码：拿订单页面（支付入口）")
    p.add_argument("--order-id", required=True)
    p.add_argument("--code", required=True)
    p.set_defaults(func=cmd_verify)

    p = sub.add_parser("ask", help="向星愿提问（需订阅 token）")
    p.add_argument("question")
    p.add_argument("--token", default="")
    p.set_defaults(func=cmd_ask)

    # --table 允许写在子命令后面（人更常这么打）
    argv = list(argv if argv is not None else sys.argv[1:])
    if "--table" in argv:
        i = argv.index("--table")
        argv.pop(i)
        argv.insert(0, "--table")
    a = ap.parse_args(argv)
    if a.base:
        globals()["BASE"] = a.base.rstrip("/")
    try:
        return a.func(a)
    except urllib.error.URLError as exc:
        print(json.dumps({"ok": False, "error": "network", "detail": str(exc)[:120]},
                         ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
