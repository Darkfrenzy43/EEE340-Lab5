.data

true_string: .asciiz "true"
false_string: .asciiz "false"
    
string_0: .asciiz "Negative of 10 is "
string_1: .asciiz "Testing parens, subtraction and integer negation...\n"
string_2: .asciiz "10 + (-3) = "

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
sw     $t0 0($sp) 
addiu  $sp $sp -4 
li     $t0 3
neg    $t0, $t0 

lw     $s1 4($sp) 
add    $t0 $s1 $t0 
addiu  $sp $sp 4

move   $a0 $t0
li     $v0 1
syscall


halt:

li $v0 10
syscall
