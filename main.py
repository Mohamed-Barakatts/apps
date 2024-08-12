from flet import *
import random
import string
import requests
import base64
import json

url = 'http://v2.expanel.co/prnew.php'

def generate_random_hex(length):
    hex_digits = string.hexdigits[:-6]  # Exclude lowercase letters
    return ''.join(random.choice(hex_digits) for _ in range(length))

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-us',
    'Accept-Encoding': '*',
    'User-Agent': '',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'v2.expanel.co',
    'Cache-Control': 'no-cache',
    'Connection': 'Keep-alive'
}
random_hex = generate_random_hex(12)

def on_button_click(e):
    user_input = code_field.value
    mac_input = mac_field.value

    # Sample data
    user_input = '611292279503'
    mac_input = '0012FBB93EA8'

    json_data = {
        'mode': 'active',
        'code': f'{user_input}',
        'mac': f'{mac_input.upper()}',
        'sn': f'{mac_input.upper()}'
    }
    data = json.dumps(json_data)

    myXorKey = 'AzXMc-3TF#8*D3yG'
    myKeyLength = len(myXorKey)
    encrypted_request = ''
    for i in range(len(data)):
        encrypted_request += chr(ord(data[i]) ^ ord(myXorKey[i % myKeyLength]))

    encoded_bytes = base64.b64encode(encrypted_request.encode('utf-8'))
    payload = {'json': encoded_bytes.decode('utf-8')}

    encoded_payload = '&'.join([f'{key}={value}' for key, value in payload.items()])
    headers['Content-Length'] = str(len(encoded_payload))

    response = requests.post(url, data=payload, headers=headers)
    response_t = response.text

    encrypted_response = ''
    for i in range(len(response_t)):
        encrypted_response += chr(ord(response_t[i]) ^ ord(myXorKey[i % myKeyLength]))

    result_text.value = encrypted_response
    page.update()

def main(page: Page):
    page.title = 'Express V4 Crack'
    page.window_width = 350
    page.window_height = 600

    global code_field, mac_field, result_text

    title = Text('Express V4 API Crack V1 \n\n Enter your Code Here')
    code_field = TextField(label='Code', autofocus=True)
    mac_label = Text('Enter your MAC Here')
    mac_field = TextField(label='MAC')
    button = ElevatedButton('Get Code Info', on_click=on_button_click)
    result_text = Text()

    footer = Text('Created by Mohamed & Mr. Amr')

    page.add(title, code_field, mac_label, mac_field, button, result_text, footer)

app(target=main)
