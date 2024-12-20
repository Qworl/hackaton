import aiohttp
import asyncio
import asyncpg

URL = 'https://www.banki.ru/services/responses/list/ajax/'


async def connect():
    return await asyncpg.connect(user='postgres', password='postgres', database='feedback', host='postgres_db')


def beauty_text(text: str) -> str:
    return text.replace('<p>', '').replace('</p>', '').replace('</b>', '').replace('</b>', '').replace('[b]', '').replace('[/b]', '').replace('\n', '').replace('\r', '')


async def make_request(page: int):
    params = {
        'page': page,
        'is_countable': 'on',
        'bank': 'promsvyazbank',
    }

    async with aiohttp.ClientSession() as session:
        response = await session.get(URL, params = params)
        result = await response.json()
        return result


async def write_data(values):
    conn = await connect()
    await conn.execute('''
        INSERT INTO feedback (title, text, comment_id, grade)
        (SELECT
            f.title, f.text, f.comment_id, f.grade
        FROM
            unnest($1::feedback_type[]) as f
        )
        ON CONFLICT (comment_id) DO UPDATE SET
            title = excluded.title,
            text = excluded.text,
            grade = excluded.grade
    ''', values)
    await conn.close()


async def parse():
    print('Start parsing job')

    page = 1
    hasMorePages = True
    values = []
    while hasMorePages:
        page_result = await make_request(page)

        hasMorePages = page_result['hasMorePages'] and page_result['data']

        for item in page_result['data']:
            values.append((item['title'], beauty_text(item['text']), int(item['id']), int(item['grade'])))
 
        print(page)
        page += 1
        await write_data(values)




asyncio.run(parse())
