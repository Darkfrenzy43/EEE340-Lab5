"""
Given a global scope and type annotations, and operating as an ANTLR
listener over a semantically-correct Nimble parse tree, generates equivalent
MIPS assembly code. Does not consider function definitions, function calls,
or return statements.

Authors: TODO: Your names here
Date: TODO: Submission date here

Instructor version: 2023-03-15
"""

import templates
from nimble import NimbleListener, NimbleParser
from semantics import PrimitiveType


class MIPSGenerator(NimbleListener):

    def __init__(self, global_scope, types, mips):
        self.current_scope = global_scope
        self.types = types
        self.mips = mips
        self.label_index = -1
        self.string_literals = {}


    def unique_label(self, base):
        """
        Given a base string "whatever", returns a string of the form "whatever_x",
        where the x is a unique integer. Useful for generating unique labels.
        """
        self.label_index += 1
        return f'{base}_{self.label_index}'

    # ---------------------------------------------------------------------------------
    # Provided for you
    # ---------------------------------------------------------------------------------

    def enterMain(self, ctx: NimbleParser.MainContext):
        self.current_scope = self.current_scope.child_scope_named('$main')

    def exitScript(self, ctx: NimbleParser.ScriptContext):
        self.mips[ctx] = templates.script.format(
            string_literals='\n'.join(f'{label}: .asciiz {string}'
                                      for label, string in self.string_literals.items()),
            main=self.mips[ctx.main()]
        )

    def exitMain(self, ctx: NimbleParser.MainContext):
        self.mips[ctx] = self.mips[ctx.body()]
        self.current_scope = self.current_scope.enclosing_scope

    def exitBlock(self, ctx: NimbleParser.BlockContext):
        self.mips[ctx] = '\n'.join(self.mips[s] for s in ctx.statement())

    def exitBoolLiteral(self, ctx: NimbleParser.BoolLiteralContext):
        value = 1 if ctx.BOOL().getText() == 'true' else 0
        self.mips[ctx] = 'li     $t0 {}'.format(value)

    def exitIntLiteral(self, ctx: NimbleParser.IntLiteralContext):
        self.mips[ctx] = 'li     $t0 {}'.format(ctx.INT().getText())

    def exitStringLiteral(self, ctx: NimbleParser.StringLiteralContext):
        label = self.unique_label('string')
        self.string_literals[label] = ctx.getText()
        self.mips[ctx] = 'la     $t0 {}'.format(label)

    def exitPrint(self, ctx: NimbleParser.PrintContext):
        """
        Bool values have to be handled separately, because we print 'true' or 'false'
        but the values are encoded as 1 or 0
        """
        if self.types[ctx.expr()] == PrimitiveType.Bool:
            self.mips[ctx] = templates.print_bool.format(expr=self.mips[ctx.expr()])
        else:
            # in the SPIM print syscall, 1 is the service code for Int, 4 for String
            self.mips[ctx] = templates.print_int_or_string.format(
                expr=self.mips[ctx.expr()],
                service_code=1 if self.types[ctx.expr()] == PrimitiveType.Int else 4
            )

    # ---------------------------------------------------------------------------------
    # Partially provided for you - see lab instructions for suggested order
    # ---------------------------------------------------------------------------------

    def exitBody(self, ctx: NimbleParser.BodyContext):
        # TODO: extend to include varBlock
        self.mips[ctx] = self.mips[ctx.block()]

    def exitAddSub(self, ctx: NimbleParser.AddSubContext):

        # TODO: extend for String concatenation

        self.mips[ctx] = templates.add_sub_mul_div.format(
            operation='add' if ctx.op.text == '+' else 'sub',
            expr0=self.mips[ctx.expr(0)],
            expr1=self.mips[ctx.expr(1)]
        )

    def exitIf(self, ctx: NimbleParser.IfContext):
        # TODO: extend to support `else`
        self.mips[ctx] = templates.if_.format(
            condition=self.mips[ctx.expr()],
            true_block=self.mips[ctx.block(0)],
            endif_label=self.unique_label('endif')
        )

    # ---------------------------------------------------------------------------------
    # Yours to implement - see lab instructions for suggested order
    # ---------------------------------------------------------------------------------

    def exitVarBlock(self, ctx: NimbleParser.VarBlockContext):
        pass

    def exitVarDec(self, ctx: NimbleParser.VarDecContext):
        pass

    def exitAssignment(self, ctx: NimbleParser.AssignmentContext):
        pass

    def exitWhile(self, ctx: NimbleParser.WhileContext):
        pass

    def exitNeg(self, ctx: NimbleParser.NegContext):

        # Unary minus code
        if ctx.op.text == '-':
            self.mips[ctx] = templates.unary_minus.format(expr = self.mips[ctx.expr()]);

    def exitParens(self, ctx: NimbleParser.ParensContext):
        self.mips[ctx] = self.mips[ctx.expr()]

    def exitCompare(self, ctx: NimbleParser.CompareContext):
        pass

    def exitVariable(self, ctx: NimbleParser.VariableContext):
        pass

    def exitMulDiv(self, ctx: NimbleParser.MulDivContext):

        self.mips[ctx] = templates.add_sub_mul_div.format(
            operation = 'mul' if ctx.op.text == '*' else 'div',
            expr0 = self.mips[ctx.expr(0)],
            expr1 = self.mips[ctx.expr(1)]
        )


