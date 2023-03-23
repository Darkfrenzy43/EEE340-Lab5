.data

true_string: .asciiz "true"
false_string: .asciiz "false"
    
string_2: .asciiz "\n"
string_5: .asciiz "done"

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


li     $t0 1
beqz   $t0 endif_0
li     $t0 1
move   $a0 $t0
li     $v0 1
syscall

b endelse_1
endif_0:

endelse_1:

la     $t0 string_2
move   $a0 $t0
li     $v0 4
syscall

li     $t0 0
beqz   $t0 endif_3
li     $t0 99
move   $a0 $t0
li     $v0 1
syscall

b endelse_4
endif_3:

endelse_4:

la     $t0 string_5
move   $a0 $t0
li     $v0 4
syscall


halt:

li $v0 10
syscall
