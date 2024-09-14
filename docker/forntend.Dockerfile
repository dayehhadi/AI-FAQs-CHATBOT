# Use an official Nginx image to serve the frontend
FROM nginx:alpine

# Remove default Nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy the frontend files
COPY frontend /usr/share/nginx/html

# Expose port
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
