# ApiRequester
 
Тестовый проект к 24 модулю SkillFactory курса QAP

В директории /tests располагается файл с тестами

В корневой директории лежит файл settings.py - содержит информацию о валидном логине и пароле

В корневой директории лежит файл api.py, который является библиотекой к REST api сервису веб приложения Pet Friends

Библиотека api написана в классе, что соответствует принципам ООП и позволяет удобно пользоваться её методами. При инициализации библиотеки объявляется переменная base_url которая используется при формировании url для запроса.

Методы имеют подробное описание.

Тесты проверяют работу методов используя api библиотеку.

Был выявлен баг в методе добавления нового питомца с некорретном возрастом.