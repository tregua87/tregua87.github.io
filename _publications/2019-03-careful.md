---
title: "Careful-Packing: A Practical and Scalable Anti-Tampering Software Protection enforced by Trusted Computing"
collection: publications
permalink: /publication/2019-03-careful
excerpt:
date: "March 2019"
venue: 'The 9th ACM Conference on Data and Application Security and Privacy'
paperurl: 'https://dl.acm.org/citation.cfm?id=3300029'
citation:
---

**Authors:** **Flavio Toffalini**, Mart&iacute;n Ochoa, Jun Sun, Jianying Zhou

**Abstract:**  
Ensuring the correct behaviour of an application is a critical security issue. One of the most popular ways to modify the intended behaviour of a program is to tamper its binary. Several solutions have been proposed to solve this problem, including trusted computing and anti-tampering techniques. Both can substantially increase security, and yet both have limitations. In this work, we propose an approach which combines trusted computing technologies and anti-tampering techniques, and that synergistically overcomes some of their inherent limitations. In our approach critical software regions are protected by leveraging on trusted computing technologies and cryptographic packing, without introducing additional software layers. To illustrate our approach we implemented a secure monitor which collects user activities, such as keyboard and mouse events for insider attack detection. We show how our solution provides a strong anti-tampering guarantee with a low overhead: around 10 lines of code added to the entire application, an average execution time overhead of 5.7% and only 300KB of memory allocated for the trusted module.

[Download paper here](https://dl.acm.org/citation.cfm?id=3300029)

[Slides](https://www.slideshare.net/FlavioToffalini/careful-packing)
