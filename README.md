# Корпус криптидных текстов и пр. необычных явлений
Крипти́ды (греч. κρύπτω — скрытый) — животные или растения, существование которых считается возможным сторонниками псевдонаук криптозоологии и криптоботаники, но не признано академической наукой.

http://karimova-home.axes.io/

## Суть проекта 
Не так давно мы с командой молодых литераторов объединились в кружок прекарных криптидов, чтобы исследовать тексты современной (и не очень) литературы через криптидную оптику. Также в наши интересы входило исследование различных необычных явлений, например, задокументированных SCP или нашими активистами. Но так как текстов необозримое количество, мной было решено облегчить коллегам поиск паттернов поведения около-криптидных литературных деятелей (нпр. Драгомощенко), а также внести в базу данные SCP Foundation для поиска возможных корреляций. 

## Заглянем под капот
Из специальных инструментов были использованы: natasha, dawg_python, pymorphy2, fastapi. Веб-приложение поднято на сервере хостера digitalocean.com

Навигация по репозиторию:
- /app.py - веб-сервис
- /fastapi_app/helpers.py - парсинг текстов и поиск
- /templates/ - шаблоны страниц

## Возможности поиска
- слово/словом/словами - найти все предложения, где слово встречается в любой форме
- “cлово” - нужно найти предложения только с этой формой
- слово+NOUN - нужно найти все предложения, где встречается существительное “слово” 
- NOUN - найти все предложения с существительными

## Особенности и недочеты

- базы данных нет, все сразу парсится через приложение. Тексты загружаются в директорию texts, потом перезапуск. 
- ввиду специфики исследования тексты отбирались вручную, собственно вручную же и собирались. 
- в качестве источника указывается .txt файл

## Что можно исправить? 

- подключение базы данных SQL на отдельном хосте при наращивании объема корпуса
- автоматическая выгрузка данных с Wiki SCP Foundation и архива "Митиного Журнала" (один из самых криптидных журналов, Дмитрий Волчек великий)
- возможность построения графиков и отчетов для среднестатистического юзера
- перенаправление на источник текста, а не просто вывод названия файла, откуда взят текст
- криптидный дизайн с гифками лохнесского монстра

## Sources
- https://scp-wiki.wikidot.com/
- http://kolonna.mitin.com/?page=archive

## Команда
- Каримова В. А. - сбор текстов, POS-tagging, функции поиска
- Каримова Виктория - бэкенд, деплой
- Вика Каримова - отсутствие дизайна 
- Кот Марвин - психологическая поддежка
- Нурофен, Пенталгин, Red Bull - сделали возможным этот Read Me
