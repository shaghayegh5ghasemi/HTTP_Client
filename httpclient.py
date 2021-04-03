import requests
import sys
import re
import os.path

#Parameters
url = sys.argv[1]
method = None
headers = {}
queries = {}
body = None
timeout = 80000
response = None

#Get the arguments
urlvalidation = re.compile(r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})")
if re.match(urlvalidation,url) == None:
    print("Invalid UrL")
    exit(0)

for index,argument in enumerate(sys.argv):
    if argument == "-M" or argument == "--method":
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
                print("*************************************************************")
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
        dataValidation = re.compile("([A-Za-z0-9%./]+=[^\s]+)")
        if re.match(dataValidation,sys.argv[index + 1]) == None:
            print("Data entered is not in the x-www-form-urlencoded format")
            print("*************************************************************")
        body = sys.argv[index + 1]
    if argument == "--json":
        if "content-type" not in headers.keys():
            headers["content-type"] = "application/json"
        if sys.argv[index + 1][0] != "{" or sys.argv[index + 1][-1] != "}" or ":" not in sys.argv[index + 1]:
            print("Data entered is not in the json format")
            print("*************************************************************")
        body = sys.argv[index + 1]
    if argument == "--timeout":
        timeout = float(sys.argv[index + 1])
    if argument == "--file":
        if "content-type" not in headers.keys():
            headers["content-type"] = "application/octet-stream"
        filePath = sys.argv[index + 1]
        if os.path.isfile(filePath):
            fileContent = open(filePath, "rb")
            body = fileContent.read()
        else:
            print("File does not exist!")
            print("*************************************************************")
            exit(0)
        

if(method == None):
    method = "GET"
   
#Send the request
try:
    if(method=="GET"):
        response = requests.get(url, params=queries, headers=headers, timeout=timeout, data=body, stream=True)
        
    if(method=="POST"):
        response = requests.post(url, params=queries, headers=headers, timeout=timeout, data=body, stream=True)
        
    if(method=="PUT"):
        response = requests.put(url, params=queries, headers=headers, timeout=timeout, data=body, stream=True)
            
    if(method=="PATCH"):
        response = requests.patch(url, params=queries, headers=headers, timeout=timeout, data=body, stream=True)

    if(method=="DELETE"):
        response = requests.delete(url, params=queries, headers=headers, timeout=timeout, data= body, stream=True)

    #print the result
    print("Method           -----> " + method)
    print("Status code      -----> " + str(response.status_code))
    print("Status Massage   -----> " + response.reason)
    print()
    print("Rsponse Headers: ")
    for i in response.request.headers.keys():
        print(i + " >>> " + response.request.headers[i])

    if response.headers['content-type'] in ["image/jpeg", "image/png", "video/ogg", "application/pdf", "application/octet-stream"]:
        file_type = response.url.split(".")
        file_name = "downloaded_file." + file_type[-1]
        myfile = open(file_name, "wb")
        total_size= int(response.headers.get('content-length', 0))
        block_size = 1024
        temp = 0
        for data in response.iter_content(block_size):
            myfile.write(data)
            temp += len(data)
            percent = (temp/total_size)*100
            print(int(percent), "%", end="\r")
        print("100")
        print("File name is: ", file_name)
    else:
        print()
        print("Body:")
        print(response.text)

except requests.exceptions.ConnectTimeout:
        print("Connection timed out")
        exit(0)
except:
    print("Server is unavailable!")
    exit(0)

