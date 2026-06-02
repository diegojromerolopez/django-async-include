FROM ghcr.io/puppeteer/puppeteer:22.0.0

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY run_e2e.js .

CMD ["node", "run_e2e.js", "http://website:8000"]
