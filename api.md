## API Doc

host: ...
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

**based query：**
| 参数名 | 位置 | 类型 | 说明 |
|:--: | :--:  |:--: | :--:|
| kind | query | int | 分类器类型，0/1/2/3 |

| kind | 分类器 |
| :--: | :--: |
| 0 | 文本图+简单自训练算法 |
| 1 | Doc2vec+CentroidEM |
| 2 | SIF+Word2vec+CentroidEM |
| 3 | TFIDF+CentroidEM |

**传文件：**
| 参数名 | 位置 | 类型 | 说明 |
|:--: | :--:  |:--: | :--:|
| file | body | file stram | |

文件内容：
```
123
test
太强了
```

**传 json：**
```json
{
	// "data": [
	//     "123","test","太强了"
	// ],
    "data": [
        {
            "content": "123",
            "file_name": ""
        },{
            "content": "test",
            "file_name": ""
        },{
            "content": "太强了",
            "file_name": ""
        }
    ]
}
```


**Response Data**
```json
{
    "msg": "ok",
    "data": [
        {
            "result": 0, // 0为非不良语言
            "content": "123",
            "file_name": ""
        }, {
            "result": 0,
            "content": "test",
            "file_name": ""
        }, {
            "result": 0,
            "content": "太强了",
            "file_name": ""
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

| 参数名 | 位置 | 类型 | 说明 |
|:--: | :--:  |:--: | :--:|
| kind | query | int | 板块类型，取值为0/1/2/3 |

**Response Data**

```json
{
    "list": [
        {
            "id": 1,
            "name": "",
            "url": "",
            "kind": 1,
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

| 参数名 | 位置 | 类型 | 说明 |
|:--: | :--:  |:--: | :--:|
| Authorization | header | string | basic base64(username:pwd) |

不加数据默认全部删除

```json
{
    "list": [1,4,5,20], // 删除的文章 id
    "kind": 0, // 若全部删除，则选定需要删除的板块
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

| 参数名 | 位置 | 类型 | 说明 |
|:--: | :--:  |:--: | :--:|
| Authorization | header | string | basic base64(username:pwd) |

```json
{
    "list": [
        {
			"name": "1.关于人工智能的未来，张亚勤、张宏江在聊什么",
			"url": "https://www.jiqizhixin.com/articles/2021-03-30-12",
			"kind": 0,
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