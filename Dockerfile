# Roberto Rueda Fitness App - Railway Deployment
# Using official Odoo 18 base image
FROM odoo:18

# Switch to root for setup
USER root

# Copy fitness module
COPY odoo-18.0+e.20250521/custom_addons /mnt/extra-addons

# Copy config
COPY odoo.conf /etc/odoo/odoo.conf

# Set permissions and create directories
RUN mkdir -p /app/filestore && \
    chown -R odoo:odoo /mnt/extra-addons /etc/odoo /app/filestore

# Switch back to odoo user
USER odoo

# Expose Odoo port
EXPOSE 8069

# Use the standard Odoo entrypoint
ENTRYPOINT ["/entrypoint.sh"]
CMD ["odoo", "-c", "/etc/odoo/odoo.conf"] 