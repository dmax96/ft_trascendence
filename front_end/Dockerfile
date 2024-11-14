# Use the Nginx image from Docker Hub as the base image
FROM nginx:alpine

# Install openssl
RUN apk add --no-cache openssl

# Create a directory for the keys
RUN mkdir -p /etc/nginx/ssl


# Remove the default Nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf

# Copy the HTML file to the Nginx document root
COPY *.html /usr/share/nginx/html/

COPY nginx.key /etc/nginx/ssl/

COPY nginx.crt /etc/nginx/ssl/

COPY Despairs-X3Wxo.ttf /usr/share/nginx/html/

COPY media/ /usr/share/nginx/html/media

COPY *.js /usr/share/nginx/html/

# Copy the CSS file to the Nginx document root
COPY *.css /usr/share/nginx/html/

# Copy a configuration file from the current directory
COPY nginx.conf /etc/nginx/conf.d

# Expose ports 80 and 443
EXPOSE 80 443

# Start Nginx when the container has provisioned
CMD ["nginx", "-g", "daemon off;"]