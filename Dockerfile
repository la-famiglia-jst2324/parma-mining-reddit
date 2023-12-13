FROM --platform=linux/amd64 mambaorg/micromamba:1.5.3

COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yml /tmp/environment.yml

RUN micromamba install -y -n base -f /tmp/environment.yml && \
micromamba clean --all --yes

WORKDIR /app

COPY --chown=$MAMBA_USER:$MAMBA_USER parma_mining /app/parma_mining

ENV FIREBASE_ADMINSDK_CERTIFICATE=$FIREBASE_ADMINSDK_CERTIFICATE
ENV REDDIT_API_KEY=$REDDIT_API_KEY
ENV REDDIT_BASE_URL=$REDDIT_BASE_URL
ENV REDDIT_CLIENT_ID=$REDDIT_CLIENT_ID
ENV REDDIT_DATA_SOURCE=$REDDIT_DATA_SOURCE
ENV ANALYTICS_BASE_URL=$ANALYTICS_BASE_URL

EXPOSE 8080

ENTRYPOINT ["/usr/local/bin/_entrypoint.sh"]
CMD ["uvicorn", "parma_mining.reddit.api:app", "--host", "0.0.0.0", "--port", "8080"]
