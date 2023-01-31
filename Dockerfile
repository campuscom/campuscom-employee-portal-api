FROM python:3.7 AS compile-image

WORKDIR /opt/app
RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

# Add credentials on build
RUN mkdir /root/.ssh/
ARG SSH_PRIVATE_KEY
RUN echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa && chmod 600 /root/.ssh/id_rsa

# Make sure your domain is accepted
# RUN touch /root/.ssh/known_hosts
# ARG SSH_KNOWN_HOST
# RUN ssh-keyscan ${SSH_KNOWN_HOST} >> /root/.ssh/known_hosts

# ARG REPO_URL_CC_LIBS
# ARG VERSION_CC_LIBS
# RUN git clone --branch ${VERSION_CC_LIBS} ${REPO_URL_CC_LIBS} /opt/marketplace-shared-lib/
#
# ARG REPO_URL_CC_MODELS_PG
# ARG VERSION_CC_MODELS_PG
# RUN git clone --branch ${VERSION_CC_MODELS_PG} ${REPO_URL_CC_MODELS_PG} /opt/campuscom-shared-models/
#
# ARG REPO_URL_CC_MODELS_MONGO
# ARG VERSION_CC_MODELS_MONGO
# RUN git clone --branch ${VERSION_CC_MODELS_MONGO} ${REPO_URL_CC_MODELS_MONGO} /opt/marketplace-shared-models/

COPY . .

RUN pip install -r requirements.txt

FROM python:3.7-slim AS build-image
COPY --from=compile-image /opt/venv /opt/venv
COPY --from=compile-image /opt/app /opt/app
COPY --from=compile-image /opt/app/docker-entrypoint.sh /usr/local/bin
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

WORKDIR /opt/app
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 5432
EXPOSE 5000
# CMD ["gunicorn", "--workers=3", "--threads=6", "--worker-class=gthread", "--chdir=/opt/app/admin_api", "-b", ":5000", "--log-level=info", "app.wsgi:application"]

CMD ["docker-entrypoint.sh"]

ENV PYTHONUNBUFFERED=1
