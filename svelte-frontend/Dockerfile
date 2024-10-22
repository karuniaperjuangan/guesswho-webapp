FROM  node:22.6.0-alpine3.20 AS builder

WORKDIR /app

COPY . .

COPY package.json .

RUN npm install

RUN npm run build

FROM nginx:alpine3.20

COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]