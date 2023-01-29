from database.core import crud
from database.common.models import History, db
from tg_API import core
from site_API.core import headers, params, site_api, url


db_write = crud.create()
db_read = crud.retrieve()