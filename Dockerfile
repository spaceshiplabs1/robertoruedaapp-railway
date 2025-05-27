# Roberto Rueda Fitness App - Railway Deployment
# Using official Odoo 18 base image
FROM odoo:18

# Switch to root for setup
USER root

# Copy custom fitness module
COPY odoo-18.0+e.20250521/custom_addons /mnt/extra-addons

# Copy main configuration
COPY odoo.conf /etc/odoo/odoo.conf

# Create and set permissions for all directories
RUN mkdir -p /app/filestore /var/lib/odoo && \
    chown -R odoo:odoo /mnt/extra-addons /etc/odoo /app/filestore /var/lib/odoo

# Switch back to odoo user
USER odoo

# Set working directory
WORKDIR /usr/lib/python3/dist-packages/odoo

# Expose Odoo port
EXPOSE 8069

# Start Odoo with our configuration
# Using python3 explicitly since that's what's available in the container
CMD ["python3", "/usr/lib/python3/dist-packages/odoo/odoo-bin", "-c", "/etc/odoo/odoo.conf"] 