# Generated from Promela.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PromelaParser import PromelaParser
else:
    from PromelaParser import PromelaParser

# This class defines a complete generic visitor for a parse tree produced by PromelaParser.

class PromelaVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by PromelaParser#spec.
    def visitSpec(self, ctx:PromelaParser.SpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#unit.
    def visitUnit(self, ctx:PromelaParser.UnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#chanDecl.
    def visitChanDecl(self, ctx:PromelaParser.ChanDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#mtypeDecl.
    def visitMtypeDecl(self, ctx:PromelaParser.MtypeDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#typedefDecl.
    def visitTypedefDecl(self, ctx:PromelaParser.TypedefDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#varDecl.
    def visitVarDecl(self, ctx:PromelaParser.VarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#typename.
    def visitTypename(self, ctx:PromelaParser.TypenameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#proctype.
    def visitProctype(self, ctx:PromelaParser.ProctypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#paramGroup.
    def visitParamGroup(self, ctx:PromelaParser.ParamGroupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#init.
    def visitInit(self, ctx:PromelaParser.InitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#inlineDecl.
    def visitInlineDecl(self, ctx:PromelaParser.InlineDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#sequence.
    def visitSequence(self, ctx:PromelaParser.SequenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#step.
    def visitStep(self, ctx:PromelaParser.StepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#skipStmt.
    def visitSkipStmt(self, ctx:PromelaParser.SkipStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#breakStmt.
    def visitBreakStmt(self, ctx:PromelaParser.BreakStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#labeledStmt.
    def visitLabeledStmt(self, ctx:PromelaParser.LabeledStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#gotoStmt.
    def visitGotoStmt(self, ctx:PromelaParser.GotoStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#assignStmt.
    def visitAssignStmt(self, ctx:PromelaParser.AssignStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#arrayAssignStmt.
    def visitArrayAssignStmt(self, ctx:PromelaParser.ArrayAssignStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#fieldAssignStmt.
    def visitFieldAssignStmt(self, ctx:PromelaParser.FieldAssignStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#ifStmt.
    def visitIfStmt(self, ctx:PromelaParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#doStmt.
    def visitDoStmt(self, ctx:PromelaParser.DoStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#atomicStmt.
    def visitAtomicStmt(self, ctx:PromelaParser.AtomicStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#dstepStmt.
    def visitDstepStmt(self, ctx:PromelaParser.DstepStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#blockStmt.
    def visitBlockStmt(self, ctx:PromelaParser.BlockStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#assertStmt.
    def visitAssertStmt(self, ctx:PromelaParser.AssertStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#printfStmt.
    def visitPrintfStmt(self, ctx:PromelaParser.PrintfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#printmStmt.
    def visitPrintmStmt(self, ctx:PromelaParser.PrintmStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#sendStmt.
    def visitSendStmt(self, ctx:PromelaParser.SendStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#receiveStmt.
    def visitReceiveStmt(self, ctx:PromelaParser.ReceiveStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#receivePollStmt.
    def visitReceivePollStmt(self, ctx:PromelaParser.ReceivePollStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#receiveArrowStmt.
    def visitReceiveArrowStmt(self, ctx:PromelaParser.ReceiveArrowStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#runStmt.
    def visitRunStmt(self, ctx:PromelaParser.RunStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#inlineCallStmt.
    def visitInlineCallStmt(self, ctx:PromelaParser.InlineCallStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#exprStmt.
    def visitExprStmt(self, ctx:PromelaParser.ExprStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#optionLists.
    def visitOptionLists(self, ctx:PromelaParser.OptionListsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#option.
    def visitOption(self, ctx:PromelaParser.OptionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#lenExpr.
    def visitLenExpr(self, ctx:PromelaParser.LenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#trueExpr.
    def visitTrueExpr(self, ctx:PromelaParser.TrueExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#fieldAccessExpr.
    def visitFieldAccessExpr(self, ctx:PromelaParser.FieldAccessExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#numberExpr.
    def visitNumberExpr(self, ctx:PromelaParser.NumberExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#bitwiseOrExpr.
    def visitBitwiseOrExpr(self, ctx:PromelaParser.BitwiseOrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#nrPrExpr.
    def visitNrPrExpr(self, ctx:PromelaParser.NrPrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#bitwiseAndExpr.
    def visitBitwiseAndExpr(self, ctx:PromelaParser.BitwiseAndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#mulDivModExpr.
    def visitMulDivModExpr(self, ctx:PromelaParser.MulDivModExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#bitwiseNotExpr.
    def visitBitwiseNotExpr(self, ctx:PromelaParser.BitwiseNotExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#timeoutExpr.
    def visitTimeoutExpr(self, ctx:PromelaParser.TimeoutExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#parenExpr.
    def visitParenExpr(self, ctx:PromelaParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#stringExpr.
    def visitStringExpr(self, ctx:PromelaParser.StringExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#logicalNotExpr.
    def visitLogicalNotExpr(self, ctx:PromelaParser.LogicalNotExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#nemptyExpr.
    def visitNemptyExpr(self, ctx:PromelaParser.NemptyExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#enabledExpr.
    def visitEnabledExpr(self, ctx:PromelaParser.EnabledExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#arrayAccessExpr.
    def visitArrayAccessExpr(self, ctx:PromelaParser.ArrayAccessExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#unaryMinusExpr.
    def visitUnaryMinusExpr(self, ctx:PromelaParser.UnaryMinusExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#postDecrExpr.
    def visitPostDecrExpr(self, ctx:PromelaParser.PostDecrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#falseExpr.
    def visitFalseExpr(self, ctx:PromelaParser.FalseExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#addSubExpr.
    def visitAddSubExpr(self, ctx:PromelaParser.AddSubExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#bitwiseXorExpr.
    def visitBitwiseXorExpr(self, ctx:PromelaParser.BitwiseXorExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#logicalAndExpr.
    def visitLogicalAndExpr(self, ctx:PromelaParser.LogicalAndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#nfullExpr.
    def visitNfullExpr(self, ctx:PromelaParser.NfullExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#nonProgressExpr.
    def visitNonProgressExpr(self, ctx:PromelaParser.NonProgressExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#pidExpr.
    def visitPidExpr(self, ctx:PromelaParser.PidExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#fullExpr.
    def visitFullExpr(self, ctx:PromelaParser.FullExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#relationalExpr.
    def visitRelationalExpr(self, ctx:PromelaParser.RelationalExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#shiftExpr.
    def visitShiftExpr(self, ctx:PromelaParser.ShiftExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#logicalOrExpr.
    def visitLogicalOrExpr(self, ctx:PromelaParser.LogicalOrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#emptyExpr.
    def visitEmptyExpr(self, ctx:PromelaParser.EmptyExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#postIncrExpr.
    def visitPostIncrExpr(self, ctx:PromelaParser.PostIncrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#unaryPlusExpr.
    def visitUnaryPlusExpr(self, ctx:PromelaParser.UnaryPlusExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#equalityExpr.
    def visitEqualityExpr(self, ctx:PromelaParser.EqualityExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#idExpr.
    def visitIdExpr(self, ctx:PromelaParser.IdExprContext):
        return self.visitChildren(ctx)



del PromelaParser
