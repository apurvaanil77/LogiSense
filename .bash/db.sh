docker run -d \
  --name postgres \
  -e POSTGRES_USER=root \
  -e POSTGRES_PASSWORD=root \
  -e POSTGRES_DB=logisense \
  -p 5432:5432 \
  postgres:17
