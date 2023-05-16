""" Модуль для работы с API hotels4.p.rapidapi.com """


from config_data.config import RAPID_API_KEY
import requests
import json
from typing import Dict, Optional


def get_city(city_name: str) -> Optional[Dict]:
    """
    Функция GET запроса городов по названию

    Args:
        city_name (str): название города для запроса

    Returns:
        cities (Optional[Dict[str: str]): словарь ключ - название города, значение - id этого города
    """
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
    }
    url = f'https://hotels4.p.rapidapi.com/locations/v3/search/'
    params = {
        "q": city_name,
        "locale": "ru_RU",
        "langid": "1033",
        "siteid": "300000001"
    }
    response = requests.get(url, headers=headers, params=params, timeout=10)
    if response.status_code == requests.codes.ok:
        cities = dict()
        result = json.loads(response.text)
        for i_city in result['sr']:
            if i_city['@type'] == 'gaiaRegionResult':
                cities[i_city['regionNames']['fullName']] = i_city['gaiaId']
        return cities


def get_hotels(city_id: str, hotels_amount: int, sort: str, price: tuple = None) -> Optional[Dict]:
    """
    Функция POST запроса по id города для получения списка отелей

    Args:
        city_id (str): id города
        hotels_amount (int): количество отелей в результате
        sort (str): тип сортировки отелей
        price (tuple): price[0] - цена от, price[1] - цена до

    Returns:
        hotel_id (Optional[Dict[str: Any[str, int]]]): словарь ключ - название отеля, значение - его id
    """
    if price:
        payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "ru_RU",
            "siteId": 300000001,
            "destination": {"regionId": city_id},
            "checkInDate": {
                "day": 14,
                "month": 10,
                "year": 2022
            },
            "checkOutDate": {
                "day": 15,
                "month": 10,
                "year": 2022
            },
            "rooms": [{"adults": 1}],
            "resultsStartingIndex": 0,
            "resultsSize": hotels_amount,
            "sort": sort,
            "filters": {
                "availableFilter": "SHOW_AVAILABLE_ONLY",
                "price": {
                    "max": price[1],
                    "min": price[0],
                        }
            }
        }
    else:
        payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "ru_RU",
            "siteId": 300000001,
            "destination": {"regionId": city_id},
            "checkInDate": {
                "day": 10,
                "month": 10,
                "year": 2022
            },
            "checkOutDate": {
                "day": 15,
                "month": 10,
                "year": 2022
            },
            "rooms": [{"adults": 1}],
            "resultsStartingIndex": 0,
            "resultsSize": hotels_amount,
            "sort": sort,
            "filters": {"availableFilter": "SHOW_AVAILABLE_ONLY"}
        }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    url = 'https://hotels4.p.rapidapi.com/properties/v2/list'
    try:
        response = requests.post(headers=headers, url=url, json=payload, timeout=10)
        if response.status_code == requests.codes.ok:
            hotel_id = dict()
            result = json.loads(response.text)
            if result['data']['propertySearch']['properties']:
                for i_hotel in result['data']['propertySearch']['properties']:
                    hotel_id[i_hotel['name']] = i_hotel['id']
                return hotel_id
    except Exception:
        return None


def get_hotel_info(hotel_id) -> Dict:
    """
    Функция POST запроса по id города для получения списка отелей

    Args:
        hotel_id (str): id отеля
    Returns:
        hotel_info (Dict[str: str]): ключ - параметр отеля, значение - данные параметра
    """
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "propertyId": hotel_id,
    }
    url = 'https://hotels4.p.rapidapi.com/properties/v2/detail'
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    if response.status_code == requests.codes.ok:
        hotel_info = dict()
        result = json.loads(response.text)
        hotel_info['name'] = result['data']['propertyInfo']['summary']['name']
        hotel_info['coordinates'] = {
            'x': result['data']['propertyInfo']['summary']['location']['coordinates']['latitude'],
            'y': result['data']['propertyInfo']['summary']['location']['coordinates']['longitude']
        }
        hotel_info['address'] = result['data']['propertyInfo']['summary']['location']['address']['firstAddressLine']
        hotel_info['tagline'] = result['data']['propertyInfo']['summary']['tagline']
        hotel_info['img_urls'] = list()
        for number, i_image in enumerate(result['data']['propertyInfo']['propertyGallery']['images']):
            if number == 10:
                break
            else:
                hotel_info['img_urls'].append(i_image['image']['url'])
        return hotel_info
