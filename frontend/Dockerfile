FROM node:18-alpine AS build
# Add a work directory
WORKDIR /app
# Install pnpm
RUN npm install -g pnpm
# Cache and Install dependencies
COPY package.json .
COPY pnpm-lock.yaml .
RUN pnpm install
# Copy app files
COPY . .
# Start the app
RUN pnpm run build

FROM nginx:1.19-alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx/default.conf.template /etc/nginx/templates/default.conf.template
