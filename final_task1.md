# Второй уровень. В бой!

## Преамбула

Ты открываешь глаза и снова обнаруживаешь себя сидящим на жестком деревянном стуле. Но теперь всё иначе: комната больше не погружена во тьму — она залита ярким, почти ослепительным светом. Вместо стен стеклянные перегородки, за которыми видны такие же помещения со столами, компьютерами и древними ЭЛТ-мониторами. Внутри них — другие люди. Они тоже осматриваются с недоумением и тревогой, также ничего не понимая. Прямо перед тобой возвышается огромный каменный Сфинкс, еще более древний, чем твой монитор. А под ним — электронные часы, замершие на отметке «08:00».

Ты оглядываешься. За стеклами — чужие лица, такие же потерянные, как твое. Как ты здесь оказался? Кто поместил тебя в этот странный стеклянный аквариум? И что вообще было до этого момента? Слишком много вопросов — и ни одного ответа. Ты уже собираешься подняться, чтобы попытаться установить контакт с одним из соседей, как вдруг экран твоего компьютера вспыхивает, и воздух прорезает резкий, скрежещущий голос:

— Время пришло, мои дорогие участники!

Ты вскидываешь голову — и замираешь. Говорит не кто иной, как тот самый гигантский Сфинкс. Его каменные губы медленно двигаются, издавая звук перетирающихся камней.

— У вас есть восемь часов и ваши знания, чтобы заполучить то, что вы так отчаянно ищете! — продолжает Сфинкс. — Вы все прошли необходимые испытания и доказали свою готовность к бою! — Он делает паузу. — Так пусть же начнётся финал!

## Задача

— На своих устройствах вы найдёте программу. Внутри неё заблудшие путники. Ваша задача — создать алгоритм, который проведёт этих путников сквозь препятствия как можно дальше. Ваш алгоритм должен быть универсальным, ведь дорог — бесчисленное множество, как и самих препятствий. Победит тот, чей путник пройдёт дальше всех... если не до самого конца! — взревел Сфинкс. — Все дальнейшие инструкции вы найдёте на своих устройствах. И да пребудет с вами мудрость!

Сразу после этих слов электронные часы под Сфинксом издали пронзительный писк и изменились на «09:59». Время пошло — значит, пора начинать разбираться.

Обрати внимание на папку materials. В ней ты найдешь описание симуляционной программы. Саму симуляционную программу ты можешь увидеть на своем рабочем столе под названием Final2025.

## Условия

Для создания алгоритма воспользуйся написанным на Первом уровне веб-сервером. Там же можешь найти описание необходимого API и условий по запуску в Docker-контейнере и на 8080 порту. Обрати внимание, что API должен получиться синхронным, а написанный веб-сервер — Stateful. Если ты пропустил Первый уровень, то можешь найти его в папке materials.

Помни, что проект и Dockerfile должны быть размещены в папке src. Также учти, что при проверках сборка контейнера будет производиться из директории src без каких-либо дополнительных аргументов.

Залей написанный на Первом уровне веб-сервер с готовыми заглушками эндпоинтов в репозиторий в ветку first_level. А итоговое решение Второго уровня должно быть залито в репозиторий в ветку develop.

Сама по себе симуляция представляет из себя многоуровневый лабиринт. Для перехода на следующий уровень необходимо взаимодействие со Сфинксом и выполнение его испытаний. Где-то испытания попроще, где-то посложнее. Как именно их выполнять — р ешение целиком на тебе. За некорректное выполнение испытаний полагается наказание.

Анализируй данные, которые присылает симуляция на твой сервер, пробуй проводить путника до цели руками и экспериментируй. В общем, делай всё, чтобы разработать необходимый алгоритм за отведенное время. Потому что в конце дня путник останется совсем один в совершенно новом окружении, и ему придется выбираться из него исключительно при помощи твоего алгоритма.

## Критерии

Максимальное время ответа на запрос от симуляции не должно превышать 20 секунд. Время — понятие относительное, поэтому для определенности считай эталонной мерой производительности ограничения твоей рабочей станции.

На Первом уровне будет проверяться следование требованиям стадии необходимой подготовки и описанной в задании спецификации API.

Формальные критерии Второго уровня: проверяется штатная работа веб-сервиса с возможностью прохождения уровней симуляции.

Техническая эффективность Второго уровня: замеряется средняя нагрузка на CPU, среднее потребление оперативной памяти и время выполнения.

Функциональные критерии Второго уровня: оценивается количество успешно пройденных уровней симуляции. Контрольный набор содержит аналогичные уровни по типам испытаний от Сфинкса, но с отличающимся наполнением этих испытаний.

## Ограничения

Можно использовать любые алгоритмы, методы, методики, приемы и подходы.

Можно использовать любые библиотеки, фреймворки, готовые офлайн-модели. Главное, чтобы итоговый Docker-образ весил не более 4 ГБ, все пакеты были доступны на территории РФ, а выполнение шло на CPU.

Можно использовать внешние сервисы, доступные на территории РФ, но учитывай ограничения на время запроса.

Можно использовать облачную языковую модель, тебе предоставлен доступ к GigaChat API. Если твое решение использует GigaChat API, то ключ авторизации должен задаваться через переменную окружения GIGA_AUTH. Учти это при чтении конфигурации в своем решении и написании обновленного Dockerfile.