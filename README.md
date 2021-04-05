# bad-lan-sniffle

### API Doc

[文档](./api.md)

### Run

```shell
python3 manage.py
# or
flask run -h 127.0.0.1 -p 5000
```

### Docker

#### 构建

```shell
docker build -t bad-lan-sniffle:0.1 .
```

#### 创建 DB

先进入容器
```shell
docker ps
docker exec -it {CONTAINER ID} /bin/bash
```

再使用python命令行创建
```python3
from app import db
db.create_all()
```