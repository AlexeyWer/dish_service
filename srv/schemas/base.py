from marshmallow import EXCLUDE, Schema, ValidationError, fields, validates_schema
from marshmallow.validate import Range


class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE


class Product(BaseSchema):
    name = fields.String(required=True, metadata={"description": "Наименование продукта"})
    measure = fields.String(required=True, metadata={"description": "Мера измерения"})


class ProductResponse(Product):
    id = fields.Integer(required=True, metadata={"description": "ID продукта"})


class DeleteProduct(BaseSchema):
    id = fields.Integer(load_default=None, metadata={"description": "ID продукта"})
    name = fields.String(load_default=None, metadata={"description": "Наименование продукта"})

    @validates_schema
    def check_empty_fields(self, data: dict, *args, **kwargs):
        if not any([value is not None for value in data.values()]):
            return ValidationError("Fill in one of the fields: id/name")


class Dish(BaseSchema):
    name = fields.String(required=True, metadata={"description": "Наименование блюда"})
    description_of_cooking = fields.String(load_default=None, metadata={"description": "Описание приготовления"})


class DishResponse(Dish):
    id = fields.Integer(required=True, metadata={"description": "ID блюда"})


class ProductInDish(BaseSchema):
    dish = fields.Integer(required=True, metadata={"description": "ID блюда"})
    product = fields.Integer(required=True, metadata={"description": "ID продукта"})
    quantity = fields.Float(required=True, validate=Range(min=0) ,metadata={"description": "Количество продукта"})
