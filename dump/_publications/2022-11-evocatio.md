---
title: "Evocatio: Conjuring Bug Capabilities from a Single PoC"
collection: publications
permalink: /publication/2022-11-evocatio
excerpt:
date: "Nov 2022"
venue: "ACM SIGSAC Conference on Computer and Communications Security"
paperurl: https://www.flaviotoffalini.info/files/evocatio.pdf
citation:
---

**Authors:** Zhiyuan Jiang, Shuitao Gan, Adrian Herrera, **Flavio Toffalini**, Lucio Romerio, Chaojing Tang, Manuel Egele, Chao Zhang, Mathias Payer

**Abstract:** The popularity of coverage-guided greybox fuzzers has led to a tsunami of security-critical bugs that developers must prioritize and fix. Knowing the capabilities a bug exposes (e.g., type of vulnerability, number of bytes read/written) enables prioritization of bug fixes. Unfortunately, understanding a bug's capabilities is a timeconsuming process, requiring (a) an understanding of the bug's root cause, (b) an understanding how an attacker may exploit the bug, and (c) the development of a patch mitigating these threats. This is a mostly-manual process that is qualitative and arbitrary, potentially leading to a misunderstanding of the bug’s capabilities.  
Evocatio automatically discovers a bug's capabilities. Evocatio analyzes a crashing test case (i.e., an input exposing a bug) to understand the full extent of how an attacker can exploit a bug. Evocatio leverages a capability-guided fuzzer to efficiently uncover new bug capabilities (rather than only generating a single crashing test case for a given bug, as a traditional greybox fuzzer does).  
We evaluate Evocatio on 38 bugs (34 CVEs and four bug reports) across eight open-source applications. From these bugs, Evocatio: (i) discovered 10× more capabilities (that is, the number of unique capabilities induced by a set of crashes was 10× higher) than AFL++'s crash exploration mode; (ii) converted 19 of the 38 bugs to new bug types (demonstrating the limitations of manual qualitative analysis); and (iii) generated new proof-of-concept (PoC) test cases violating patches for 7 out of 16 tested CVEs, one of which still triggers in the latest version of the software.

[Artifact](https://github.com/HexHive/Evocatio)

[Download paper here](https://www.flaviotoffalini.info/files/evocatio.pdf)