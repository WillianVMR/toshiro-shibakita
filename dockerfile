FROM nginx:latest

# Copia o arquivo nginx.conf customizado
COPY nginx.conf /etc/nginx/nginx.conf

# Expondo a porta configurada
EXPOSE 4500
