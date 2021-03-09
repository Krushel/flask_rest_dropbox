## Flask rest api with dropbox as a BLOB storage

## Installation

Install flask and dropbox and start the server:
Windows:
```sh
pip install dropbox
pip install flask
```
Linux:
```sh
pip3 install dropbox
pip3 install flask
```

Then start /restflask/api.py

## Attributes: 
Attribute  | Type
------------- | -------------
key |String
value  |BLOB

## Links

Link  | Request
------------- | -------------
/create  |key and value in JSON reques
/update/<string:key>  |(key in link, value in JSON request)
/delete/<str:key> |(key in link)
/get/<str:key>  | (key in link)

Link  | Answer
------------- | -------------
/create  |{ "success": true}
/update/<string:key>  |{ "success": true}
/delete/<str:key> |{ "success": true}
/get/<str:key>  | binary value that match with a key