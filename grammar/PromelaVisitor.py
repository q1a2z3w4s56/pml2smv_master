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


    # Visit a parse tree produced by PromelaParser#SkipStmt.
    def visitSkipStmt(self, ctx:PromelaParser.SkipStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#BreakStmt.
    def visitBreakStmt(self, ctx:PromelaParser.BreakStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#LabeledStmt.
    def visitLabeledStmt(self, ctx:PromelaParser.LabeledStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#GotoStmt.
    def visitGotoStmt(self, ctx:PromelaParser.GotoStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#ExprStmt.
    def visitExprStmt(self, ctx:PromelaParser.ExprStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#AssignStmt.
    def visitAssignStmt(self, ctx:PromelaParser.AssignStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#ArrayAssignStmt.
    def visitArrayAssignStmt(self, ctx:PromelaParser.ArrayAssignStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#FieldAssignStmt.
    def visitFieldAssignStmt(self, ctx:PromelaParser.FieldAssignStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#IfStmt.
    def visitIfStmt(self, ctx:PromelaParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#DoStmt.
    def visitDoStmt(self, ctx:PromelaParser.DoStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#AtomicStmt.
    def visitAtomicStmt(self, ctx:PromelaParser.AtomicStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#DstepStmt.
    def visitDstepStmt(self, ctx:PromelaParser.DstepStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#BlockStmt.
    def visitBlockStmt(self, ctx:PromelaParser.BlockStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#PrintfStmt.
    def visitPrintfStmt(self, ctx:PromelaParser.PrintfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#PrintmStmt.
    def visitPrintmStmt(self, ctx:PromelaParser.PrintmStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#AssertStmt.
    def visitAssertStmt(self, ctx:PromelaParser.AssertStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#SendStmt.
    def visitSendStmt(self, ctx:PromelaParser.SendStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#ReceiveStmt.
    def visitReceiveStmt(self, ctx:PromelaParser.ReceiveStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#ReceivePollStmt.
    def visitReceivePollStmt(self, ctx:PromelaParser.ReceivePollStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#RunStmt.
    def visitRunStmt(self, ctx:PromelaParser.RunStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#InlineCallStmt.
    def visitInlineCallStmt(self, ctx:PromelaParser.InlineCallStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#options.
    def visitOptions(self, ctx:PromelaParser.OptionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#option.
    def visitOption(self, ctx:PromelaParser.OptionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#StringExpr.
    def visitStringExpr(self, ctx:PromelaParser.StringExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#TrueExpr.
    def visitTrueExpr(self, ctx:PromelaParser.TrueExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#BitwiseOrExpr.
    def visitBitwiseOrExpr(self, ctx:PromelaParser.BitwiseOrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#EnabledExpr.
    def visitEnabledExpr(self, ctx:PromelaParser.EnabledExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#EmptyExpr.
    def visitEmptyExpr(self, ctx:PromelaParser.EmptyExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#RelationalExpr.
    def visitRelationalExpr(self, ctx:PromelaParser.RelationalExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#LogicalAndExpr.
    def visitLogicalAndExpr(self, ctx:PromelaParser.LogicalAndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#PostIncrementExpr.
    def visitPostIncrementExpr(self, ctx:PromelaParser.PostIncrementExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#FalseExpr.
    def visitFalseExpr(self, ctx:PromelaParser.FalseExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#PreIncrementExpr.
    def visitPreIncrementExpr(self, ctx:PromelaParser.PreIncrementExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#EqualityExpr.
    def visitEqualityExpr(self, ctx:PromelaParser.EqualityExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#NonProgressExpr.
    def visitNonProgressExpr(self, ctx:PromelaParser.NonProgressExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#PostDecrementExpr.
    def visitPostDecrementExpr(self, ctx:PromelaParser.PostDecrementExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#NumberExpr.
    def visitNumberExpr(self, ctx:PromelaParser.NumberExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#BitwiseNotExpr.
    def visitBitwiseNotExpr(self, ctx:PromelaParser.BitwiseNotExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#FieldAccessExpr.
    def visitFieldAccessExpr(self, ctx:PromelaParser.FieldAccessExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#NfullExpr.
    def visitNfullExpr(self, ctx:PromelaParser.NfullExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#ShiftExpr.
    def visitShiftExpr(self, ctx:PromelaParser.ShiftExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#BitwiseAndExpr.
    def visitBitwiseAndExpr(self, ctx:PromelaParser.BitwiseAndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#NemptyExpr.
    def visitNemptyExpr(self, ctx:PromelaParser.NemptyExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#IdExpr.
    def visitIdExpr(self, ctx:PromelaParser.IdExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#ArrayAccessExpr.
    def visitArrayAccessExpr(self, ctx:PromelaParser.ArrayAccessExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#PreDecrementExpr.
    def visitPreDecrementExpr(self, ctx:PromelaParser.PreDecrementExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#LenExpr.
    def visitLenExpr(self, ctx:PromelaParser.LenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#LogicalNotExpr.
    def visitLogicalNotExpr(self, ctx:PromelaParser.LogicalNotExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#FullExpr.
    def visitFullExpr(self, ctx:PromelaParser.FullExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#LogicalOrExpr.
    def visitLogicalOrExpr(self, ctx:PromelaParser.LogicalOrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#TimeoutExpr.
    def visitTimeoutExpr(self, ctx:PromelaParser.TimeoutExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#MulDivModExpr.
    def visitMulDivModExpr(self, ctx:PromelaParser.MulDivModExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#UnaryPlusExpr.
    def visitUnaryPlusExpr(self, ctx:PromelaParser.UnaryPlusExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#ParenExpr.
    def visitParenExpr(self, ctx:PromelaParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#BitwiseXorExpr.
    def visitBitwiseXorExpr(self, ctx:PromelaParser.BitwiseXorExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#AddSubExpr.
    def visitAddSubExpr(self, ctx:PromelaParser.AddSubExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PromelaParser#UnaryMinusExpr.
    def visitUnaryMinusExpr(self, ctx:PromelaParser.UnaryMinusExprContext):
        return self.visitChildren(ctx)



del PromelaParser