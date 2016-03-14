#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import base64
import json
import urllib.request
import sys
import os

GITHUB_REPOS_API_BASE_URL = 'https://api.github.com/repos/'

def write_file(item, dir_name):
    name = item['name']
    url = item['url']

    request = urllib.request.Request(url)
    """
    # if you have github token, you can try add autorization into request
    token = "3c1ba9c29be3ebb06a1d9401e76a672104b432cf"
    request.add_header('Authorization', 'token %s' % token)
    """
    # request type is <urllib.request.Request object at 0x7fcae7e380b8>
    # https://docs.python.org/3/library/urllib.request.html#request-objects

    responce = urllib.request.urlopen(request)
    # https://docs.python.org/3/library/http.client.html#httpresponse-objects

    # you can view some information in responce header:
    # for key, value in responce.getheaders():
    #     print(key, '=', value)

    body = responce.read()
    # Reads and returns the response body type(body) = <class 'bytes'>.
    #
    # b'{"name":"bugs.html",
    # "path":"dir/bugs.html",
    # "sha":"e1d69557f6daa8143a84b47d5999459af186bb8b",
    # "size":7592,
    # "url":"https://api.github.com/repos/swasher/testrepo/contents/dir/bugs.html?ref=master",
    # "html_url":"https://github.com/swasher/testrepo/blob/master/dir/bugs.html",
    # "git_url":"https://api.github.com/repos/swasher/testrepo/git/blobs/e1d69557f6daa8143a84b47d5999459af186bb8b",
    # "download_url":"https://raw.githubusercontent.com/swasher/testrepo/master/dir/bugs.html",
    # "type":"file",
    # "content":"PCFET0NUWVBFIGh0bWw+CjxodG1sIGxhbmc9ImVuIj4KPGhlY"
    # "encoding":"base64",
    # "_links":{"self":"https://api.github.com/repos/swasher/testrepo/contents/dir/bugs.html?ref=master",
    # "git":"https://api.github.com/repos/swasher/testrepo/git/blobs/e1d69557f6daa8143a84b47d5999459af186bb8b",
    # "html":"https://github.com/swasher/testrepo/blob/master/dir/bugs.html"}}'


    body_utf = body.decode('utf-8')
    # Convert bytes to string, using utf-8 coding
    # body_utf type is <class 'str'>


    # Convert string into python data structure. Its actually json's encoding. Try decode:
    responce_dict = json.loads(body_utf)
    # ok, now we have dict: type(responce_dict) == <class 'dict'>


    # Let's see, what store in content:
    coded_string = responce_dict['content']
    # Its a string: type(content) == <class 'str'>
    # And `content` have something like
    # R0lGODlhZABAAOf/AAABAAMFAQcJBRETEBQWExYZGxgZFx0fHCQmJC0uLJkC
    # AJEIAZMMApsHB5wIAKUEADM1MpQNAJ4MCZ8OAqERAKkNALIJADs+PrQNAKQV
    # BpsYEJwZCa0TAq0UAEFDQLgTALMbALsYArMcB6MhHERJS8QWAKwgDb0aAKYk
    # GL0bDUlLSMcbAbAkF8whANQdAE1SVMUlC6kwI7crHNciAlVXVNolANIoCuIi


    # Trying decode using base64 algorithm
    contents = base64.b64decode(coded_string)
    # contents type is <class 'bytes'>
    # Now contents store binary data, which can write directly to file, like this:
    # for image
    # b'GIF89ad\x00@\x00\xe7\xff\x00\x00\x01\x00\x03\x05\x01\x07\t\x05\x11\x13\x10\x14\x16\x13\x16\x19\x1b\x18\x19\x17\x1d\x1f\x1'
    # for text
    # b'<!DOCTYPE html>\n<html lang="en">\n<head>\n <title>\xd0\x97\xd0\xb0\xd0\xbf\xd0\xb8\xd1\x81\xd0\xba\xd0\xb8 \xd0\xbe'


    print(os.path.join(dir_name, name))
    # Write binary into file
    with open(os.path.join(dir_name, name), 'wb') as f:
        f.write(contents)


def write_files(url, dir_name):

    print('url', url)
    os.makedirs(dir_name)
    responce = urllib.request.urlopen(url).read().decode('utf-8')
    github_dir = json.loads(responce)
    for item in github_dir:
        if item['type'] == 'file':
            write_file(item, dir_name)
        elif item['type'] == 'dir':
            write_files(item['url'], dir_name=os.path.join(dir_name, item['name']))


if __name__ == '__main__':
    args = dict(enumerate(sys.argv))
    path = args[1]
    path = path.split('/')

    new_dir_name = path[-1]
    if os.path.exists(new_dir_name):
        print('Directory', new_dir_name, 'already exists')
        exit()

    # use contents api
    path.insert(2, 'contents')
    path = '/'.join(path)

    write_files(GITHUB_REPOS_API_BASE_URL + path, new_dir_name)
