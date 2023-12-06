# public_utilities
### ETL данных квитанций за коммунальные услуги.
В репозитории находятся два скрипта, которые с помощью библиотеки `camelot` парсят данные квитанций из PDF и загружают в таблицу.

`public_utilities_local.ipynb` работает с pdf файлами из папки на локальном диске и выгружает данные в csv файл.
- `./bills/` содержит pdf,
- `checked_files.txt` содержит имена обработанных pdf,
- `bills.csv` - выходной файл.

`public_utilities_google.ipynb` работает с письмами из Gmail, достаёт из них pdf, парсит и выгружает данные в Google таблицу.
- `TOKEN_GMAIL` - токен для работы с API Gmail,
- `TOKEN_GSPREAD` - токен для работы с API Google Spreadsheets,
- `WBOOK`, `WSHEET` - имена таблицы и листа в ней на Google Drive,
- `./tmp/last.pdf` - последний обработанный файл,
- `from:your_email@gmail.com AND subject:Квитанция AND filename:pdf AND is:unread` - запрос на поиск письма.
