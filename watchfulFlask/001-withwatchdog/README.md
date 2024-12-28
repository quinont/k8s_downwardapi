# para ejecutar
``` 
docker build -t logwatchapi .

docker run -p 8080:8080 watchfulflask
```

## Para correr


Importante: el watchdog solo funciona cuando se monta el volumen y no el archivo. Tener cuidado con esto.

```
docker run -p 8080:8080 -e CONFIG_DIR="/config/" -e CONFIG_FILE_NAME="log_config.txt" -v $PWD/:/config/ --rm watchfulflask:1
```
