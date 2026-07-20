# Guía de Deploy (Render / Railway / Fly.io)

Este proyecto ahora incluye un `Dockerfile` en la raíz que arma una sola
imagen con **JDK 17 + sbt + Python 3 + SWI-Prolog**, y sirve la app Flask
con **gunicorn**. Con eso el dashboard funciona desde el arranque (usa el
`data/salida/puntajes.json` que ya viene calculado), y si alguien hace clic
en "Recalcular" el pipeline completo (Scala → Python → Prolog) también corre
dentro del mismo contenedor.

## 0. Requisito único: sube el proyecto a GitHub

Todas estas plataformas despliegan desde un repo. Si aún no tienes uno:

```bash
cd "Proyecto Lenguaje de Programacion"
git init
git add .
git commit -m "Deploy: Dockerfile + gunicorn"
gh repo create seleccion-personal --public --source=. --push
# o crea el repo en github.com y haz git remote add origin <url> && git push
```

## 1. Probar el build localmente (recomendado antes de desplegar)

```bash
docker build -t seleccion-personal .
docker run -p 8080:8080 seleccion-personal
# abre http://localhost:8080
```

No pude ejecutar `docker build` en este entorno (el sandbox donde te ayudo
no tiene Docker ni red), así que te recomiendo correr esto en tu máquina
antes de desplegar, para detectar cualquier detalle antes de subirlo.

## 2. Desplegar en Render (más simple, tiene free tier con Docker)

1. Ve a https://dashboard.render.com → **New +** → **Web Service**
2. Conecta tu repo de GitHub
3. Render detecta el `Dockerfile` automáticamente (Environment: Docker)
4. Deja el **Instance Type** en Free o Starter
5. No necesitas configurar variables de entorno; el `Dockerfile` ya lee `$PORT`
6. Click **Create Web Service** — el primer build tarda ~5-8 min (descarga JDK/sbt/dependencias Scala)

## 3. Alternativa: Railway

1. https://railway.app → **New Project** → **Deploy from GitHub repo**
2. Railway detecta el Dockerfile solo
3. En **Settings → Networking**, genera un dominio público
4. Railway inyecta `$PORT` automáticamente, no hace falta configurarlo

## 4. Alternativa: Fly.io

```bash
flyctl launch --no-deploy   # detecta el Dockerfile, genera fly.toml
# en fly.toml, confirma: internal_port = 8080
flyctl deploy
```

## Notas importantes

- **Primer build lento**: sbt descarga las dependencias de Circe la primera
  vez (~1-2 min). El Dockerfile ya corre `sbt compile` durante el build para
  cachear eso en la imagen, así que "Recalcular" en producción no debería
  tener que bajar nada de internet.
- **Plan gratuito y "cold starts"**: en el free tier de Render, el servicio
  se duerme tras 15 min sin tráfico; el primer request tras dormir tarda
  varios segundos.
- **Timeout de "Recalcular"**: ese botón ejecuta `sbt run` + Python + swipl
  de forma síncrona, puede tardar 20-40s. El `Dockerfile` ya configura
  `gunicorn --timeout 300` para que no se corte. Si tu plataforma tiene su
  propio timeout de proxy más corto (algunas rutas free de 30s), el request
  podría cortarse igual — para la demo, el dashboard ya carga con datos
  precalculados sin necesitar tocar ese botón.
- **Persistencia**: si usas "+ Candidato" / "+ Puesto" / "Recalcular", los
  cambios se escriben dentro del contenedor. En Render/Railway/Fly, el
  filesystem de un contenedor **no es persistente entre deploys** (se
  reinicia con cada redeploy). Para una demo puntual no es problema; para
  uso real habría que mover `data/` a un volumen o base de datos.
- Variable opcional `FLASK_DEBUG=1` si necesitas debug del servidor (no
  recomendado en producción).
