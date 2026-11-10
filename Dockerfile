# Single Railway image with a startup mode switch: dashboard (default) or variables.
# Keep Dashboard and Variables aligned with the pinned Ubuntu CLI release.
FROM nousresearch/hermes-agent:v0.23.1

USER root
COPY railway-entrypoint.sh /usr/local/bin/hermes-railway-entrypoint.sh
COPY dashboard-entrypoint.sh /usr/local/bin/hermes-railway-dashboard-entrypoint.sh
COPY variables/railway-entrypoint.sh /usr/local/bin/hermes-railway-variables-entrypoint.sh
COPY variables/generate-config.sh /usr/local/bin/hermes-railway-generate-config.sh
RUN chmod 0755 \
    /usr/local/bin/hermes-railway-entrypoint.sh \
    /usr/local/bin/hermes-railway-dashboard-entrypoint.sh \
    /usr/local/bin/hermes-railway-variables-entrypoint.sh \
    /usr/local/bin/hermes-railway-generate-config.sh

ENV HERMES_HOME=/opt/data \
    TZ=Asia/Jakarta

ENTRYPOINT ["/usr/local/bin/hermes-railway-entrypoint.sh"]
CMD ["gateway", "run"]
