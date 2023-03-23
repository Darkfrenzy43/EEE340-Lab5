.data

true_string: .asciiz "true"
false_string: .asciiz "false"
    
string_0: .asciiz "Testing multiplication...\n"
string_1: .asciiz "30 * 70 = "
string_2: .asciiz "\n\n"
string_3: .asciiz "Testing division...\n"
string_4: .asciiz "99 / 33 = "
string_5: .asciiz "\n\n"

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

la     $t0 string_1
move   $a0 $t0
li     $v0 4
syscall

li     $t0 30
sw     $t0 0($sp) 
addiu  $sp $sp -4 
li     $t0 70
lw     $s1 4($sp) 
mul    $t0 $s1 $t0 
addiu  $sp $sp 4

move   $a0 $t0
li     $v0 1
syscall

la     $t0 string_2
move   $a0 $t0
li     $v0 4
syscall

la     $t0 string_3
move   $a0 $t0
li     $v0 4
syscall

la     $t0 string_4
move   $a0 $t0
li     $v0 4
syscall

li     $t0 99
sw     $t0 0($sp) 
addiu  $sp $sp -4 
li     $t0 33
lw     $s1 4($sp) 
div    $t0 $s1 $t0 
addiu  $sp $sp 4

move   $a0 $t0
li     $v0 1
syscall

la     $t0 string_5
move   $a0 $t0
li     $v0 4
syscall


halt:

li $v0 10
syscall
