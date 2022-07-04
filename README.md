Телеграм бот для работы с кредитами. В папке mysql находятся 2 sql скрипта для создания таблиц необходимой конфигурации. Бот в телеграме - @DeeplayTestBot.

Управление происходит в меню с 2 уровнями иерархии.

Первый уровень - выбор темы. Работа с кредитами или обращение в службу поддержки.

Второй уровень - варианты работы с кредитами. Доступны следующие функции: добавление нового кредита (при наличии кредита у пользователя в заданном банке будет обновлена сумма кредита на заданную), расчёт кредитного пакета в процентах для каждого банка, возврат в главное меню.

На всех этапах работы, кроме выбора темы тикета в службу поддержки, предусмотрена кнопка отмены действия, чтобы вернуться в главное меню при необходимости.

Временно необходимо вводить текст на английском, так как при вводе русского текста получаются непонятные символы в json-файлах тикетов и названий банков для добавления кредитов. Также для тикетов в службу поддержки доступна загрузка только одного изображения.

В качестве бахы данных используется MySQL. БД содержит 2 таблицы:

   1) Таблица users. Содержит 2 поля: id - id записи в таблице, primary key, auto inkrement; userid - идентификатор пользователяв телеграм.
   
   2) Таблица credits. Содержит 4 поля: id - id записи в таблице, primary key, auto inkrement; userid - идентификатор пользователяв телеграм; size - сумма кредита;
                                        bank - название банка, в котором оформлен кредит.
                                        
Параметры базы данных: host - localhost, port - 3306, user - badchaos, password - pe0038900, database - deeplay.

Все необходимые для настройки данные находятся в .env файле
