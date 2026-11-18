# xingyuan — 星愿榜单 CLI

九平台中文音乐榜单的命令行客户端。**零依赖**（Python 3.9+ 标准库），专为「人和 agent 都能直接跑」设计：默认输出 JSON，`--table` 给人看。

## 安装

```bash
# 直接用，不安装
python3 xingyuan.py risers --limit 5 --table

# 或放进 PATH
curl -O https://raw.githubusercontent.com/gezhongjian/xingyuan-charts-data/main/cli/xingyuan.py
chmod +x xingyuan.py && mv xingyuan.py ~/.local/bin/xingyuan
```

## 用法

```bash
xingyuan charts --platform netease --limit 5      # 按榜取前 N（--board 热歌榜 可筛榜名）
xingyuan risers --limit 10 --table                # 涨得最快的
xingyuan cross --min 4 --table                    # 跨平台同时在榜（≥4 个平台）
xingyuan song "雨爱" --table                       # 单曲在各榜的名次
xingyuan subscribe --email you@example.com        # 下单：验证码发到这个邮箱
xingyuan verify --order-id XY... --code 123456     # 验码 → 返回订单页（支付入口）
xingyuan ask "这周做什么能蹭流量"                   # 提问（需订阅 token）
```

## 给 agent 的约定

- 默认输出 JSON 数组；出错输出 `{"ok": false, "error": "..."}`，退出码非 0，不用解析栈。
- `--base` 或 `XINGYUAN_BASE` 可指向镜像/本地实例。
- 下单三步：`subscribe`（拿 order_id）→ 查收 6 位验证码 → `verify`（拿订单页）→ 支付。
  服务端接口：`POST /api/order`、`POST /api/verify`（JSON，无 Cookie、无 CSRF，限流同网页）。
- `ask` 需要订阅：`XINGYUAN_TOKEN=<订单 token>` 或 `--token`，凭据不落盘。
- 数据契约：<https://xingyuan.beer/charts.json>（`contract_version` 字段）；agent 说明在 `/agent.txt`。

## 数据来源与边界

榜单来自九个平台的**公开榜单页**，每天两班只读快照；不登录、不绕过风控、不转售音频。
只引用名次与名次变化，不构成收益承诺。
