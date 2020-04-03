from sqlalchemy import Column, String, Integer
from .entity import Entity, Base

from marshmallow import Schema, fields

class LogEntry (Entity, Base):
    __tablename__ = 'log_entry'

    title = Column(String)
    description = Column(String)

    def __init__(self, title, description, created_by):
        Entity.__init__(self, created_by)
        self.title = title
        self.description = description

class LogSchema(Schema):
    id = fields.Number()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    last_updated_by = fields.Str()
    ips = fields.Str()
    date = fields.DateTime()
    command = fields.Str()
    resource = fields.Str()
    proto = fields.Str()
    response =fields.Int()
    size = fields.Int()
    info = fields.Str()