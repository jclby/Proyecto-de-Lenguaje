# ─────────────────────────────────────────────────────────────────────────
# Sistema de Seleccion de Personal - Imagen unica con Scala + Python + Prolog
# ─────────────────────────────────────────────────────────────────────────
FROM eclipse-temurin:17-jdk-jammy

ENV DEBIAN_FRONTEND=noninteractive

# ── Dependencias de sistema: Python, SWI-Prolog, curl/gnupg para el repo de sbt
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv \
        swi-prolog \
        curl gnupg ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# ── Instalar sbt
RUN echo "deb https://repo.scala-sbt.org/scalasbt/debian all main" | tee /etc/apt/sources.list.d/sbt.list \
    && curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | gpg --dearmor | tee /etc/apt/trusted.gpg.d/sbt.gpg > /dev/null \
    && apt-get update \
    && apt-get install -y --no-install-recommends sbt \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ── Copiar el proyecto completo
COPY . .

# ── Dependencias Python (capa web)
RUN pip3 install --no-cache-dir -r web/requirements.txt

# ── Precalentar sbt: descarga dependencias (circe) y compila, para que un
#    "Recalcular" en produccion no tenga que bajar internet la primera vez
RUN cd scala && sbt compile || true

EXPOSE 8080

# gunicorn sirve web/app.py; $PORT lo inyecta la plataforma (Render/Railway/Fly)
CMD ["sh", "-c", "cd web && gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 2 --timeout 300 app:app"]
