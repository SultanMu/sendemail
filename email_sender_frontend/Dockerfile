# Use Node.js 20 Alpine as the base image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application data
COPY . .

# Expose the new Vite port
EXPOSE 5175

# Run in development mode with hot reloading on the new port
CMD ["npx", "vite", "--host", "0.0.0.0", "--port", "5175"]
