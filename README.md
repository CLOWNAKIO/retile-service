ДОКУМЕНТАЦИЯ
- - -

ПОРЯДОК РАЗВЕРТЫВАНИЯ СЕРВИСА
-

cd some_dir

git clone https://github.com/CLOWNAKIO/retile-service

cd retile-service

docker-compose up --build


КОНФИГУРАЦИИ СЕРВИСА
(ФАЙЛ PROVIDERS.JSON)
-

Данные поставщиков представлены в формате JSON.

Пример файла конфигурации:

{
  "provider1": "url1",
  "provider2": "url2"
}

provider - строка имени поставщика, используемая в API запросе;

url - строка адреса сервиса. Обязательно использовать {z}, {x}, {y}, например: http://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}

Изначально установлено 2 поставщика: google и mapbox

АРХИТЕКТУРА СЕРВИСА
-
Сервис представлен в рамках API, написанного с использованием Django и Django REST Framework

Сервис предоставляет возможность ретайлирования на основе верхних и нижних уровней тайлов.

Работа с сервисом осуществляется посредством HTTTP запросов по следующему адресу:
GET /retile/{provider}/{level}/{resolution}/{z}/{x}/{y}.png/

Параметры запроса имеют следующий формат:

- provider: string (Должен быть указан в файле конфигурации providers.json)
- level: integer (-inf < value < inf)
- resolution, z, x, y: integer (value >= 0), при этом x, y в диапозоне (0, 2<sup>z</sup>-1)

  Например: GET /retile/google/2/512/0/0/0.png/

  При не совпадении с форматом данных возвращается HTTP ответ со статусом 422.

  При возникновении ошибок при выполнении запроса возвращается HTTP ответ со статусом 500.

  При удачном запросе возвращается HTTP ответ со статусом 200 и изображение в формате png.





