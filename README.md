# LinkedIn Scraping Project with Docker

This project uses Docker to run a Python script that scrapes LinkedIn pages to gather information about the number of posts on a profile. The project interacts with a Baserow database to update the number of posts and perform actions (such as sending a webhook) when new posts are found.

## Prerequisites

1. **Docker**: Ensure that Docker is installed on your machine. You can download Docker from [here](https://www.docker.com/get-started).
2. **Python**: This project uses Python 3 along with specific libraries like `requests`, `beautifulsoup4`, and `fake_useragent`.

## Installation

1. Clone the repository (or download the files) to a local directory.
   
2. Build the Docker image with the following command:
    ```bash
    docker build -t image-scrapping .
    ```

3. Run the Docker container with the following command:
    ```bash
    docker run --rm -it -v $(pwd):/scrapping image-scrapping
    ```

## Code Explanation

The project uses several Python libraries to perform the following tasks:

### 1. **Connecting to Baserow**

The script connects to a Baserow database via a REST API. An authentication token is used to interact with the database.

**Function `getHeadersTokenBaserow`**:
This function returns the necessary headers, including the token to authenticate requests to the Baserow API.

```python
def getHeadersTokenBaserow():
    headers_bdd = {
        'Authorization': 'Token ',
        'Content-Type': 'application/json',
    }
    return headers_bdd
```

### 2. **Getting the Number of Posts**

The function `getLastPostCount` queries the Baserow API to retrieve the last known number of posts.

```python
def getLastPostCount():
    headers_bdd = getHeadersTokenBaserow()
    response_bdd = requests.get('', headers=headers_bdd)
    response_bdd_json = response_bdd.json()
    lastNbPost = int(response_bdd_json[''])
    return lastNbPost
```

### 3. **Scraping LinkedIn**

The script performs web scraping on a LinkedIn profile page. A random `User-Agent` is used to avoid LinkedIn blocking the requests.

**Function `getContentPage`**:
This function sends an HTTP request to retrieve the content of the LinkedIn profile page.

```python
def getContentPage():
    url = ""
    user_agent = UserAgent()
    headers_linkedin = {
        'user-agent': user_agent.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }
    page = requests.get(url, headers=headers_linkedin)
    return page
```

### 4. **Updating Baserow**

If new posts are found on the LinkedIn page, the number of posts is updated in Baserow.

**Function `insertNewCountPost`**:
This function inserts the new post count into the database.

```python
def insertNewCountPost(lastNbPost):
    headers_bdd = getHeadersTokenBaserow()
    data = {'': lastNbPost}
    requests.patch('', headers=headers_bdd, json=data)
```

### 5. **Main Script**

The `main()` function is the entry point of the script. It coordinates the scraping, checking for new posts, and sending updates.

```python
def main():
    page = getContentPage()
    lastNbPost = getLastPostCount()

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        content_post = soup.find_all('p', class_='attributed-text-segment-list__content text-color-text !text-sm whitespace-pre-wrap break-words')
        currNbPost = len(content_post)

        if currNbPost > lastNbPost:
            insertNewCountPost(currNbPost)
            print("New post")
            lastPost = content_post[0].text
            data = {'post': lastPost}
            requests.post('', data=data)
        else:
            print("No new post")

main()
```

## How It Works

1. The script scrapes a LinkedIn profile page to retrieve the posts' content.
2. It checks if the number of posts has changed since the last run.
3. If the number of posts has increased, it updates the Baserow database and sends the latest post via a webhook.

## Configuration Variables

1. **Baserow Token**: You need to insert your own authentication token to access the Baserow API.
2. **LinkedIn URL**: The URL of the LinkedIn profile to scrape.
3. **Webhook**: You need to configure the webhook URL to send the latest post data.

## Dependencies

- **requests**: To perform HTTP requests.
- **beautifulsoup4**: To parse the HTML content of the scraped pages.
- **fake_useragent**: To generate random user-agents to avoid blocking.

