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
