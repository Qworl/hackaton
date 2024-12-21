import json

from gigachat import GigaChat
import asyncpg
import asyncio
from gigachat.models import Chat, Messages, MessagesRole


async def main():
    conn: asyncpg.Connection = await asyncpg.connect(user='postgres', password='postgres', database='feedback',
                                                     host='postgres_db')
    table_name = "feedback"
    credentials = "MWExZTU2NjQtZmQzYi00NDcwLTgzMzUtNjUyZGNjYzVkOGUwOmMwODQ4NDhlLTg1ZDEtNDA0NC05YjI5LWU4ZTllNTQzMzc5MA=="

    messages = [Messages(role=MessagesRole.SYSTEM,
                         content="Ты - ассистент сотрудника банка и тебе необходимо произвести классификацию по следующим параметрам"
                                 " category 1: претензия(1), благодарность(2) или предложение(3)."
                                 "is_finance 2. Относится ли обращение к финансовому(1) или нет(0)"
                                 "sub_category 3. связано "
                                 "ли обращение с ошибкой "
                                 "не применимо(0), сотрудника(1), несогласием с тарифами(2), технический сбой или скоростью обслуживания. (3)"
                                 "Объедини результаты в json следующего формата: {"
                                 "category:number - Характер обращения,"
                                 "sub_category:number - Дополнительный характер обращения,"
                                 "is_finance:number - Финансовый вопрос или нет"
                                 "}."
                                 "Ответ выдай только в формате json. Пояснения к ответу давать не надо",

                         )]

    values: list[asyncpg.Record] = await conn.fetch(f"SELECT * from {table_name}")

    async with GigaChat(credentials=credentials, verify_ssl_certs=False) as model:
        for value in values:
            resp = await model.achat(Chat(messages=messages + [
                Messages(role=MessagesRole.USER, content=value.get("title") + " " + value.get("text"))]))
            resp_json = json.loads(resp.choices[0].message.content)
            await conn.execute(
                f'UPDATE {table_name} SET is_new = False, is_qualified = True, feedback_type = {resp_json["category"]},'
                f'is_finance = {resp_json["is_finance"]}, subcategory_type = {resp_json["sub_category"]} '
                f'WHERE id = {value.get("id")}')


if __name__ == '__main__':
    asyncio.run(main())
