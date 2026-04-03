# Настройки экономики
START_MONEY = 2000
CIRCLE_BONUS = 500
TAX_AMOUNT = 200

# Игровое поле (0 - СТАРТ, 6 - ТЮРЬМА, 18 - ОТПРАВЛЯЙТЕСЬ В ТЮРЬМУ)
BOARD = [
    {"name": "СТАРТ", "type": "start"},
    {"name": "Улица Лосяша 🟧", "type": "property", "price": 100},
    {"name": "НАЛОГ", "type": "tax"},
    {"name": "МАГАЗИН", "type": "shop"},
    {"name": "Улица Лилейная 🟧", "type": "property", "price": 115},
    {"name": "Проспект Чилла 🟧", "type": "property", "price": 145},
    {"name": "ТЮРЬМА (Экскурсия)", "type": "jail_visit"},
    {"name": "Могила Им. Марка 🟫", "type": "property", "price": 180},
    {"name": "ШАНС", "type": "chance"},
    {"name": "МАГАЗИН", "type": "shop"},
    {"name": "Могила им. Империи Слэя 🟫", "type": "property", "price": 220},
    {"name": "Могила Им. Шифунова 🟫", "type": "property", "price": 260},
    {"name": "Зона Отдыха", "type": "rest"},
    {"name": "НАЛОГ", "type": "tax"},
    {"name": "Улица Империи Слэя 🟪", "type": "property", "price": 305},
    {"name": "МАГАЗИН", "type": "shop"},
    {"name": "Набережная Тюленей 🟪", "type": "property", "price": 350},
    {"name": "Улица Парка Любви 🟪", "type": "property", "price": 400},
    {"name": "ОТПРАВЛЯЙТЕСЬ В ТЮРЬМУ", "type": "go_to_jail"},
    {"name": "Улица Ледяной Вечеринки 🟦", "type": "property", "price": 495},
    {"name": "Улица Им. Марины Вип Люкс 🟦", "type": "property", "price": 550},
    {"name": "МАГАЗИН", "type": "shop"},
    {"name": "ШАНС", "type": "chance"},
    {"name": "Улица Им. Варфоломея 🟦", "type": "property", "price": 450}
]
