# Usa l'immagine di base di Python
FROM python:3.9

RUN pip install --upgrade pip

# Imposta la directory di lavoro
WORKDIR /app

# Copia il file requirements.txt nella directory di lavoro
COPY requirements.txt /app/

# Installa le dipendenze
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y postgresql-client

# Copia il resto del codice nella directory di lavoro
COPY . /app


COPY wait-for.sh .
RUN chmod +x wait-for.sh
EXPOSE 8001
# RUN python3 trascendence/manage.py migrate
# Imposta le variabili d'ambiente per Django


# Avvia il server Django
# CMD [ "./wait-for.sh", "db", "5432", "--", "python", "trascendence/manage.py", "runserver", "0.0.0.0:9000"]
# CMD [ "./wait-for.sh", "db", "5432", "--", "python", "trascendence/manage.py", "migrate", "runserver", "0.0.0.0:9000"]
# CMD [ "./wait-for.sh", "db", "5432", "--", "python3", "trascendence/manage.py", "migrate", "&&", "python3", "trascendence/manage.py", "runserver", "0.0.0.0:9000"]
# CMD ["./wait-for.sh", "db", "5432", "--", "sh", "-c", "python trascendence/manage.py migrate && python trascendence/manage.py runserver 0.0.0.0:9000"]
CMD until PGPASSWORD=$POSTGRES_PASSWORD psql -h db -U $POSTGRES_DB -d $POSTGRES_USER -c '\q'; do echo "Postgres is unavailable - sleeping"; sleep 1; done && python3 trascendence/manage.py makemigrations && python3 trascendence/manage.py migrate && python3 trascendence/manage.py runserver 0.0.0.0:8001

