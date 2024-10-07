import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as psql


metadata = sa.MetaData()


PRODUCTS = sa.Table(
    "products",
    metadata,
    sa.Column("id", sa.Integer(), primary_key=True),
    sa.Column("name", sa.String(256), unique=True, nullable=False, comment="Наименование продукта"),
    sa.Column("measure", sa.String(32), nullable=False, comment="Мера измерения"),
    sa.Column("created", sa.DateTime(), server_default=sa.func.now()),
    sa.Column("updated", sa.DateTime(), server_default=sa.func.now()),
    comment="Продукты",
)


DISHES = sa.Table(
    "dishes",
    metadata,
    sa.Column("id", sa.Integer(), primary_key=True),
    sa.Column("name", sa.String(256), unique=True, nullable=False, comment="Наименование блюда"),
    sa.Column("description_of_cooking", sa.String(), comment="Описание приготовления блюда"),
    sa.Column("created", sa.DateTime(), server_default=sa.func.now()),
    sa.Column("updated", sa.DateTime(), server_default=sa.func.now()),
    comment="Блюда",
)


PRODUCTS_IN_DISHES = sa.Table(
    "products_in_dishes",
    metadata,
    sa.Column("id", sa.Integer(), primary_key=True),
    sa.Column("dish", sa.Integer(), sa.ForeignKey("dishes.id"), comment="Ссылка на блюдо"),
    sa.Column("product", sa.Integer(), sa.ForeignKey("products.id"), comment="Ссылка на продукт"),
    sa.Column("quantity", psql.NUMERIC(15, 3), sa.CheckConstraint("quantity > 0"), nullable=False, comment="Кол-во продукта в блюде"),
    sa.Column("created", sa.DateTime(), server_default=sa.func.now()),
    sa.Column("updated", sa.DateTime(), server_default=sa.func.now()),
    comment="Продукты в блюдах",
)


class Tables:

    @property
    def dishes(self) -> sa.Table:
        return DISHES
    
    @property
    def products(self) -> sa.Table:
        return PRODUCTS
    
    @property
    def products_in_dishes(self) -> sa.Table:
        return PRODUCTS_IN_DISHES
