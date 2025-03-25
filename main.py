import uvicorn
from fastapi import FastAPI, Query, Body, Path
from fastapi.openapi.docs import get_swagger_ui_html

app = FastAPI(docs_url=None)

hotels = [
    {"id": 1, "title": "Sochi", "name": "Laguna"},
    {"id": 2, "title": "Дубай", "name": "Grand"},
]


@app.put("/hotels/{hotel_id}")
def change_hotel_all_values(
        hotel_id: int = Path(description="Айдишник отеля"),
        title: str = Body(description="Новый title отеля"),
        name: str = Body(description="Новое имя отеля")
):
    data = None
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            data = hotel

        return {"message": "successfully changed!", "data": data}


@app.patch("/hotels/{hotel_id}")
def change_hotel_value(
        hotel_id: int = Path(description="Айдишник отеля"),
        title: str | None = Body(default=None, description="Новый title отеля"),
        name: str | None = Body(default=None, description="Новое имя отеля")
):
    data = None
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title is not None:
                hotel["title"] = title
            if name is not None:
                hotel["name"] = name
            data = hotel

    return {"message": "Successfully changed", "data": data}


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
