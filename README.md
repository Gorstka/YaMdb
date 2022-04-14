YaMDb
=====
*YaMDb - учебный проект, разработанный командой студентов Яндекс.Практикум.</br>
Это бэкенд и REST API сервис  для обработки запросов по оценке различных произведений*
------------------------------------
### Описание проекта
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). </br>
Произведения делятся на категории: «Книги», «Фильмы», «Музыка». </br> 
(По желанию категории могут быть расширены) </br>
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку. </br>
Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).</br>
Новые жанры может создавать только администратор. </br>
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (Review)</br>
и ставят произведению оценку в диапазоне от одного до десяти (целое число);</br>
из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число).</br>
На одно произведение пользователь может оставить только один отзыв.

### Инструкция по установке
1.Склонируйте репозиторий в необходимую Вам директорию:
```
  git clone https://github.com/timelord78/api_yamdb.git YaMDb
```
2.В предустановленном виртуальном окружении в директории проекта установите зависимости:
```
pip install -r requirements.txt
```
3. В директории /api_yamdb выполните команды для запуска сервера разработки Django
```
python manage.py migrate
python manage.py runserver
```
4. Вам станет доступна документация Redoc по следующему адресу
```
http://127.0.0.1:8000/redoc/
```
5. При необходимости протестировать проект запросами при помощи Postman либо др. сервисов.

### _Автор_

Горстка Сергей, github.com/Gorstka, gorstkasergei@gmail.com 
Яков Зубец
Алексей Поляков
