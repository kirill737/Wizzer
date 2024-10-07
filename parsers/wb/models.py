"""
TEMPLATE DOCSTRING
"""
from typing import List
from pydantic import BaseModel

# Вспомогательные функции
# def getModel(text):
#     # Регулярное выражение для поиска модели iPhone, включая такие варианты, как "Pro Max", "mini", "Pro", и т.д.
#     model_pattern = r"(iphone\s*(\d+|XS|SE|XR)?\s*(mini|pro max|pro max plus|pro|max|promax|plus)?\s*)"
#     model_match = re.search(model_pattern, text, re.IGNORECASE)

#     if model_match:
#         model = model_match.group(0).strip()
#         return model.capitalize()
#     else:
#         return ""
#     return None

# @staticmethod
# def getMemory(text):
#     memory_pattern = r"(\d+)\s*(gb|гб|tb|тб)"
#     memory_match = re.search(memory_pattern, text, re.IGNORECASE)

#     if memory_match:
#         memory_size = memory_match.group(1)
#         memory_unit = memory_match.group(2).lower()

#         if memory_unit in ["gb", "гб"]:
#             return f"{memory_size}GB"
#         elif memory_unit in ["tb", "тб"]:
#             return f"{memory_size}TB"
#     else:
#         return ""

#     return None

# Модель для размеров (sizes)


class Price(BaseModel):
    total: int


class Size(BaseModel):
    price: Price


class Color(BaseModel):
    name: str
# Модель продукта


class Product(BaseModel):
    brand: str
    brandId: int
    id: int
    name: str  # fullname
    colors: List[Color]  # [{"name": "белый"}]
    sizes: List[Size]  # [{"total": 6449300}]
    rating: float
    reviewRating: float
    feedbacks: int

    # Дополнительные поля, которые будут вычисляться автоматически
    # model: Optional[str] = None
    # memory: Optional[str] = None
    # color: Optional[str] = None
    # price: Optional[float] = None
    # Валидация fullname, model, memory
    # @model_validator(mode='before')
    # def process_fullname(cls, values):
    #     fullname = values.get('name', '')
    #     # values['model'] = getModel(fullname)
    #     # values['memory'] = getMemory(fullname)
    #     # values['color'] =
    #     return values

# Модель данных, содержащая список продуктов


class Data(BaseModel):
    products: List[Product]

# Модель для входного JSON


class InputJSON(BaseModel):
    state: int
    version: int
    payloadVersion: int
    data: Data

# Модель для выходного JSON


class OutputProduct(BaseModel):
    brand: str
    brandId: int
    id: int
    color: str
    fullname: str
    # model: str
    # memory: str
    rating: float
    reviewRating: float
    feedbacks: int
    price: float

    # Валидатор для создания нового объекта на основе Product
    @classmethod
    def from_product(cls, product: Product):
        return cls(
            brand=product.brand,
            brandId=product.brandId,
            id=product.id,
            color=product.colors[0].name if product.colors else "",
            fullname=product.name,
            # model=product.model,
            # memory=product.memory,
            rating=product.rating,
            reviewRating=product.reviewRating,
            feedbacks=product.feedbacks,
            price=product.sizes[0].price.total / 100
        )
