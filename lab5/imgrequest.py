import requests
import re

def build_links_for_name(name):
    url = 'https://www.google.com/search?q=' + name + '&client=firefox-b-ab&tbm=isch&tbo=u&source=univ&sa=X&ved=2ahUKEwjN5fWwxu3eAhUQmIsKHeA-D90QsAR6BAgEEAE'
    headers = {'User-Agent': 'Nokia5250/10.0.011 (SymbianOS/9.4; U; Series60/5.0 Mozilla/5.0; Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/525 (KHTML, like Gecko) Safari/525 3gpp-gba'}
    response = requests.get(url, headers=headers)
    text_file = open("output.html", "w")
    text_file.write(response.text)
    text_file.close()
    ans = []
    results = re.findall(r'<img src="h.*?>', response.text)
    for result in results:
        urlg = re.search(r'"(.+?)"', result)
        if urlg:
            url = urlg.group(1)
            ans.append(url)
    return ans

if __name__ == '__main__':
    print(build_links_for_name("John Smith"))