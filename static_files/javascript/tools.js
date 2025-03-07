
function print(str) {
    console.log(str)
}

function replace_innerHTML(id, str) {
    document.getElementById(id).innerHTML = str
}

async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function including(Obj, ...Objs) {
    return Objs.includes(Obj)
}

function hide_element(id) {
    for (let i = 0; i < id.length; i++) {
        document.getElementById(id[i]).style.display = "none"
    }
}

function show_element(id) {
    for (let i = 0; i < id.length; i++) {
        document.getElementById(id[i]).style.display = "block"
    }
}

function element_display_toggle(id) {
    for (let i = 0; i < id.length; i++) {
        if (document.getElementById(id[i]).style.display != "none") {
            document.getElementById(id[i]).style.display = "none"
        } else {
            document.getElementById(id[i]).style.display = "block"
        }
    }
}

function request(method, URL, param, callback = function () { }, callback_args = []) {
    let http_request = new XMLHttpRequest()
    try {
        http_request.open(method, URL)
        http_request.send(param)
        http_request.onloadend = function () {
            data_backup = http_request.responseText
            callback(http_request.responseText, callback_args)
        }
    } catch (err) {
        print(err)
    }
}

function request_json(method, URL, params) {
    let request = XMLHttpRequest()
    request.open(method, URL, false)
    request.send(JSON.stringify(params))
}

async function upload() {
    const file_list = document.getElementById("file_list");
    file_list.innerHTML = "";
    let form = new FormData();
    const files = document.getElementById("file_input").files;

    for (let i = 0; i < files.length; i++) {
        form.append(i, files[i]);
    }
    form.append("editor_data", editor.getValue());

    try {
        let r = await fetch("/API", {
            method: "POST",
            body: form
        });

        let rClone = r.clone();
        let contentType = r.headers.get("Content-Type");
        if (contentType && contentType.includes("application/json")) {
            let j = await r.json();
            let res = {};
            let c = 0;
            Object.keys(j).forEach((key) => {
                res[c++] = j[key]["file_name"];
            });
            editor.setValue(JSON.stringify(res));
            document.getElementById("file_input").value = "";
            return
        } else {
            let b = await rClone.blob();
            let blob_url = window.URL.createObjectURL(b);
            let a = document.createElement('a');
            a.href = blob_url;
            a.download = "blink-in.zip";
            a.target = "_blank";
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(blob_url);
        }
    } catch (error) {
        console.error("An error occurred:", error);
    }
    editor.setValue("{}")
    document.getElementById("file_input").value = "";
}


function file_upload_display() {
    document.getElementById("file_input").addEventListener("change", function (event) {
        const file_list = document.getElementById("file_list")
        file_list.innerHTML = ""
        for (const file of event.target.files) {
            const list_item = document.createElement("li")
            list_item.textContent = file.name
            file_list.appendChild(list_item)
        }
    })
}