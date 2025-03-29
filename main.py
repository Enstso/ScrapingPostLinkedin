import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def getHeadersTokenBaserow():
    # give the baserow token
    headers_bdd = {
            'Authorization': 'Token ',
            'Content-Type': 'application/json',
        } 
    return headers_bdd

# func to get the number of post in the baserow db
def getLastPostCount():
    try:
        # token baserow
        headers_bdd = getHeadersTokenBaserow()
        # url de nombre post connu de baserow
        response_bdd = requests.get('baserow_url',headers=headers_bdd)
        response_bdd_json = response_bdd.json()
        # Name of the Baserow field that contains the number of posts.
        lastNbPost = int(response_bdd_json[''])
        return lastNbPost
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except Exception as err:
        print ("Other error:",err)


# func to get the content of linkedin page
def getContentPage():
    try:
        # Profil url linkedin
        url = ""
        # User agent to avoid LinkedIn blocking.
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

# func to insert the number of post in the baserow db.
def insertNewCountPost(lastNbPost):
    try:
        # token baserow
        headers_bdd = getHeadersTokenBaserow()
        # The name of the Baserow field that contains the number of posts.
        data = {'': lastNbPost}
        # URL of the known post number in Baserow.
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
        # Retrieving the <p> tags + class of the posts to identify the posts.
        content_post = soup.find_all('p',class_='attributed-text-segment-list__content text-color-text !text-sm whitespace-pre-wrap break-words')
        # Retrieving the number of posts on the LinkedIn profile.
        currNbPost = len(content_post)
        # If the number of posts is different from the last known number of posts, we insert the new number of posts into the Baserow database
        if currNbPost > lastNbPost:
            insertNewCountPost(currNbPost)
            print("New post")
            lastPost = content_post[0].text
            data = {'post': lastPost}
            # Execution/sending of the latest post to the webhook
            requests.post('',data=data)
        else:
            print("No new post")
main()



