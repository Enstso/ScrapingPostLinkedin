import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def getHeadersTokenBaserow():
    #spécifier le token baserow
    headers_bdd = {
            'Authorization': 'Token ',
            'Content-Type': 'application/json',
        } 
    return headers_bdd

#fonction qui récupère le nombre de post dans la base baserow
def getLastPostCount():
    try:
        #token baserow
        headers_bdd = getHeadersTokenBaserow()
        #url de nombre post connu de baserow'
        response_bdd = requests.get('',headers=headers_bdd)
        response_bdd_json = response_bdd.json()
        #nom du champs baserow qui contient le nombre de post
        lastNbPost = int(response_bdd_json[''])
        return lastNbPost
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except Exception as err:
        print ("Other error:",err)


#fonction qui récupère le contenu de la page linkedin
def getContentPage():
    try:
        #url du profil linkedin
        url = ""
        #user agent pour éviter le blocage de linkedin
        user_agent = UserAgent()
        headers_linkedin = {
        'user-agent': user_agent.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
        }
        page = requests.get(url,headers=headers_linkedin)
        return page
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except Exception as err:
        print ("Other error:",err)

#fonction qui insère le nombre de post dans la base baserow
def insertNewCountPost(lastNbPost):
    try:
        #token baserow
        headers_bdd = getHeadersTokenBaserow()
        #nom du champs baserow qui contient le nombre de post
        data = {'': lastNbPost}
        #url de nombre post connu de baserow
        requests.patch('', headers=headers_bdd, json=data)
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except Exception as err:
        print ("Other error:",err)

def main():

    page = getContentPage()
    print(page)
    lastNbPost = getLastPostCount()

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        #récupération des balises <p> + classe des posts pour identifier les posts
        content_post = soup.find_all('p',class_='attributed-text-segment-list__content text-color-text !text-sm whitespace-pre-wrap break-words')
        #récupération du nombre de post sur le profile linkedin
        currNbPost = len(content_post)
        #si le nombre de post est différent du dernier nombre de post connu, on insère le nouveau nombre de post dans la base baserow
        if currNbPost > lastNbPost:
            insertNewCountPost(currNbPost)
            print("New post")
            lastPost = content_post[0].text
            data = {'post': lastPost}
            #éxécution/envoi du dernier post sur le webhook
            requests.post('',data=data)
        else:
            print("No new post")



main()



