# Лабораторная работа 5

https://console-openshift-console.apps.osw.ntmk.ru/

https://registry.ural.evraz.com/

## Push приложения в registry

```shell
cd app
```

В случае, если Docker не работает без _sudo_

```shell
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
```

Авторизируемся в registry
```shell
docker login $REGISTRY
```
или

```shell
podman login $REGISTRY # --tls-verify=false
```

Собираем образ и присваиваем ему тэг
```shell
docker build -t ${REGISTRY}/${SURNAME}-test-app:1.0.0 .
```

Делаем push во внешний registry
```shell
docker push ${REGISTRY}/${SURNAME}-test-app:1.0.0
```

![img](./.readme-images/01-registry.png)

## Деплой приложения

Заходим в OpenShift кластер

![img](./.readme-images/02-cluster.png)

При желании, можете делать эти же операции в терминале

```shell
oc login $CLUSTER_API_ADDRESS -u $YOUR_USERNAME
```

Создадим новый проект:
1) Нажимаем на `Administrator`, переключимся на `Developer`
2) Вверху кликаем на выпадающий список `Project: ...`
3) Нажимаем `Create Project`

Создадим новое приложение:
1) Нажимаем на `+Add`
2) Выбираем `Container Image`
3) Нажимаем `create an Image pull secret`. Заполняем поля, используя те же данные что и для docker login
4) Вводим тот тэг образа, с которым вы делали docker push
5) Нажимаем `Create`

![img](./.readme-images/03-new-app.png)

Отредактируем _deployment_ для нашего приложения. Это нужно сделать, чтобы _deployment_ знал какой _secret_ нужно использовать при скачке образа из registry.

1) Нажимаем на `Topology`
2) Выбираем приложение
3) Нажимаем `Actions`
4) Нажимаем `Edit Deployment`
5) Добавляем
```yaml
imagePullSecrets:
  - name: имя того secret, который был создан для registry
```
6) Сохраняем

![img](./.readme-images/04-edit-deploy.png)

На этом этапе приложение должно начать деплой и стать доступно через несколько секунд.

1) Нажимаем на `Topology`
2) Выбираем приложение
3) Нажимаем `View Logs`

![img](./.readme-images/05-logs.png)

1) Нажимаем на `Topology`
2) Выбираем приложение
3) Кликаем на ссылку в секции `Routes`

![img](./.readme-images/06-route.png)
