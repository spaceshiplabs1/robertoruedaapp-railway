# Use Railway's Odoo base image or official Odoo image
FROM odoo:18

# Set the user to root to install packages and copy files
USER root

# Copy our custom addons to the extra-addons directory
COPY odoo-18.0+e.20250521/custom_addons /mnt/extra-addons

# Copy our configuration files
COPY odoo.conf /etc/odoo/odoo.conf
COPY odoo_local.conf /etc/odoo/odoo_local.conf

# Set proper permissions
RUN chown -R odoo:odoo /mnt/extra-addons /etc/odoo

# Switch back to odoo user
USER odoo

# Expose port
EXPOSE 8069

# Set the default command to run Odoo with our addons
CMD ["python", "/usr/lib/python3/dist-packages/odoo/odoo-bin", "-c", "/etc/odoo/odoo.conf", "--addons-path=/mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons"] 