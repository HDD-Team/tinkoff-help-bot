# QnA-Bot Тинькофф
# Установка:
- Для установки зависимостей:
`pip install fastapi pydantic typing langchain_community langchain beautifulsoup4 faiss-cpu sentence-transformers langchain_core lxml dotenv`

- Для работы кода необходим `api.env`:
```
OPENAI_API_KEY = <API-ключ сервиса OpenAI>
# При необходимости прокси сервера:
PROXY_LOGIN = <Логин сервера>
PROXY_PASS = <Пароль сервера>
```

Использовались модели:
- **rubert-tiny2**
- **gpt-3.5-turbo**
- **Mistral**

# Использование:
## Отправить POST запрос (при запуске у себя)
```
curl -X POST -H "Content-Type: application/json" -d '{"query": "<Ваш вопрос>"}' http://0.0.0.0:8000/assist -k
```
## Отправить POST запрос (Если на наш сервер)
```
curl -X POST -H "Content-Type: application/json" -d '{"query": "<Ваш вопрос>"}' http://46.147.127.169:8000/assist -k
```
