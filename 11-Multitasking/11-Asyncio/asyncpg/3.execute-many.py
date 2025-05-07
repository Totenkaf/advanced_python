import asyncpg
import asyncio
from typing import List, Tuple, Union
from random import randint
from random import sample


def load_common_words() -> List[str]:
    with open('common_words.txt') as common_words:
        # read whole file and then splitlines by \n
        return common_words.read().splitlines()


def generate_brand_names(words: List[str]) -> List[Tuple[Union[str,]]]:
    return [(words[index],) for index in sample(range(100), 100)]


async def insert_brands(common_words, connection) -> int:
    brands = generate_brand_names(common_words)
    insert_brands = "INSERT INTO brand VALUES(DEFAULT, $1)"
    return await connection.executemany(insert_brands, brands)


def gen_products(
    common_words: List[str],
    brand_id_start: int,
    brand_id_end: int,
    products_to_create: int,
) -> List[Tuple[str, int]]:
    products = []
    for _ in range(products_to_create):
        description = [common_words[index] for index in sample(range(1000), 10)]
        brand_id = randint(brand_id_start, brand_id_end)
        products.append((" ".join(description), brand_id))
    return products


def gen_skus(
    product_id_start: int,
    product_id_end: int,
    skus_to_create: int,
) -> List[Tuple[int, int, int]]:
    skus = []
    for _ in range(skus_to_create):
        product_id = randint(product_id_start, product_id_end)
        size_id = randint(1, 3)
        color_id = randint(1, 2)
        skus.append((product_id, size_id, color_id))
    return skus


async def main():
    connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='test-user',
        database='test-db',
        password='qwerty',
    )
    common_words = load_common_words()

    # firstly because of brand_id foreign key
    await insert_brands(common_words, connection)

    # firstly because of brand_id foreign key
    product_tuples = gen_products(
        common_words=common_words,
        brand_id_start=1,
        brand_id_end=100,
        products_to_create=1000,
    )
    await connection.executemany(
        "INSERT INTO product VALUES(DEFAULT, $1, $2)",
        product_tuples,
    )

    sku_tuples = gen_skus(
        product_id_start=1,
        product_id_end=1000,
        skus_to_create=100000,
    )
    await connection.executemany(
        "INSERT INTO sku VALUES(DEFAULT, $1, $2, $3)",
        sku_tuples,
    )

    await connection.close()


if __name__ == '__main__':
    # IF YOU FAILED ON SEQUENCE use it directly in DB
    # TRUNCATE brand RESTART IDENTITY CASCADE;

    asyncio.run(main())
