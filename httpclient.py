import requests
import sys
import re

url = sys.argv[1]
method = None
headers = {}
queries = {}
body = None
timeout = 80000
response = None
urlvalidation = re.compile(r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})")
if re.match(urlvalidation,url) == None:
    print("Invalid UrL")
    exit(0)

for index,argument in enumerate(sys.argv):
    if(argument == "-M" or argument == "--method"):
        if sys.argv[index + 1].upper() not in ["GET","POST","PATCH" , "DELETE","PUT"]:
            print("Invalid Method")
            exit(0)
        method = sys.argv[index + 1].upper()
    if argument == "-H" or argument == "--headers":
        h = sys.argv[index + 1].split(",")
        for i in h:
            temp = i.split(":")
            if temp[0] in headers.keys():
                print("Pay Attention! Duplicated Headers.")
            headers[temp[0].lower()] = temp[1]
    if argument == "-Q" or argument == "--queries":
        q = sys.argv[index + 1].split("&")
        for i in q:
            temp = i.split("=")
            if temp[0] in queries.keys():
                print("Pay Attention! Duplicated Queries.")
            queries[temp[0]] = temp[1]
    if argument == "-D" or argument == "--data":
        if "content-type" not in headers.keys():
            headers["content-type"] = "application/x-www-form-urlencoded"
        body = sys.argv[index + 1]
    if argument == "--json":
        if "content-type" not in headers.keys():
            headers["content-type"] = "application/json"
        body = sys.argv[index + 1]
    if argument == "--timeout":
        timeout = float(sys.argv[index + 1])
        

if(method == None):
    method = "GET"

try:
    if(method=="GET"):
        response = requests.get(url, params=queries, headers=headers, timeout=timeout)

    if(method=="POST"):
        response = requests.post(url, params=queries, headers=headers, timeout=timeout, data=body)
        
    if(method=="PUT"):
        response = requests.put(url, params=queries, headers=headers, timeout=timeout, data=body)
            

    if(method=="PATCH"):
        response = requests.patch(url, params=queries, headers=headers, timeout=timeout, data=body)

    if(method=="DELETE"):
        response = requests.delete(url, params=queries, headers=headers, timeout=timeout)

except requests.exceptions.ConnectTimeout:
        print("Connection timed out")
        exit(0)
except:
    print("Server is unavailable!")
    exit(0)

#print the result
print("Method           -----> " + method)
print("Status code      -----> " + str(response.status_code))
print("Status Massage   -----> " + response.reason)
print("Rsponse Headers: ")
for i in response.request.headers.keys():
    print(i + " >>> " + response.request.headers[i])