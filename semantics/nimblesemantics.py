"""
The nimblesemantics module contains classes sufficient to perform a semantic analysis
of a subset of Nimble programs, not including function definitions, function calls,
and return statements.

Author: Greg Phillips
Version: 2023-03-15

"""
from .errorlog import ErrorLog, Category
from nimble import NimbleListener, NimbleParser
from .symboltable import PrimitiveType, Scope

TYPES = {'Int': PrimitiveType.Int,
         'Bool': PrimitiveType.Bool,
         'String': PrimitiveType.String}


class DefineScopesAndSymbols(NimbleListener):

    def __init__(self, error_log: ErrorLog, global_scope: Scope, types: dict):
        self.error_log = error_log
        self.current_scope = global_scope
        self.type_of = types

    def enterMain(self, ctx: NimbleParser.MainContext):
        self.current_scope = self.current_scope.create_child_scope('$main', PrimitiveType.Void)

    def exitMain(self, ctx: NimbleParser.MainContext):
        self.current_scope = self.current_scope.enclosing_scope

    def enterFuncDef(self, ctx: NimbleParser.FuncDefContext):
        self.error_log.add(ctx, Category.UNSUPPORTED_LANGUAGE_FEATURE,
                           'this implementation does not support function definitions')

    def enterFuncCall(self, ctx: NimbleParser.FuncCallContext):
        self.error_log.add(ctx, Category.UNSUPPORTED_LANGUAGE_FEATURE,
                           'this implementation does not support function calls')

    def enterReturn(self, ctx: NimbleParser.ReturnContext):
        self.error_log.add(ctx, Category.UNSUPPORTED_LANGUAGE_FEATURE,
                           'this implementation does not support return statements')


