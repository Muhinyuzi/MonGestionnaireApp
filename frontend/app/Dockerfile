# ---------- BUILD ANGULAR ----------
FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# ✅ build PRODUCTION via package.json
RUN npm run build

# ---------- NGINX ----------
FROM nginx:alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

# ⚠️ Angular 18 → dist/app/browser
COPY --from=build /app/dist/app/browser /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
