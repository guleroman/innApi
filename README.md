# innApi
## Описание
Веб-сервис для получения юридической информации об организации по ИНН.

## Подготовка
### 1. With Dockerfile
#### 1.1 Download the full repository located on this page
```
D:\> git clone https://github.com/guleroman/innApi.git
```
#### 1.2 Install docker
#### 1.3 Build.. 

```
D:\> docker build -t innapi .
```

..then Run (where x.x.x.x - you host)

```
D:\> docker run --name innapi -p x.x.x.x:8888:5000 -d innapi 
```

#### 1.4 Enjoy

In browser... (where 7704252261 - INN)
```
D:\> http://x.x.x.x:8888/api/?inn=7704252261
```
![img](/img/img1.jpg)



### 2. No Dockerfile
#### 2.1 Download the full repository located on this page
```
D:\> git clone https://github.com/guleroman/innApi.git
```
#### 2.2 Install requirements

```
D:\> cd innApi
```

```
D:\innApi> pip install -r requirements.txt 
```

#### 2.3 Run.. (where 7705353706 - INN)

```
D:\innApi> python innApi.py 7705353706 
```

#### 2.4 Enjoy

In browser...  
```
D:\> http://x.x.x.x:8888/api/?inn=7705353706
```
![img](/img/img2.jpg)

## Requirements
python 3.x.x

requests

bs4

flask

