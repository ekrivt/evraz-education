# evraz-education

sudo apt-get update
  
sudo apt-get install -y apt-transport-https ca-certificates curl
  
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
  
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
   
sudo apt-get update

sudo apt-get install -y kubelet kubeadm kubectl

kubectl version

chmod +x ./kubectl

sudo mv ./kubectl /usr/local/bin/kubectl

kubectl version –client

curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.9.0/kind-linux-amd64

sudo chmod +x ./kind

sudo mv ./kind /usr/local/bin/kind

kind version

kind create cluster --config kind-config.yaml

Создайте файл конфигурации
kind: Cluster 
apiVersion: kind.x-k8s.io/v1alpha4 
nodes:
 - role: control-plane
 - role: worker
 - role: worker

Создайте файл: 

vi kind-config.yaml
нажмите ‘i’ для вставки текста, вставьте текст и сохраните используя комбинацию клавиш ESC и далее ‘:wq’
Запустите создание кластера
kind create cluster --config kind-config.yaml


kubectl get nodes


## Создание кластера с помошью kubeadm

wget https://tinyurl.com/yb4xturm -O rbac-kdd.yaml
wget https://tinyurl.com/y8lvqc9g -O calico.yaml



Для магазина носков

kubectl create namespace sock-shop
kubectl get namespace
wget https://tinyurl.com/y8bn2awp -O complete-demo.yaml
less complete-demo.yaml
kubectl apply -f complete-demo.yaml
kubectl get pods
kubectl get pods -n sock-shop
kubectl get svc -n sock-shop
