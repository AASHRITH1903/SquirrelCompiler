.data
	arr__2:
		.word 0, 0, 0, 0

.text
.globl main

main:

move $s8, $sp

li $t0, 1
addi $t1, $t0, 0
li $t2, 1
addi $t3, $t2, 0
_L13:
li $t4, 4
sub $t5, $t3, $t4
ble $t5, $zero, _L14
j _L11
_L14:
mult $t3, $t5
mflo $t5
mult $t5, $t6
mflo $t6
li $t7, 1
add $s0, $t3, $t7
addi $s1, $s0, 0
sw $s1, arr__2($t6)
mult $t1, $t3
mflo $s2
addi $t1, $s2, 0
li $v0, 1
move $a0, $t3
syscall
li $s3, 1
add $s4, $t3, $s3
addi $t3, $s4, 0
j _L13
_L11:
li $v0, 1
move $a0, $t1
syscall
move $sp, $s8
jr $ra