class InferTypesAndCheckConstraints(NimbleListener):
    """
    The type of each expression parse tree node is calculated and stored in the `types`
    dictionary, using the tree node as the key.

    The types of declared variables are stored in the current Scope object.

    Any semantic errors detected, e.g., undefined variable names,
    type mismatches, etc, are logged in the `error_log`
    """

    def __init__(self, error_log: ErrorLog, global_scope: Scope, types: dict):
        self.error_log = error_log
        self.current_scope = global_scope
        self.type_of = types

    # --------------------------------------------------------
    # Program structure
    # --------------------------------------------------------

    def enterMain(self, ctx: NimbleParser.MainContext):
        self.current_scope = self.current_scope.child_scope_named('$main')

    def exitMain(self, ctx: NimbleParser.MainContext):
        self.current_scope = self.current_scope.enclosing_scope

    # --------------------------------------------------------
    # Variable declarations
    # --------------------------------------------------------

    def log_invalid_assign(self, ctx, var_name):
        self.error_log.add(ctx, Category.ASSIGN_TO_WRONG_TYPE,
                           f"Can't assign {self.type_of[ctx.expr()]} expression to variable"
                           f"{var_name} of type {self.current_scope.resolve(var_name)}")

    def exitVarDec(self, ctx: NimbleParser.VarDecContext):
        var_name = ctx.ID().getText()
        if self.current_scope.resolve_locally(var_name):
            self.error_log.add(ctx, Category.DUPLICATE_NAME,
                               f"Can't redeclare {var_name}; already declared "
                               f"as {self.current_scope.resolve_locally(var_name)}")
        else:
            self.current_scope.define(var_name, TYPES[ctx.TYPE().getText()])
            if ctx.expr() and self.current_scope.resolve(var_name).type != self.type_of[ctx.expr()]:
                self.log_invalid_assign(ctx, var_name)

    # --------------------------------------------------------
    # Statements
    # --------------------------------------------------------

    def exitAssignment(self, ctx: NimbleParser.AssignmentContext):
        var_name = ctx.ID().getText()
        symbol = self.current_scope.resolve(var_name)
        if symbol:
            if symbol.type != self.type_of[ctx.expr()]:
                self.log_invalid_assign(ctx, var_name)
        else:
            self.error_log.add(ctx, Category.UNDEFINED_NAME,
                               f'Assignment target {var_name} not declared')

    def check_boolean_condition(self, ctx, kind):
        if self.type_of[ctx.expr()] != PrimitiveType.Bool:
            self.error_log.add(ctx, Category.CONDITION_NOT_BOOL,
                               f"{kind} condition {ctx.getText()} has type {self.type_of[ctx.expr()]} not Bool")

    def exitWhile(self, ctx: NimbleParser.WhileContext):
        self.check_boolean_condition(ctx, 'While')

    def exitIf(self, ctx: NimbleParser.IfContext):
        self.check_boolean_condition(ctx, 'If')

    def exitPrint(self, ctx: NimbleParser.PrintContext):
        if self.type_of[ctx.expr()] == PrimitiveType.ERROR:
            self.error_log.add(ctx, Category.UNPRINTABLE_EXPRESSION,
                               f"Can't print expression {ctx.getText()} as it has type ERROR")

    # --------------------------------------------------------
    # Expressions
    # --------------------------------------------------------

    def exitIntLiteral(self, ctx: NimbleParser.IntLiteralContext):
        self.type_of[ctx] = PrimitiveType.Int

    def exitNeg(self, ctx: NimbleParser.NegContext):
        if ctx.op.text == '-' and self.type_of[ctx.expr()] == PrimitiveType.Int:
            self.type_of[ctx] = PrimitiveType.Int
        elif ctx.op.text == '!' and self.type_of[ctx.expr()] == PrimitiveType.Bool:
            self.type_of[ctx] = PrimitiveType.Bool
        else:
            self.type_of[ctx] = PrimitiveType.ERROR
            self.error_log.add(ctx, Category.INVALID_NEGATION,
                               f"Can't apply {ctx.op.text} to {self.type_of[ctx.expr()].name}")

    def exitParens(self, ctx: NimbleParser.ParensContext):
        self.type_of[ctx] = self.type_of[ctx.expr()]

    def binary_on_ints(self, ctx, result_type):
        if self.type_of[ctx.expr(0)] == PrimitiveType.Int and self.type_of[ctx.expr(1)] == PrimitiveType.Int:
            self.type_of[ctx] = result_type
        else:
            self.type_of[ctx] = PrimitiveType.ERROR
            self.error_log.add(ctx, Category.INVALID_BINARY_OP,
                               f"Can't apply {ctx.op.text} to {self.type_of[ctx.expr(0)]}"
                               f" and {self.type_of[ctx.expr(1)]}")

    def exitMulDiv(self, ctx: NimbleParser.MulDivContext):
        self.binary_on_ints(ctx, PrimitiveType.Int)

    def exitAddSub(self, ctx: NimbleParser.AddSubContext):
        if (ctx.op.text == '+' and
                self.type_of[ctx.expr(0)] == PrimitiveType.String and
                self.type_of[ctx.expr(1)] == PrimitiveType.String):
            self.type_of[ctx] = PrimitiveType.String
        else:
            self.binary_on_ints(ctx, PrimitiveType.Int)

    def exitCompare(self, ctx: NimbleParser.CompareContext):
        self.binary_on_ints(ctx, PrimitiveType.Bool)

    def exitVariable(self, ctx: NimbleParser.VariableContext):
        var_name = ctx.getText()
        symbol = self.current_scope.resolve(var_name)
        if symbol:
            self.type_of[ctx] = symbol.type
        else:
            self.type_of[ctx] = PrimitiveType.ERROR
            self.error_log.add(ctx, Category.UNDEFINED_NAME,
                               f'Variable {var_name} is not declared')

    def exitStringLiteral(self, ctx: NimbleParser.StringLiteralContext):
        self.type_of[ctx] = PrimitiveType.String

    def exitBoolLiteral(self, ctx: NimbleParser.BoolLiteralContext):
        self.type_of[ctx] = PrimitiveType.Bool
