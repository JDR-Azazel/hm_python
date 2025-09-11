"""
Разработать систему регистрации пользователя, используя Pydantic для валидации входных данных, обработки вложенных 
структур и сериализации. Система должна обрабатывать данные в формате JSON.
Задачи:

1. Создать классы моделей данных с помощью Pydantic для пользователя и его адреса.
2. Реализовать функцию, которая принимает JSON строку, десериализует её в объекты Pydantic, валидирует данные, и в 
случае успеха сериализует объект обратно в JSON и возвращает его.
3. Добавить кастомный валидатор для проверки соответствия возраста и статуса занятости пользователя.
4. Написать несколько примеров JSON строк для проверки различных сценариев валидации: успешные регистрации и случаи, 
когда валидация не проходит (например возраст не соответствует статусу занятости).

Модели:
- Address: Должен содержать следующие поля:

city: строка, минимум 2 символа.
street: строка, минимум 3 символа.
house_number: число, должно быть положительным.

User: Должен содержать следующие поля:

name: строка, должна быть только из букв, минимум 2 символа.
age: число, должно быть между 0 и 120.
email: строка, должна соответствовать формату email.
is_employed: булево значение, статус занятости пользователя.
address: вложенная модель адреса.

Валидация:
Проверка, что если пользователь указывает, что он занят (is_employed = true), его возраст должен быть от 18 до 65 лет.
"""
from pydantic import BaseModel, Field, EmailStr, field_validator
import json

class Address(BaseModel):
    city: str = Field(..., min_length=2)
    street: str = Field(..., min_length=3)
    house_number: int = Field(..., gt=0)


class User(BaseModel):
    name: str = Field(..., min_length=2, pattern=r'^[A-Za-zА-Яа-яЁё\s]+$')
    age: int = Field(..., ge=0, le=120)
    email: EmailStr
    is_employed: bool
    address: Address

    @field_validator("is_employed")
    def check_age_for_employment(cls, v, info):
        age = info.data["age"]
        if v and not (18 <= age <= 65):
            raise ValueError("Работающий пользователь должен быть в возрасте от 18 до 65 лет.")
        return v


def process_user_registration(json_str: str) -> str:
    try:
        user = User.model_validate_json(json_str)

        return user.model_dump_json(indent=4)

    except Exception as e:
        return f"Ошибка валидации: {e}"


    except Exception as e:
        return f"Ошибка валидации: {e}"


json_valid = """{
    "name": "Alan",
    "age": 23,
    "email": "alan@example.com",
    "is_employed": true,
    "address": {
        "city": "Lübek",
        "street": "Oistr",
        "house_number": 3
    }
}"""

json_invalid_age = """{
    "name": "John Doe",
    "age": 70,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}"""

json_invalid_name = """{
    "name": "Alex3D",
    "age": 38,
    "email": "Al@example.com",
    "is_employed": true,
    "address": {
        "city": "Hamburg",
        "street": "Gatti",
        "house_number": 9
    }
}"""

if __name__ == "__main__":
    print("---- Успешный случай ----")
    print(process_user_registration(json_valid))

    print("\n---- Ошибка: возраст ----")
    print(process_user_registration(json_invalid_age))

    print("\n---- Ошибка: имя ----")
    print(process_user_registration(json_invalid_name))
