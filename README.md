 <body>
    <h1>Frilance place</h1>
    <h2>Содержание</h2>
    <ul>
      <li><a href="#description">Описание</a></li>
      <li><a href="#installation">Установка</a></li>
      <li><a href="#database">База данных</a></li>
<li><a href="#env">Заполнение .env</a></li>
    </ul>
    <h2 id="description">Описание</h2>
    <h3>Данное веб-приложение - Фриланс площадка

"Customer" может создавать заказы, которые надо выполнить

"Executor" может принимать и выполнять заказы от "Customer"-ов</h3>

<h2 id="installation">Установка</h2>
    <p>Для удобного запуска используется <pre>docker compose </pre> Чтобы использовать файлы из этого репозитория, просто склонируйте репозиторий на свой локальный компьютер:</p>
    <pre><code>git clone https://github.com/Peskovatskow-Ignat/Frilance_place.git </code> </pre>
    <p>Далее зайдите в директорию проекта и запустите контейнеры командой:</p>
    <pre><code>docker compose up --build</code></pre>
    <p>После этого перейдите по адресу:</p>
    <pre><code>127.0.0.1:${FLASK_PORT}/ </code> </pre>

<h2 id="database">База данных</h3>

<h3>Таблица "customer":
    Предназначена для хранения информации о клиентах.</h3>
    <h3>Поля:</h3>

- id (Целое число) - уникальный идентификатор клиента (генерируется автоматически).
- username (Строка до 50 символов) - имя пользователя.
- first_name (Строка до 50 символов) - имя клиента.
- last_name (Строка до 50 символов) - фамилия клиента.
- email (Строка до 100 символов, обязательное поле) - адрес электронной почты клиента.
- password (Строка до 100 символов, обязательное поле) - пароль клиента.
- data (Метка времени) - дата создания записи (по умолчанию - текущая метка времени).
- rating (Целое число) - рейтинг клиента (от 0 до 5, значение по умолчанию - 0).
- photo (Двоичные данные) - фотография клиента.

<h3>Таблица "orders":</h3>
    Предназначена для хранения информации о заказах.
    <h3>Поля:</h3>

- id (Целое число) - уникальный идентификатор заказа (генерируется автоматически).
- title (Строка до 100 символов) - название заказа.
- price (Целое число) - цена заказа.
- description (Текстовое поле) - краткое описание заказа.
- full_description (Текстовое поле) - полное описание заказа.
- date (Метка времени) - дата создания заказа (по умолчанию - текущая метка времени).
- customer_id (Целое число) - ссылка на клиента, создавшего заказ.
- skill (Строка до 100 символов) - навык, связанный с заказом.
- status (Логическое значение) - статус заказа (по умолчанию - true).

<h3>Таблица "executor" Предназначена для хранения информации об исполнителях.</h3>
<h3>Поля:</h3>

- id (Целое число) - уникальный идентификатор исполнителя (генерируется автоматически).
- email (Строка до 100 символов, обязательное поле) - адрес электронной почты исполнителя.
- username (Текстовое поле) - имя пользователя исполнителя. 
- first_name (Строка до 50 символов) - имя исполнителя.
- last_name (Строка до 50 символов) - фамилия исполнителя.
- specialty (Строка до 100 символов) - специализация исполнителя.
- data (Метка времени) - дата создания записи (по умолчанию - текущая метка времени).
- password (Строка до 100 символов) - пароль исполнителя.
- rating (Целое число) - рейтинг исполнителя (от 0 до 5, значение по умолчанию - 0).
- photo (Двоичные данные) - фотография исполнителя.

<h3>Таблица "executor_to_order":
    Предназначена для установления связей между исполнителями и заказами.</h3>
    <h3> Поля:</h3>

- executor_id (Целое число, обязательное поле) - ссылка на исполнителя.
- order_id (Целое число, обязательное поле) - ссылка на заказ.
- status (Логическое значение, по умолчанию - true) - статус связи.
- flag (Логическое значение, по умолчанию - false) - флаг.
- data (Метка времени) - дата создания записи (по умолчанию - текущая метка времени).


<h3 id="env">Заполнение .env</h3>
Для полноценной работы надо заполнить файл .env следующим образом

    SECRET_KEY - ваш_секретный_ключ
    
    MAIL_USERNAME - Адрес вашей почты
    MAIL_PASSWORD - Пароль вашей почты для приложений
    MAIL_DEFAULT_SENDER - Адрес вашей почты
    

    POSTGRES_PORT - Порт Postgres внутри docker compose
    POSTGRES_DB - Название БД
    POSTGRES_USER - Пользователь БД
    POSTGRES_PASSWORD - Пароль пользователя БД
    
    FLASK_PORT - Порт на котором будет работать Flask 


