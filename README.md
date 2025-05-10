# description
Simple sample for MCP Client and MCP Server

![](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/2266010/02527af1-32b8-4c8f-9229-7365cac18c9e.gif)

notice: If you do scrape, we recommend that you pay attention to the site's terms and conditions and only do so for personal use.

# how to use
## folder structure
```
L mcp-client (mcp library)
L mcp-server (fastapi)
```

## setup
use [rye](https://rye.astral.sh/)

1. mcp-server
```
$ rye sync
```

2. mcp-client
```
// fill your OPENAI_API_KEY=sk-proj-*
$ cp .env.sample .env

$ rye sync
```

## execute
1. mcp-server
```
$ rye run python src/main.py
```
server launched: http://localhost:8000

2. mcp-client
```
$ rye run python src/main.py
```
