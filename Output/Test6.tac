start:
params 0

int a`2[36]
a`2[0] = 1
a`2[4] = 2
a`2[8] = 3
a`2[12] = 4
a`2[16] = 5
a`2[20] = 6
a`2[24] = 7
a`2[28] = 8
a`2[32] = 9

#L8:
int b`2[36]
b`2[0] = -1
b`2[4] = 2
b`2[8] = -3
b`2[12] = 4
b`2[16] = -4
b`2[20] = 6
b`2[24] = -11
b`2[28] = 8
b`2[32] = -10

#L6:
int c`2[36]
c`2[0] = 0
c`2[4] = 0
c`2[8] = 0
c`2[12] = 0
c`2[16] = 0
c`2[20] = 0
c`2[24] = 0
c`2[28] = 0
c`2[32] = 0

#L4:
~t0 = 0

i`3 = (int) ~t0

#L13:

~t1 = 9

if i`3 < ~t1 goto #L14
goto #L11

#L14:


~t5 = 3

~t4 = i`3 / ~t5

p`3 = (int) ~t4

#L23:

~t7 = 3

~t6 = i`3 % ~t7

q`3 = (int) ~t6

#L21:

~t8 = p`3 * 3
~t9 = q`3 * 1
~t10 = ~t8 + ~t9

~t11 = ~t10 * 4


~t12 = p`3 * 3
~t13 = q`3 * 1
~t14 = ~t12 + ~t13

~t15 = ~t14 * 4
~t16 = a`2[~t15]


~t17 = p`3 * 3
~t18 = q`3 * 1
~t19 = ~t17 + ~t18

~t20 = ~t19 * 4
~t21 = b`2[~t20]

~t22 = ~t16 + ~t21

~t23 = (int) ~t22
c`2[~t11] = ~t23

#L19:

~t24 = p`3 * 3
~t25 = q`3 * 1
~t26 = ~t24 + ~t25

~t27 = ~t26 * 4
output int, c`2[~t27]

#L17:
~t28 = (string) "\n"
output string, ~t28

#L15:


~t2 = 1

~t3 = i`3 + ~t2

i`3 = ~t3

goto #L13
#L11:

#L10:
return 

#L1: