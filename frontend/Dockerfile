# Use official Node.js image as a base
FROM node:16

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy project files
COPY . .

# Run the build process
RUN npm run build

# Expose the application
EXPOSE 8080

# Set the environment variable
ENV PORT 8080

# Install serve globally
RUN npm install -g serve

# Serve the application
CMD ["serve", "-s", "dist"]
