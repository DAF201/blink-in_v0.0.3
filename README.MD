this was designed for image bed initally. I am using github for now since I cannot find a good place to store at this moment

#APIs

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
