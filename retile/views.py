import os
import json
from io import BytesIO
import requests
import mercantile
from django.http import HttpResponse
from rest_framework.views import APIView
from PIL import Image
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException


class WrongParametres(APIException):
    status_code = 422
    default_detail = 'Введены неверные параметры запроса'
    default_code = 'wrong_paraments'


class InternalError(APIException):
    status_code = 500
    default_detail = 'Произошла внутреняя ошибка'
    default_code = 'internal_error'


@api_view(['GET'])
def handler422(request, **kwargs):
    raise WrongParametres


def retile(x: int, y: int, zoom: int, src_zoom: int, url: str) -> Image.Image:
    if zoom == src_zoom:
        try:
            provider_img_url = url.format(z=src_zoom, x=x, y=y)
            response = requests.get(provider_img_url, stream=True)
            img = Image.open(BytesIO(response.content))

        except:
            raise InternalError

    else:
        tile = mercantile.Tile(x, y, zoom)
        if zoom < src_zoom:
            corners = [(0, 0), (512, 0), (512, 512), (0, 512)]
            img = Image.new('RGB', (1024, 1024))
            image_children_tiles = mercantile.children(*tile)
            for i in range(4):
                img.paste(retile(*image_children_tiles[i], src_zoom, url), corners[i])

        else:
            corners = [(0, 0), (256, 0), (256, 256), (0, 256)]
            image_parent_tiles = mercantile.parent(x, y, zoom)
            neighbour_tiles = mercantile.children(*image_parent_tiles)
            corner_id = neighbour_tiles.index(tile)
            corner = (
                corners[corner_id][0], corners[corner_id][1], corners[corner_id][0] + 256, corners[corner_id][1] + 256)
            img = retile(*image_parent_tiles, src_zoom, url).crop(corner)

    return img.resize((512, 512), resample=Image.LANCZOS)


class IndexAPI(APIView):
    def get(self, request, *args, **kwargs):
        try:
            provider, level, resolution, z, x, y = kwargs.values()

            if z >= 0 and z + level >= 0:
                min_coord, max_coord = mercantile.minmax(z)
                if not (min_coord <= x <= max_coord and min_coord <= y <= max_coord):
                    raise WrongParametres
            else:
                raise WrongParametres

            try:
                provider_file_path = str(settings.BASE_DIR) + '/providers.json'
                with open(provider_file_path, 'r') as provider_file:
                    provider_file_content = provider_file.read()
                    providers = json.loads(provider_file_content)
                    url = providers[provider]
            except:
                raise WrongParametres

            result_filename = 'result.png'
            img_path = settings.MEDIA_ROOT + result_filename
            img = retile(x, y, z, z + level, url)
            img = img.resize((resolution, resolution), resample=Image.LANCZOS)
            response = HttpResponse(content_type='image/png', status=200)
            img.save(response, "PNG")
            return response 

        except WrongParametres:
            raise WrongParametres

        except:
            raise InternalError
