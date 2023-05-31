## Запуск Docker контейнера
```
docker run -d --name docker-influxdb-grafana -p 3003:3003  -p 3004:8083  -p 8086:8086 -v </path/for/influxdb>:/var/lib/influxdb -v </path/for/grafana>:/var/lib/grafana -v <path/to/app>:/root/app anrewg/tig
```

## Порты
| Host |  Container  | Service |
|:-----|:--------:|------:|
| 3003   | 3003 | grafana |
| 3004   |  8083  |   chronograf |
| 8086   | 8086 |    influxdb |
					
### Подключение к контейнеру
`ssh -> docker exec -it <CONTAINER_ID> bash`
### Запуск скрипта для копирования данных из папки data в influxDB
`ssh -> docker exec <CONTAINER_ID> cd /root/app ; python3 data_to_db.py`
