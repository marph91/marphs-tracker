## Overview

From https://github.com/Xinyuan-LilyGO/LilyGo-T-SIM7080G-MicroPython:

> SIM7080G supports NB-IoT and Cat-M in global frequency bands, but does not support 2G/3G/4G. Please confirm that the SIM card used supports NB-IoT or Cat-M before use.

Cat-M is a sub category of LTE-M. See https://en.wikipedia.org/wiki/LTE-M#3GPP_Narrowband_Cellular_Standards. For simplicity, they are not differentiated here.

| Plan                                  | Initial Cost      | Basic Fee   | Price     | Billing Unit | Remark                              |
| ------------------------------------- | ----------------- | ----------- | --------- | ------------ | ----------------------------------- |
| Soracom plan01s                       | -                 | $0.06/day   | $0.02/MB  | 1 KB         | [1], [2]                            |
| Soracom plan01s Low Data Volume (LDV) | -                 | $0.40/month | $0.50/MB  | 1 kB         | LTE Cat-M1 and NB-IoT not available |
| Things Mobile                         | -                 | $1.00/month | $0.12/MB  | 1 KB         |                                     |
| DPTechnics                            | 9.95 € for 250 MB | -           | -         | 1 KB         | Soracom card, 1 year valid          |
| simHERO                               | 22.00 €           | €0.20/month | €0.15/MB  | 1 KB         | [3]                                 |
| Vodafone CallYa Classic               | -                 | €0/month    | €0.03/MB  | **1 MB**     |                                     |
| KPN Horse Watch Prepaid IoT SIM – EU  | 12.50 € for 1 GB  | -           | -         | ?            | 1 year valid                        |
| Simbase Global IoT                    | $5                | €0.01/day   | €0.005/MB | ?            |                                     |

[1] https://developers.soracom.io/en/docs/network-connectivity/supported-carriers/#plan01s
[2] https://developers.soracom.io/en/docs/billing-pricing/pricing-fee-schedule/
[3] https://revierbedarf.at/products/multi-sim-karte

## Considerations

There are good and cheap NB-IoT SIM cards available - for business customers. [1NCE](https://www.1nce.com/en-eu/1nce-connect/pricing), [simbase](https://simbase.com/de/best-iot-sim-card/germany), [Soracom](https://soracom.io/global-iot-sim/) to name a few.

For private customers, I found only two options:

1. [Things Mobile](https://www.thingsmobile.com/) with 0.10 € per MB. The big advertisement is "no fixed monthly costs, no minimum quantities and no surprises". But in the details "For every account, a monthly fee of €3.00 is charged for use of the IoT Portal.". Well, no.
2. [DPTechnics](https://shop.dptechnics.com/home/1-250mb-worldwide-m2m-sim.html). 9.95 € with 250 MB included for a year. That was good enough for me. But for buying, you need to provide pictures of you and your ID card. I didn't want to do that.

## First try - Vodafone SIM

Last resort: Trying a usual SIM card from Otelo. They usually specify to work with LTE, but not explicitly with **LTE-M**. It just worked! Otelo uses the Vodafone net, so I just looked for a good Vodafone prepaid SIM and found it: Vodafone CallYa Classic for 0 €, 0 € per month, 0.03 € per MB.

Problem: [They charge not only 0.03 € per MB, but 0.03 € per connection](https://forum.vodafone.de/t5/Ohne-Vertrag-Prepaid-Tarife/Abrechnung-Datenverbindung-CallYa-Classic/td-p/3249132). So I burned 5 € just for sending 166 separate small HTTP requests.

## Second try - Simbase SIM

Searching for other options at the Traccar forum, there is [this thread](https://www.traccar.org/forums/topic/iot-sim-for-europa-for-private-use/) that suggests a Simbase SIM. That finally works and has a reasonable pricing. Thanks for the hint!
