this was designed for image bed initally. I am using github for now since I cannot find a good place to store at this moment

https://blink-in.com

# API

```python
from requests import post
#upload file
with open("test.py", "rb") as t:
    r = post(
        "https://blink-in.com/API", params={"editor_data": "{}"}, files={"test.py": t}
    )

#download file
with open("test.zip", "wb") as tz:
    tz.write(
        post(
            "https://blink-in.com/API", params={"editor_data": '{"0":"test.py"}'}
        ).content
    )

```

# WEB

## download

enter/paste the target files as json to editor and click upload, ensure no file selected for upload at same time

![](https://github.com/DAF201/blink-in_v0.0.3/blob/master/static_files/image/download.png)

## upload

select files and click upload

![](https://github.com/DAF201/blink-in_v0.0.3/blob/master/static_files/image/upload.png)
