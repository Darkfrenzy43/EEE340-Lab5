.data

true_string: .asciiz "true"
false_string: .asciiz "false"
    
string_0: .asciiz "Negative of 10 is "
string_1: .asciiz "\n\nTesting parens, subtraction and integer negation...\n"
string_2: .asciiz "10 + (-3) = "
string_3: .asciiz "\n\n\n"
string_4: .asciiz "Testing boolean negation...\n"
string_5: .asciiz "The evaluated value of !true is "
string_6: .asciiz "\n"
string_7: .asciiz "The evaluated value of !!(!false) is "
string_8: .asciiz "\n"

.text

true_false_string:
beq    $t0 $zero choose_false
la     $a0 true_string
j      end_true_false_string
choose_false:
la     $a0 false_string
end_true_false_string:
jr     $ra

main: 

move $fp $sp


la     $t0 string_0
move   $a0 $t0
li     $v0 4
syscall

li     $t0 10
neg    $t0, $t0 

move   $a0 $t0
li     $v0 1
syscall

la     $t0 string_1
move   $a0 $t0
li     $v0 4
syscall

la     $t0 string_2
move   $a0 $t0
li     $v0 4
syscall

li     $t0 10
addiu  $sp $sp -4 
sw     $t0 0($sp) 
li     $t0 3
neg    $t0, $t0 

lw     $s1 0($sp) 
add    $t0 $s1 $t0 
addiu  $sp $sp 4

move   $a0 $t0
li     $v0 1
syscall

la     $t0 string_3
move   $a0 $t0
li     $v0 4
syscall

la     $t0 string_4
move   $a0 $t0
li     $v0 4
syscall

la     $t0 string_5
move   $a0 $t0
li     $v0 4
syscall

li     $t0 1
li     $s1 1
xor    $t0, $s1, $t0

jal    true_false_string
li     $v0 4
syscall

la     $t0 string_6
move   $a0 $t0
li     $v0 4
syscall

la     $t0 string_7
move   $a0 $t0
li     $v0 4
syscall

li     $t0 0
li     $s1 1
xor    $t0, $s1, $t0

li     $s1 1
xor    $t0, $s1, $t0

li     $s1 1
xor    $t0, $s1, $t0

jal    true_false_string
li     $v0 4
syscall

la     $t0 string_8
move   $a0 $t0
li     $v0 4
syscall


halt:

li $v0 10
syscall
