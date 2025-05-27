# Roberto Rueda Fitness App - Railway Deployment
# Using official Odoo 18 base image
FROM odoo:18

# Switch to root for setup
USER root

# Install envsubst for environment variable substitution and gosu for user switching
RUN apt-get update && apt-get install -y gettext-base gosu && rm -rf /var/lib/apt/lists/*

# Copy fitness module
COPY odoo-18.0+e.20250521/custom_addons /mnt/extra-addons

# Copy Railway-specific config template
COPY odoo.railway.conf /etc/odoo/odoo.railway.conf

# Copy custom entrypoint
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Set permissions and create directories
RUN mkdir -p /app/filestore && \
    chown -R odoo:odoo /mnt/extra-addons /etc/odoo /app/filestore /docker-entrypoint.sh && \
    chmod -R 755 /app/filestore

# Don't switch to odoo user yet - entrypoint needs root for permissions
# USER odoo

# Expose Odoo port
EXPOSE 8069

# Use our custom entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["gosu", "odoo", "odoo", "-c", "/etc/odoo/odoo.conf"] 