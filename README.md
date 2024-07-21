# public_utilities
### ETL данных квитанций за коммунальные услуги.
В репозитории находятся три скрипта, которые с помощью библиотеки `camelot` парсят данные квитанций из PDF и загружают в таблицу.

`public_utilities_local.ipynb` работает с pdf файлами из папки на локальном диске и выгружает данные в csv файл.
- `./bills/` содержит pdf,
- `checked_files.txt` содержит имена обработанных pdf,
- `bills.csv` - выходной файл.

`public_utilities_google.ipynb` работает с письмами из Gmail по API, достаёт из них pdf, парсит и выгружает данные в Google таблицу.
- `TOKEN_GMAIL` - токен для работы с API Gmail,
- `TOKEN_GSPREAD` - токен для работы с API Google Spreadsheets,
- `WBOOK`, `WSHEET` - имена таблицы и листа в ней на Google Drive,
- `./tmp/last.pdf` - последний обработанный файл,
- `from:your_email@gmail.com AND subject:Квитанция AND filename:pdf AND is:unread` - запрос на поиск писем.

`docker_run/main.py` работает с письмами из mail.ru по IMAP, достаёт из них pdf, парсит и выгружает данные в Google таблицу.
Содержимое `.env`:
- `GSPREAD_TOKEN` - токен для работы с API Google Spreadsheets,
- `GSPREAD_WBOOK` - имя таблицы на Google Drive,
- `GSPREAD_WSHEET` - имя листа в таблице на Google Drive,
- `MAIL_SERVER` - IMAP сервер,
- `MAIL_USERNAME` - адрес e-mail,
- `MAIL_PASS` - пароль для внешних приложений (в mail.ru задаётся в разделе Безопасность - Способы входа)

Из Google таблицы данные забирает Tableau для расчётов и визуализаций.
