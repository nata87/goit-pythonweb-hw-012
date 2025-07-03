# Фінальний проєкт GoIT

Це завершальне домашнє завдання курсу **FullStack Web Development with Python** від GoIT. Застосунок — це REST API для керування контактами користувача з додатковими можливостями: автентифікація, кешування, система ролей, зміна пароля, Cloudinary, документація та Docker.

---

##  Основна функціональність

###  Аутентифікація та Авторизація

* JWT (access токен)
* Валідація email
* Скидання пароля через email

###  Користувацькі ролі

* `user` та `admin`
* Лише `admin` може змінювати аватар

###  Cloudinary

* Завантаження та збереження аватарів у хмарі

###  Redis

* Кешування користувача при автентифікації

###  Тестування

* `pytest`, `pytest-cov`
* > 75% покриття (файл coverage.png)
* Модульні та інтеграційні тести

###  Документація

* `Sphinx`
* Докстрінги для всіх публічних функцій

---

##  Запуск через Docker

1. Створіть `.env` файл зі змінними:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=contacts_db
DATABASE_URL=postgresql+asyncpg://postgres:postgres@contacts-postgres:5432/contacts_db
REDIS_HOST=contacts-redis
REDIS_PORT=6379
MAIL_USERNAME=your@mail.com
MAIL_PASSWORD=yourpassword
CLOUDINARY_NAME=your_cloudinary_name
CLOUDINARY_API_KEY=your_key
CLOUDINARY_API_SECRET=your_secret
```

2. Запустіть:

```bash
docker-compose up --build
```

3. Перевірте:

* Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)
* Health Check: [http://localhost:8000/health](http://localhost:8000/health)

---

##  Команди тестування

```bash
pytest --cov=src tests/
```
---

![Coverage Report](./coverage.png)



