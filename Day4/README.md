# Лабораторная работа 4

## Пререквизиты

- Наличие учетной записи RedHat ([https://cloud.redhat.com/openshift](https://cloud.redhat.com/openshift))
- Наличие ~35GB свободного дискового пространства (`df -h`)

## Установка CodeReady Containers

Устанавливаем необходимые зависимости
```shell
sudo apt install qemu-kvm libvirt-daemon libvirt-daemon-system network-manager
```

Скачиваем CRC
```shell
wget https://mirror.openshift.com/pub/openshift-v4/clients/crc/1.26.0/crc-linux-amd64.tar.xz
```

Распаковываем
```shell
tar -xvf crc-linux-amd64.tar.xz
```

Для удобства перемещаем в `/usr/local/bin/`
```shell
sudo mv crc-linux-1.26.0-amd64/crc /usr/local/bin/
```

_В рамках лабораторной работы, из-за некоторых ограничений виртуальной машины, мы вынуждены сделать действия ниже. В иных условиях эти действия не потребуются._

```shell
crc config set network-mode vsock
```
либо
```shell
crc config set skip-check-systemd-networkd-running true
```

```shell
sudo bash -c "echo 'options kvm ignore_msrs=1' >> /etc/modprobe.d/qemu-system-x86.conf"
```

Выполняем установку CodeReady Containers
```shell
crc setup
```

_В отдельном терминале запускаем демона для vsock_ *
```shell
crc daemon
```

В браузере переходим на [https://cloud.redhat.com/openshift/create/local](https://cloud.redhat.com/openshift/create/local) под своей учетной записью. Нажимаем на кнопку `Copy pull secret`.

Возвращаемся в терминал, запускаем CRC.
```shell
crc start
```

Вставляем _pull secret_, на этапе когда мастер установки нас об этом попросит.

Первоначальный запуск займет какое-то время.

В конце ожидаем увидеть приблизительно такой вывод:

```
Started the OpenShift cluster.

The server is accessible via web console at:
  https://console-openshift-console.apps-crc.testing

Log in as administrator:
  Username: kubeadmin
  Password: aaaaa-bbbbb-ccccc-ddddd

Log in as user:
  Username: developer
  Password: developer

Use the 'oc' command line interface:
  $ eval $(crc oc-env)
  $ oc login -u developer https://api.crc.testing:6443
```

## Установка OC и ODO

### Установка Openshift Client

Скачиваем _oc_
```shell
wget https://mirror.openshift.com/pub/openshift-v4/clients/oc/latest/linux/oc.tar.gz
```

Распаковываем
```shell
tar -xvf oc.tar.gz
```

Для удобства перемещаем в `/usr/local/bin/`
```shell
sudo mv -t /usr/local/bin/ oc kubectl
```

Авторизируемся в кластере как админ. Вводим пароль, полученный на этапе установки
```shell
oc login https://api.crc.testing:6443 -u developer
```

### Установка ODO

Скачиваем _odo_
```shell
wget https://mirror.openshift.com/pub/openshift-v4/clients/odo/latest/odo-linux-amd64
```

Даем права на запуск
```shell
chmod +x odo-linux-amd64
```

Для удобства перемещаем в `/usr/local/bin/`
```shell
sudo mv odo-linux-amd64 /usr/local/bin/odo
```

Авторизируемся в кластере как разработчик. Вводим пароль, полученный на этапе установки
```shell
odo login https://api.crc.testing:6443 -u developer
```

## Развертка приложения
### С помощью _odo_

Перейдем в директорию _app_
```shell
cd app
```

Создадим новый проект
```shell
odo project create django-by-odo
```

Создаем _component_
```shell
odo create python
```

Меняем команду запуска приложения
```shell
nano devfile.yaml
```
Меняем `commandLine: python app.py` на `commandLine: python manage.py runserver`

```shell
odo config set --env PYTHONUNBUFFERED=1
```

Выполняем деплой проекта
```shell
odo push
```

Смотрим логи
```shell
odo log
```

### С помощью _oc_

Перейдем в директорию _app_
```shell
cd app
```

Создадим новый проект в CRC
```shell
oc new-project django-by-oc
```

Докеризуем приложение, создав простой Dockerfile `nano Dockerfile`
```Docker
FROM python:3

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

COPY . .
RUN pip install -r requirements.txt
RUN python manage.py migrate

CMD [ "python", "manage.py", "runserver" ]
```

Установим _podman_
```shell
source /etc/os-release
sudo sh -c "echo 'deb http://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/ /' > /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list"
wget -nv https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable/xUbuntu_${VERSION_ID}/Release.key -O- | sudo apt-key add -
sudo apt-get update -qq
sudo apt-get -qq --yes install podman
```

Авторизируемся во внутринем registry
```shell
podman login -u developer -p $(oc whoami -t) default-route-openshift-image-registry.apps-crc.testing --tls-verify=false
```

Собираем образ
```shell
podman build -t default-route-openshift-image-registry.apps-crc.testing/django-by-oc/django-by-oc-image .
```

Отправляем образ в registry
```shell
podman push default-route-openshift-image-registry.apps-crc.testing/django-by-oc/django-by-oc-image --tls-verify=false
```

Выполняем деплой приложения
```shell
oc set image-lookup django-by-oc-image

oc new-app django-by-oc-image
```
