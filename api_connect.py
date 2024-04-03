import requests
from config import URLS, Endpoint, HEADRS_L


def request_asic_info(host: str, headers : dict = ''):
    responce = requests.get(url=host, headers=headers)
    return responce


def parse_info(ip_list: list, min_hash: int, return_list = False):
    info_list = []

    for i in range(0, min(len(URLS), len(HEADRS_L))):
        info = request_asic_info(URLS[i] + Endpoint().STATS, HEADRS_L[i])
        if 'Socket connect failed' in info.text:
            info = {'error': 'Socket connect failed'}
        else:
            info = info.json()
        
        info['ip'] = URLS[i]
        info_list.append(info)

    if return_list:
        return info_list
    text = ''
    try:
        for info in info_list:
            ip = info['ip']
            if 'error' in info:
                text += f'\n [{ip}] Статус получения данных неуспешный\n'
                text += f"{info['error']}\n\n"
            elif info['STATUS']['STATUS'] != 'S':
                text += f"\n [{ip}] Вернул код ошибки асика {info['STATUS']['STATUS']}\n"
            elif info['STATUS']['STATUS'] == 'S':
                asic_type = info['INFO']['type']
                hash5s = info['STATS'][0]['rate_5s']
                is_valid = ''
                if int(hash5s) < min_hash:
                    is_valid = '🔴'
                else:
                    is_valid = '🟢'
                hashAv = f"{info['STATS'][0]['rate_avg']} {info['STATS'][0]['rate_unit']}"
                frequency = str( (
                    info['STATS'][0]['chain'][0]['freq_avg'] +
                    info['STATS'][0]['chain'][1]['freq_avg'] +
                    info['STATS'][0]['chain'][2]['freq_avg'] ) / 3)
                temps1 = f"{info['STATS'][0]['chain'][0]['temp_chip'][0]} град - {info['STATS'][0]['chain'][0]['temp_chip'][3]} град "
                temps2 = f"{info['STATS'][0]['chain'][1]['temp_chip'][0]} град - {info['STATS'][0]['chain'][1]['temp_chip'][3]} град "
                temps3 = f"{info['STATS'][0]['chain'][2]['temp_chip'][0]} град - {info['STATS'][0]['chain'][2]['temp_chip'][3]} град "
                fans = f"{info['STATS'][0]['fan'][0]} - {info['STATS'][0]['fan'][1]} - {info['STATS'][0]['fan'][2]} - {info['STATS'][0]['fan'][3]}"

                text += f'''
[{ip}]
Rig: {asic_type}
  Хэш 5 сек: {is_valid} {hash5s} MH/s
  Хэш средний: {hashAv}
  Частота: {frequency}
  Температура:
      {temps1}
      {temps2}
      {temps3}
  Обороты куллеров:
      {fans} об/мин
                    
                          '''
            else:
                text += f'\n [{ip}] Статус получения данных успешный, но код статуса асика неизвестен\n'
    except Exception as e:
        print(e)
        text += '\nОшибка получения данных\n'
        text += str(e)
    finally:
        return text
    
