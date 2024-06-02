from test_csv2 import output_api
def answer(ans):
    links, answer = output_api(ans)
    if answer:
        return {
            "answer": answer,
            "url": links
        }
    else:
        return {
            "answer": "Ошибка генерации ответа",
            "url": links
        }