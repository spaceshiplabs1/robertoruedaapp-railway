# Use official Odoo image
FROM odoo:18

# Set the user to root to install packages and copy files
USER root

# Copy our custom addons to the extra-addons directory
COPY odoo-18.0+e.20250521/custom_addons /mnt/extra-addons

# Copy our configuration files
COPY odoo.conf /etc/odoo/odoo.conf

# Set proper permissions
RUN chown -R odoo:odoo /mnt/extra-addons /etc/odoo

# Create necessary directories
RUN mkdir -p /app/filestore && chown -R odoo:odoo /app/filestore

# Switch back to odoo user
USER odoo

# Expose port
EXPOSE 8069

# Use the exact same command as the base Odoo image but with our config
CMD ["/usr/local/bin/odoo", "-c", "/etc/odoo/odoo.conf"] 