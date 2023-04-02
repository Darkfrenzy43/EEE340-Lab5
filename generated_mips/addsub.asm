.data

true_string: .asciiz "true"
false_string: .asciiz "false"
    
string_0: .asciiz "22 - 15 + 4 = "

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

li     $t0 22
addiu  $sp $sp -4 
sw     $t0 0($sp) 
li     $t0 15
lw     $s1 0($sp) 
sub    $t0 $s1 $t0 
addiu  $sp $sp 4

addiu  $sp $sp -4 
sw     $t0 0($sp) 
li     $t0 4
lw     $s1 0($sp) 
add    $t0 $s1 $t0 
addiu  $sp $sp 4

move   $a0 $t0
li     $v0 1
syscall


halt:

li $v0 10
syscall
