# Сборка фронта
FROM node:20 AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Добавляем переменную для поддержки OpenSSL 1
ENV NODE_OPTIONS=--openssl-legacy-provider

RUN npm run build

# Серверим статику через nginx
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
