"""
Задание 1. Наполнение данными
Добавьте в базу данных категории и продукты.
 1. Добавление категорий: Добавьте в таблицу categories следующие категории:
 ○ Название: "Электроника", Описание: "Гаджеты и устройства."
 ○ Название: "Книги", Описание: "Печатные книги и электронные книги."
 ○ Название: "Одежда", Описание: "Одежда для мужчин и женщин."
 2. Добавление продуктов: Добавьте в таблицу products следующие продукты, убедившись, что каждый продукт связан с
 соответствующей категорией:
 ○ Название: "Смартфон", Цена: 299.99, Наличие на складе: True, Категория: Электроника
 ○ Название: "Ноутбук", Цена: 499.99, Наличие на складе: True, Категория: Электроника
 ○ Название: "Научно-фантастический роман", Цена: 15.99, Наличие на складе: True, Категория: Книги
 ○ Название: "Джинсы", Цена: 40.50, Наличие на складе: True, Категория: Одежда
 ○ Название: "Футболка", Цена: 20.00, Наличие на складе: True, Категория: Одежда
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, create_engine, update, func
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


Base = declarative_base()


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)

    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    in_stock = Column(Boolean, default=True)

    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")

# отключил INFO засоряют чат для включения нужно изменить параметр echo=True
engine = create_engine("sqlite:///shop.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)


# Запускал код пару раз чтобы проверить и добавил небольшую проверку/костыль чтобы не дублировал данные
def seed_data():
    if session.query(Category).count() > 0:
        print("Данные уже внесены")
        print("-" * 40)
        return

    electronics = Category(name="Электроника", description="Гаджеты и устройства.")
    books = Category(name="Книги", description="Печатные книги и электронные книги.")
    clothes = Category(name="Одежда", description="Одежда для мужчин и женщин.")

    session.add_all([electronics, books, clothes])
    session.commit()

    products = [
        Product(name="Смартфон", price=299.99, in_stock=True, category=electronics),
        Product(name="Ноутбук", price=499.99, in_stock=True, category=electronics),
        Product(name="Научно-фантастический роман", price=15.99, in_stock=True, category=books),
        Product(name="Джинсы", price=40.50, in_stock=True, category=clothes),
        Product(name="Футболка", price=20.00, in_stock=True, category=clothes),
    ]

    session.add_all(products)
    session.commit()
    print("Данные добавлены")



"""
Задание 2. Чтение данных
Извлеките все записи из таблицы categories. Для каждой категории извлеките и выведите все связанные с ней продукты, 
включая их названия и цены.
"""

def read_data():
    categories = session.query(Category).all()
    for category in categories:
        print(f"Категория: {category.name} ({category.description})")
        if category.products:
            for product in category.products:
                print(f"  - {product.name}: {product.price} €")
        else:
            print("  (Нет продуктов)")
        print("-" * 40)



"""
Задание 3. Обновление данных
Найдите в таблице products первый продукт с названием "Смартфон". Замените цену этого продукта на 349.99.
"""

smartphone = session.query(Product).filter_by(name="Смартфон").first()

if smartphone:
    print("-" * 40)
    print(f"До обновления: {smartphone.name} стоит {smartphone.price} €")

    smartphone.price = 349.99
    session.commit()

    print(f"После обновления: {smartphone.name} стоит {smartphone.price} €")
    print("-" * 40)
else:
    print("Продукт 'Смартфон' не найден!")

"""
Задание 4. Агрегация и группировка
Используя агрегирующие функции и группировку, подсчитайте общее количество продуктов в каждой категории.
"""


category_counts = session.query(
    Category.name,
    func.count(Product.id).label("product_count")
).join(Product).group_by(Category.id).all()

for cat_name, count in category_counts:
    print(f"- {cat_name}: {count} продуктов")

print("-" * 40)

"""
Задание 5. Группировка с фильтрацией
Отфильтруйте и выведите только те категории, в которых более одного продукта.
"""

categories_multiple_products = session.query(
    Category.name,
    func.count(Product.id).label("product_count")
).join(Product).group_by(Category.id).having(func.count(Product.id) > 1).all()

for cat_name, count in categories_multiple_products:
    print(f"- {cat_name}: {count} продуктов")

print("-" * 40)


if __name__ == "__main__":
    seed_data()
    read_data()
