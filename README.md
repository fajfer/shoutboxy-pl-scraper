<div align="center">
<img width="460" src="https://raw.githubusercontent.com/fajfer/shoutboxy-pl-scraper/main/assets/logo.jpg">
</div>

# Shoutboxy.pl scraper #

Ten "scraper" to mały skrypt w Pythonie pozwalający na odbieranie wiadomości z wybranego shoutboxa ze strony Shoutboxy.pl i przesyłania tych wiadomości dalej poprzez Telegramowego bota i/lub Discordowy Webhook.

## Czego potrzebujemy? ##

- [Dockera](https://docs.docker.com/get-docker/), lub po prostu działającego pythona na naszej maszynie
- [docker-compose](https://docs.docker.com/compose/install/)
- [Bota](https://docs.microsoft.com/en-us/azure/bot-service/bot-service-channel-connect-telegram?view=azure-bot-service-4.0) na Telegramie (potrzebujemy jego token)
- [Webhook](https://discord.com/developers/docs/resources/webhook) na kanale Discordowym (potrzebujemy jego URL)

## Uruchomienie dockera ##

### Budowanie projektu  ###

Zbudowanie projektu polega na uruchomieniu polecenia

```console
docker build --network=host -t fajfer/shoutboxy-pl-scraper:latest .
```

### 'Czysty' docker ###

Skrypt można uruchomić jedną linijką, jeżeli nie zależy nam na wygodzie docker-compose

```console
docker run \
  --env SHOUTBOX_URL='<url>' \
  --env GROUPS='<grupy oddzielone przecinkami>' \
  --env BOT_TOKEN='<token>' \
  --env MSG_DELAY='<int>' \
  --volume ./history:/app/history \
  fajfer/shoutboxy-pl-scraper:latest
```

### Docker compose ###

Możemy też utrzymywać konfigurację w wygodnym YAMLu i postawić kontener jednym poleceniem

```console
docker-compose up -d
```

### Zbudowanie obrazu i uruchomienie kontenera za jednym zamachem

Można też zbudować obraz projektu i go uruchomić jednym poleceniem, dzięki docker-compose

```console
docker compose up -d --build
```

## Wyjaśnienie użytych zmiennych ##

Scraper będzie wysyłał aktualizacje poprzez Telegrama i/lub Discorda jeżeli ich zmienne zostaną dostarczone.
Jeżeli oba zestawy zmiennych zostaną dostarczone aktualizacje będą wysyłane i tu i tu.

Zmienne mogą zostać dostarczone przez `docker-compose.yaml`.
Domyślny plik zawiera przykładowy zestaw zmiennych.

### Wymagane zmienne ###

Te zmienne są wymagane niezależnie od tego, czy aktualizacje mają być wysyłane przez Discorda lub Telegrama.

| Nazwa          | Przykład  |  Zastosowanie  |
|----------------|-----------|----------------|
| `SHOUTBOX_URL` | https://www.shoutboxy.pl/shoutbox/get_shouts.php?id=66727&key=906820945&premium=0&_=1659272531592 | Adres URL wybranego shoutboxa |
| `MSG_DELAY`    | 60                         | Zmianna odpowiadająca liczbie sekund zanim zostanie odpytany endpoint `SHOUTBOX_URL` |

### Zmienne dotyczące Telegrama ###

| Nazwa          | Przykład  |  Zastosowanie  |
|----------------|-----------|----------------|
| `GROUPS`       | @wp_pl,@onet_pl            | ID grup na telegramie oddzielonych przecinkami |
| `BOT_TOKEN`    | 000000:AAAAAABBBBBBCCCCCCC | Token, jaki otrzymaliśmy od BotFathera na Telegramie |

### Zmienne dotyczące Discorda ###

| Nazwa          | Przykład  |  Zastosowanie                      |
|----------------|-----------|------------------------------------|
| `WEBHOOKS`     | https://discord.com/api/webhooks/111/AA-BBB-CC | URL Webhooków, można przekazać kila rozdzielonych przecinkami |
| `AVATAR_URL`   | https://shorturl.at/HOVW3                      | Opcjonalny URL do awatara postów |

`AVATAR_URL` jest parametrem opcjonalnym, bez niego aktualizacje będą miały domyślny awatar Webhooka.