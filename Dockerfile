# Utilisez une image de base qui contient un système d'exploitation Linux
FROM debian:bullseye-slim

# Mettez à jour les paquets et installez les outils de développement C
RUN apt-get update && apt-get install -y build-essential
RUN apt-get install -y python3 python3-pip 
RUN pip install requests beautifulsoup4
RUN pip install fake_useragent

#docker run --rm -it  -v $(pwd):/scrapping image-scrapping