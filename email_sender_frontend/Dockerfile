FROM node:20-alpine
 
# Set working directory
WORKDIR /app
 
# Install dependencies separately to cache
COPY package.json package-lock.json ./
RUN npm install
 
# Copy source (optional in dev since we're using volume)
COPY . .
 
# Expose dev server port
EXPOSE 3000
 
# Run your dev server (adjust if needed)
CMD ["npm", "start"]