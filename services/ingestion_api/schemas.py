from marshmallow import Schema, fields, validate


class EventSchema(Schema):
    event_type = fields.Str(required=True, validate=validate.Length(min=1))
    deployment_id = fields.Str(required=False)
    component_name = fields.Str(required=False)
    status = fields.Str(required=False)
    message = fields.Str(required=False)
    payload = fields.Dict(required=False)
