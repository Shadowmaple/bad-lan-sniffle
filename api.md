## API Doc

### 不良语言检测

| router | method | header |
|:--: | :--:  |:--: |
| api/v1/sniffle | POST  | None |

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
	    "123","sasda","是打发"
	]
}
```

**Response Data**
```json
{

}
```

### 新闻列表


### 新闻删除


### 新闻新增
