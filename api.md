## API Doc

路由前缀： /api/v1

### 不良语言检测

| 参数 | 值 | 说明 |
|:--: | :--:  |:--: |
| router | api/v1/sniffle | |
| method | POST | |
| Content-Type | ... | 传输类型，根据该值判断是传文件还是json |

Content-Type:
- 传文件：`multipart/form-data`
- 传json：`application/json`

**Request Params**

传文件：
| 参数名 | 位置 | 类型 | 说明 |
|:--: | :--:  |:--: | :--:|
| file | body | file stram | |

传 json：
```json
{
	"data": [
	    "123","test","是打发"
	]
}
```

**Response Data**
```json
{
    "msg": "ok",
    "data": [
        {
            "result": 0,
            "content": ""
        }
    ]
}
```

### 新闻列表

| 参数 | 值 | 说明 |
|:--: | :--:  |:--: |
| router | /article | |
| method | GET | |

**Request Params**
None

**Response Data**

```json
{
    "list": [
        {
            "id": 1,
            "name": "",
            "url": "",
            "type": 1,
            "date": "2021-03-04"
        }
    ]
}
```

### 新闻删除

| 参数 | 值 | 说明 |
|:--: | :--:  |:--: |
| router | /article | |
| method | DELETE | |

**Request Params**

不加数据默认全部删除

```json
{
    "list": [1,4,5,20] // 删除的文章 id
}
```

**Response Data**

```json
{
    "msg": "ok",
}
```

### 新闻新增

| 参数 | 值 | 说明 |
|:--: | :--:  |:--: |
| router | /article | |
| method | POST | |

**Request Params**

```json
{
    "list": [
        {
            "name": "",
            "url": "",
            "type": 1,
            "date": "2021-03-04"
        }
    ]
}
```

**Response Data**

```json
{
    "msg": "ok",
}
```