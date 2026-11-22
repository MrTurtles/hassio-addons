FROM node:24-alpine AS frontend
WORKDIR /src
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM ghcr.io/home-assistant/base-python:3.14-alpine3.24
RUN apk add --no-cache nginx \
    && mkdir -p /run/nginx

WORKDIR /opt/meal-planner
COPY backend/requirements.txt ./
RUN python3 -m pip install --no-cache-dir -r requirements.txt
COPY backend/app ./app
COPY backend/migrations ./migrations
COPY backend/alembic.ini ./
COPY --from=frontend /src/dist ./static
COPY rootfs /
RUN rm -f /etc/nginx/http.d/default.conf \
    && find /etc/s6-overlay/s6-rc.d -type f \( -name run -o -name finish -o -name up \) -exec chmod 755 {} \;

ENV MEALPLANNER_ENV=production \
    MEALPLANNER_DATA_DIR=/data \
    MEALPLANNER_STATIC_DIR=/opt/meal-planner/static \
    PYTHONUNBUFFERED=1
