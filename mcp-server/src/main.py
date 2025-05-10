from fastapi_mcp import FastApiMCP
import uvicorn

from api import app

mcp = FastApiMCP(
    app,
    name="suumo_mcp",
    description="SUUMOの賃貸リストを取得する",
)
mcp.mount()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

