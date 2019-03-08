# example line count
```
a_example.txt
     5  H 2 garden cat
b_lovely_landscapes.txt
 80001  H 15 tc3bj tt8d8 t01c1 tnmg2 t1sv4 t79wk tz3c1 t80n9 t6v7z tgw34 ts517 tdzn5 t7lh7 tx33s tpm7q
c_memorable_moments.txt
  1001  V 5 tpc t4q t3j1 t031 tqx
d_pet_pictures.txt
 90001  V 14 tz5 tx2 t02 tb5 t34 tq1 tl5 tl2 tb2 tp6 tp2 t25 tx1 t94
e_shiny_selfies.txt
 80001  V 23 tz9 twg tdg t19 tdf tw7 t28 t7c td2 tn2 t87 tp4 tx4 t8f t4d t9 tkd th2 tmh tl4 t4c t66 tnh
```

# scores
a: 2
b: 205509
c: 524
d: 91415
e: 6711
   304161

# input file info


| name                    | score  | tag count | slide count | slide/tag          | tag/slide         |
|-------------------------|--------|-----------|-------------|--------------------|-------------------|
| b_lovely_landscapes.txt | 12     | 840000    | 80000       | 1.7142857142857142 | 18.0              |
| c_memorable_moments.txt | 112    | 1559      | 750         | 3.04746632456703   | 6.334666666666666 |
| d_pet_pictures.txt      | 133588 | 220       | 60000       | 1575.0272727272727 | 5.7751            |
| e_shiny_selfies.txt     | 58408  | 500       | 40000       | 58.274             | 0.728425          |


# results 

gereedy 5m for 10k ~ 30m for 60k
not gereedy 2m for 50 ~ 2400m for 60k
naive n**2 14s for 50 ~ 280m for 60k
only one tag cmp 25s for 200 ~ 125m for 60k

some orderedHashSet usage 50s for 2k ~ 259s for 60k, score: 91415

# time for popping ))
## without popping

score: 205887
6.61user 0.45system 0:07.11elapsed 99%CPU (0avgtext+0avgdata 348104maxresident)k
232inputs+8outputs (0major+98195minor)pagefaults 0swaps

## with popping
score: 205620
8.90user 0.62system 0:10.14elapsed 93%CPU (0avgtext+0avgdata 359904maxresident)k
240inputs+8outputs (0major+101128minor)pagefaults 0swaps

