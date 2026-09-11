## Options

- https://www.idealo.de/preisvergleich/Liste/111758360/18650-mit-schutzschaltung.html:
  - https://www.idealo.de/preisvergleich/OffersOfProduct/202736142_-inr18650-35e-3500mah-3-6v-samsung.html
  - https://www.idealo.de/preisvergleich/OffersOfProduct/206289328_-inr18650-m35a-3500mah-molicel.html

## Power Consumption

**Rough estimate**

| Activity                   | Current | Typical Duration |            Energy |
| -------------------------- | ------: | ---------------: | ----------------: |
| Deep sleep                 |  1.1 mA |           3590 s |          1.10 mAh |
| ESP32-S3 wake              |   50 mA |              2 s |         0.028 mAh |
| WiFi scan                  |  100 mA |              5 s |         0.139 mAh |
| GNSS fix                   |   52 mA |             30 s |         0.433 mAh |
| GNSS timeout               |   52 mA |            120 s |          1.73 mAh |
| Cellular data transmission |  110 mA |             10 s |         0.306 mAh |
| Full cycle — WiFi home     |       — |      ~7 s active | ~0.17 mAh + sleep |
| Full cycle — WiFi + data   |       — |     ~17 s active | ~0.47 mAh + sleep |
| Full cycle — GNSS + data   |       — |     ~47 s active | ~1.91 mAh + sleep |

Assuming a 3450 mAh battery:

| Mode       | Interval | Expected cycles/day | Estimated battery life |
| ---------- | -------: | ------------------: | ---------------------: |
| Home       |   30 min |                  48 |              ~101 days |
| Away, WiFi |   10 min |                 144 |               ~37 days |
| Away, GNSS |   10 min |                 144 |               ~25 days |
