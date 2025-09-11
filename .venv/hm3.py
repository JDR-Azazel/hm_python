from sqlalchemy import create_engine, Column, Integer, String, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


# Задача 1: Создайте экземпляр движка для подключения к SQLite базе данных в памяти.
engine = create_engine("sqlite:///:memory:", echo=True)
Base = declarative_base()


# Задача 3: Определите модель продукта Product со следующими типами колонок:
# id: числовой идентификатор
# name: строка (макс. 100 символов)
# price: числовое значение с фиксированной точностью
# in_stock: логическое значение

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    in_stock = Column(Boolean, default=True)

# Задача 5: Установите связь между таблицами Product и Category с помощью колонки category_id.
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")



# Задача 4: Определите связанную модель категории Category со следующими типами колонок:
# id: числовой идентификатор
# name: строка (макс. 100 символов)
# description: строка (макс. 255 символов)

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))

    products = relationship("Product", back_populates="category")


# Задача 2: Создайте сессию для взаимодействия с базой данных, используя созданный движок.
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()
Base.metadata.create_all(engine)

category1 = Category(name="Электроника", description="Гаджеты и устройства")
product1 = Product(name="Смартфон", price=599.99, in_stock=True, category=category1)

session.add(category1)
session.add(product1)
session.commit()

for product in session.query(Product).all():
    print(f"Товар: {product.name}, Категория: {product.category.name}")
