from typing import Any, Dict, List, Union

import uvicorn
from fastapi import FastAPI, Request, Response, status
from loguru import logger

from app.core.config import settings
from app.core.mongo import all_templates, get_database, get_templates
from app.core.util import get_type

app = FastAPI()


@app.post("/get_forms", status_code=200, include_in_schema=False)
def get_forms(req: Request, response: Response) -> Union[List[Any], Dict[Any, Any]]:
    request_args = dict(req.query_params)
    all_args = req.query_params._list
    if request_args == {}:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return []
    if len(request_args) != len(all_args):
        response.status_code = status.HTTP_409_CONFLICT
        return []
    fields = set([get_type(item) for item in all_args])
    db = get_database()
    all_selected_templates = get_templates(db, fields)
    template_names = []
    for template in all_selected_templates:
        template_signature = set([(item, template[item]) for item in template if item not in ('_id', 'name')])
        if template_signature.issubset(fields):
            template_names.append(template["name"])

    if len(template_names) == 0:
        template_dict = {item[0]: item[1] for item in fields}
        return template_dict
    return template_names


@app.get("/forms", status_code=200)
def forms() -> list:
    db = get_database()
    all_data = all_templates(db)

    return all_data


if __name__ == "__main__":
    logger.info(
        f"settings.SERVER_HOST {settings.SERVER_HOST} "
        f"settings.SERVER_PORT: {settings.SERVER_PORT}"
    )
    uvicorn.run(app, host=settings.SERVER_HOST.host, port=settings.SERVER_PORT)
