addi s1, s2, 5
addi t0, zero, 100
addi sp, sp, -8
lw a0, 20(s1)
lw ra, 0(sp)
lw t1, 4(s0)
sltiu s1, s2, 10
sltiu a0, t0, 255
jalr ra, t1, 0
jalr zero, ra, 0
sw ra, 32(sp)
sw s1, 0(s0)
sw a0, 4(sp)