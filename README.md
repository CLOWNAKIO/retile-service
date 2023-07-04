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


АРХИТЕКТУРА СЕРВИСА
-




