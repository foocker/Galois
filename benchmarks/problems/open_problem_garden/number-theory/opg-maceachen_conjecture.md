---
id: opg-maceachen_conjecture
title: MacEachen Conjecture
status: open
difficulty: graduate
domains:
- Number Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/maceachen_conjecture
---

# Statement

Conjecture Every odd prime number must either be adjacent to, or a prime distance away from a primorial or primorial product.

# Source literature


# Progress

- This conjecture speaks to the distribution of all prime numbers, relating them to primorials. Recall that the primorials are simply the consecutive product of prime numbers eg 2,2*3,2*3*5, etc. this is OEIS A002110 {2,6,30,210,30030,...}. A new sequence A129912, related to the conjecture, ie A129912 and combines A002110 with the products of unique primorials eg 2*6,2*30,6*30, etc. The PariGP code to generate the terms is on the author's wiki site. By unique, the products mentioned would not use an entry of A002110 more than once. A numerical example is candidate number N=189239. This cannot be prime unless it is an absolute prime distance from a sequence term covering the range 0 thru 2*N. of course, it is 9059 away from sequence entry 180180, and so it may be prime (and it is). Note that the conjecture treats a required but not sufficient condition for primality. As it works for offset distance less than the candidate it could be used in a primality method if that somehow could be applied effectively (seriously doubtful). However, the insight provided into the distribution of the primes is the worthwhile part. It leaves no doubt about the non random, concrete structure of prime interdependency.

Note that the conjecture implies as others have suspected, the existence of Twin primes to be found adjacent to sequence terms. Note that the conjecture was independently confirmed through the first 50 million primes. Also, the author has attempted a strict proof, that is conditional upon Goldbach's Conjecture being true. Realizing that the author is merely an amateur hobbiest, the proof may be flawed but it can be supplied, it is quite elementary, less than a page.

I do note the independent work of several others found online, all of whom I do not personally know . One is John Sokol, who in 2002 made the following conjecture (incorrect is as far as the distance being < the candidate, think it breaks down around 331). I independently started with this same conjecture until I quickly realized the correct one. I also note the work of Bob Potter and his primorial conjecture at the link shown lower. A third person is Hank Harrell, who has done work in an area similar to Potter's.

The author plotted a normalized minimum offset seen at the primes, with the resulting scatter plot clearly indicating an asymptotic trend towards the relevant sequence entry being one greater than the prime candidate.

The author has also speculated that the A129912 sequence is useful in locating Twin Primes (not his particular interest). An earlier conjecture by the author in 2006 (A117825) concerning highly composite numbers basically parallels Fortune's conjecture (A005325).

The links mentioned above are now listed: OEIS 2110 OEIS 129912 author's wiki Wikipedia PlanetMath Harrell WikiCommons

Sokol's conjecture (sic): A primes can only exists + or - a prime from a primorial. Where 1 is considered a prime and 2 is not.

Sokol

Potter conjecture:

"All prime numbers in the vicinity of a primorial (or primorial multiple) will combine to make a Goldbach pair for the primorial. The length of sequence for which this effect holds increases as the value of the primorial or primorial multiple increases."

Potter

Many more online resources were accessed for this work, some of them are:

Pari-GP program Chris Caldwell's well respected site Dario Alpern's online ECM calculator

I am sure there are others I have forgotten.
