docker build -t tor-python-crawler .
docker stop tor_crawler_container
docker run --name tor_crawler_container -v /tmp:/tmp -p 5678:5678 -d --rm tor-python-crawler

Debug:
docker exec tor_crawler_container tor --version
docker exec tor_crawler_container service tor status
docker exec tor_crawler_container service tor start
