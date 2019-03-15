from sys import argv
import os
cmd1 = 'sudo yum install nginx httpd-tools -y'
cmd2 = 'sudo amazon-linux-extras install nginx1.12 -y'
os.system(cmd1)
os.system(cmd2)

es_endpoint = argv[1]
conf_file_part1 = "events { worker_connections  1024; }\n" +  "http {\n  upstream elasticsearch {\n server 127.0.0.1:80;\n keepalive 15;  }\n"+"server {\n listen 80;\n location / {\n proxy_pass "+es_endpoint+";\n  proxy_http_version 1.1;\n proxy_set_header Connection 'Keep-Alive';\n    proxy_set_header Proxy-Connection 'Keep-Alive';}\n}\n}\n"


f = open("nginx_keep_alive.conf", 'w')
f.write(conf_file_part1)
f.close()

cmd3 = 'sudo cp nginx_keep_alive.conf /etc/nginx/conf.d/nginx_keep_alive.conf'
cmd4 = 'sudo nginx -p /etc/nginx/ -c /etc/nginx/conf.d/nginx_keep_alive.conf'
os.system(cmd3)
os.system(cmd4)
