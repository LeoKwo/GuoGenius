# GuoGenius
GuoGenius中国宝宝特供版
#### Deployment
部署在阿里云轻量化服务器上。大模型使用DeepSeek-V3。
#### Avaible on...
[https://ruikang.tech/](https://ruikang.tech/)
### Running the bot - local
```
streamlit run guogenius.py
```
### Running the bot - server
1. install pm2
2. ```
    pm2 start myenv/bin/streamlit \
        --name guogenius \
        --interpreter ./myenv/bin/python3.11 \
        -- run guogenius.py --server.port 8501 --server.headless true```
3. pm2 save
4. install nginx
5. enable the bot with ```/etc/nginx/sites-enabled/streamlit```
    ```
    server {
        server_name bot.ruikang.tech;

        location / {
            proxy_pass http://localhost:8501;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        listen 443 ssl; # managed by Certbot
        ssl_certificate /etc/letsencrypt/live/bot.ruikang.tech/fullchain.pem; # managed by Certbot
        ssl_certificate_key /etc/letsencrypt/live/bot.ruikang.tech/privkey.pem; # managed by Certbot
        include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
        ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

    }

    server {
        if ($host = bot.ruikang.tech) {
            return 301 https://$host$request_uri;
        } # managed by Certbot
        listen 80;
        server_name bot.ruikang.tech;
        return 404; # managed by Certbot
    }

    ```
