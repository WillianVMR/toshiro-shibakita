# Balanceador de Carga NGINX com Docker

Este projeto configura um balanceador de carga baseado no NGINX para distribuir tráfego entre vários servidores backend. A configuração inclui recursos como timeouts, balanceamento de carga com `least_conn` e cabeçalhos personalizados.

## Funcionalidades
- Balanceamento de carga entre múltiplos servidores.
- Timeouts configuráveis para maior confiabilidade.
- Logs para monitoramento de acessos e erros.
- Suporte a cabeçalhos modernos (`X-Real-IP`, `X-Forwarded-For`).

---

## Como começar

### Pré-requisitos
1. Ter o [Docker](https://docs.docker.com/get-docker/) instalado.
2. Opcionalmente, ter o [Docker Compose](https://docs.docker.com/compose/install/) para facilitar o gerenciamento de múltiplos contêineres.

---

### Arquivos de Configuração

#### `nginx.conf`
Este arquivo contém a configuração do NGINX para balanceamento de carga. A configuração distribui o tráfego para três servidores backend e escuta na porta `4500`.

```nginx
http {
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;
    send_timeout 60s;

    upstream all {
        server 172.31.0.37:80 max_fails=3 fail_timeout=30s;
        server 172.31.0.151:80 max_fails=3 fail_timeout=30s;
        server 172.31.0.149:80 max_fails=3 fail_timeout=30s;
        least_conn;
    }

    server {
        listen 4500;

        location / {
            proxy_pass http://all/;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}

events { }
```

```
Dockerfile
```
O Dockerfile constrói uma imagem customizada do NGINX com a configuração fornecida.

```Dockerfile
FROM nginx:latest

# Copia a configuração personalizada do NGINX
COPY nginx.conf /etc/nginx/nginx.conf

# Expõe a porta configurada
EXPOSE 4500
```


### Processo de build:

Passo 1: Construir a imagem Docker
```
docker build -t custom-nginx .
```

Passo 2: Executar o contêiner do NGINX
```
docker run -d -p 4500:4500 --name nginx-load-balancer custom-nginx
```

Passo 3: Testar o balanceador de carga
Acesse o balanceador de carga utilizando o navegador ou qualquer cliente HTTP:
```
http://<IP_DO_HOST>:4500
```

Passo 2: Executar o contêiner do NGINX
```
docker run -d -p 4500:4500 --name nginx-load-balancer custom-nginx
```

Passo 4 (Opcional): Usando Docker Compose
Se estiver utilizando o arquivo docker-compose.yml, inicie o serviço com:
```
docker-compose up -d
```
