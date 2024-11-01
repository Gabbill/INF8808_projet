FROM python:3.12-slim as build

WORKDIR /app

COPY build_requirements.txt .

RUN echo pip install pyproj

RUN pip install -r build_requirements.txt

COPY src .

RUN python ./generate_visualizations.py

FROM python:3.12-slim as production

WORKDIR /app

COPY prod_requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r prod_requirements.txt


COPY --from=build /app/server.py .
COPY --from=build /app/app.py .
COPY --from=build /app/app_layout.py .
COPY --from=build /app/json ./json

COPY --from=build app/assets/fonts /app/assets/fonts
COPY --from=build app/assets/fonts.css /app/assets/
COPY --from=build app/assets/style.css /app/assets/
COPY --from=build app/assets/favicon.ico /app/assets/

EXPOSE 8050

CMD ["gunicorn", "--bind", "0.0.0.0:8050", "server:create_app()"]