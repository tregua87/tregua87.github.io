---
title: "SnakeGX: a sneaky attack against SGX Enclaves"
collection: publications
permalink: /publication/2021-06-snakegx
excerpt:
date: "June 2021"
venue: "19th International Conference on Applied Cryptography and Network Security"
paperurl: https://www.flaviotoffalini.info/files/snakegx.pdf
citation:
---

**Authors:** **Flavio Toffalini**, Mariano Graziano, Mauro Conti, Jianying Zhou

**Abstract:**
Intel Software Guard eXtension (SGX) is a technology to create enclaves (i.e., trusted memory regions) hardware isolated from a compromised operating system. Recently, researchers showed that unprivileged adversaries can mount code-reuse attacks to steal secrets from enclaves.
However, modern operating systems can use memory-forensic techniques to detect their traces. To this end, we propose SnakeGX, an approach that allows stealthier attacks with a minimal footprint; SnakeGX is a framework to implant a persistent backdoor in legitimate enclaves.
Our solution encompasses a new architecture specifically designed to overcome the challenges SGX environments pose, while preserving their integrity and functionality.
We thoroughly evaluate SnakeGX against StealthDB, which demonstrates the feasibility of our approach.

[Download paper here](https://www.flaviotoffalini.info/files/snakegx.pdf)

[PoC](https://github.com/tregua87/snakegx/)
