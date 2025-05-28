# Roberto Rueda Fitness App - Ultra Minimal
FROM odoo:18
USER root

# Install essentials and create directories in one layer
RUN apt-get update && apt-get install -y --no-install-recommends gettext-base postgresql-client \
    && rm -rf /var/lib/apt/lists/* && mkdir -p /mnt/enterprise-addons /mnt/extra-addons

# Copy enterprise modules for fitness business
COPY enterprise_addons/sale_subscription /mnt/enterprise-addons/sale_subscription/
COPY enterprise_addons/crm_enterprise /mnt/enterprise-addons/crm_enterprise/
COPY enterprise_addons/account_accountant /mnt/enterprise-addons/account_accountant/
COPY enterprise_addons/calendar_sms /mnt/enterprise-addons/calendar_sms/
COPY enterprise_addons/crm_sale_subscription /mnt/enterprise-addons/crm_sale_subscription/

# Copy custom fitness module (15 models)
COPY custom_addons /mnt/extra-addons/

# Copy configuration
COPY odoo.railway.conf /etc/odoo/odoo.conf
COPY docker-entrypoint.sh /docker-entrypoint.sh

# Set permissions and user
RUN chmod +x /docker-entrypoint.sh && chown -R odoo:odoo /mnt/enterprise-addons /mnt/extra-addons /etc/odoo /docker-entrypoint.sh

USER odoo
EXPOSE 8069
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["odoo", "-c", "/etc/odoo/odoo.conf"] 