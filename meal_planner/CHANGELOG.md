# Wijzigingen

## 0.1.2

- Het eigen AppArmor-profiel blokkeerde nginx. Dat profiel is verwijderd en nginx start als root met tijdelijke bestanden in /tmp.

## 0.1.1

- Nginx schrijft tijdelijke bestanden naar /tmp, zodat de app niet meer herstart met een 502.

## 0.1.0

- Eerste app met Ingress, SQLite en Nederlandse huishoudinstellingen.
- Interne API voorbereid voor de latere Home Assistant-integration.
