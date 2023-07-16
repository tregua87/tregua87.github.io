---
title: "The evidence beyond the wall: Memory forensics in SGX environments"
collection: publications
permalink: /publication/2021-12-sgxforensic
excerpt:
date: "Dec 2021"
venue: "Forensic Science International: Digital Investigation"
paperurl: https://www.flaviotoffalini.info/files/sgx-forensic.pdf
citation:
---

**Authors:** **Flavio Toffalini**, Andrea Oliveri, Mariano Graziano, Jianying Zhou, Davide Balzarotti

**Abstract:**
Software Guard eXtensions (SGX) is a hardware-based technology that introduces unobservable portions of memory, called enclaves, that physically screens software components from system tampering. Enclaves can be used to run arbitrary programs (including malicious code), but their actual impact on digital forensics and incident response remains unknown. In our work, we propose a methodical study of what information can be retrieved from an SGX machine and how to use this information to infer the enclaves interfaces and structure layout.

We tested our techniques over a dataset of 45 SGX applications and we showed the practicality of our techniques in a real-product use-case and on two malware-enclaves.

[Download paper here](https://www.flaviotoffalini.info/files/sgx-forensic.pdf)

[PoC](https://github.com/tregua87/sgx-forensic)
