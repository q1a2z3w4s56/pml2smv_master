# Generated from Promela.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PromelaParser import PromelaParser
else:
    from PromelaParser import PromelaParser

# This class defines a complete listener for a parse tree produced by PromelaParser.
class PromelaListener(ParseTreeListener):

    # Enter a parse tree produced by PromelaParser#spec.
    def enterSpec(self, ctx:PromelaParser.SpecContext):
        pass

    # Exit a parse tree produced by PromelaParser#spec.
    def exitSpec(self, ctx:PromelaParser.SpecContext):
        pass


    # Enter a parse tree produced by PromelaParser#unit.
    def enterUnit(self, ctx:PromelaParser.UnitContext):
        pass

    # Exit a parse tree produced by PromelaParser#unit.
    def exitUnit(self, ctx:PromelaParser.UnitContext):
        pass


    # Enter a parse tree produced by PromelaParser#chanDecl.
    def enterChanDecl(self, ctx:PromelaParser.ChanDeclContext):
        pass

    # Exit a parse tree produced by PromelaParser#chanDecl.
    def exitChanDecl(self, ctx:PromelaParser.ChanDeclContext):
        pass


    # Enter a parse tree produced by PromelaParser#mtypeDecl.
    def enterMtypeDecl(self, ctx:PromelaParser.MtypeDeclContext):
        pass

    # Exit a parse tree produced by PromelaParser#mtypeDecl.
    def exitMtypeDecl(self, ctx:PromelaParser.MtypeDeclContext):
        pass


    # Enter a parse tree produced by PromelaParser#typedefDecl.
    def enterTypedefDecl(self, ctx:PromelaParser.TypedefDeclContext):
        pass

    # Exit a parse tree produced by PromelaParser#typedefDecl.
    def exitTypedefDecl(self, ctx:PromelaParser.TypedefDeclContext):
        pass


    # Enter a parse tree produced by PromelaParser#varDecl.
    def enterVarDecl(self, ctx:PromelaParser.VarDeclContext):
        pass

    # Exit a parse tree produced by PromelaParser#varDecl.
    def exitVarDecl(self, ctx:PromelaParser.VarDeclContext):
        pass


    # Enter a parse tree produced by PromelaParser#typename.
    def enterTypename(self, ctx:PromelaParser.TypenameContext):
        pass

    # Exit a parse tree produced by PromelaParser#typename.
    def exitTypename(self, ctx:PromelaParser.TypenameContext):
        pass


    # Enter a parse tree produced by PromelaParser#proctype.
    def enterProctype(self, ctx:PromelaParser.ProctypeContext):
        pass

    # Exit a parse tree produced by PromelaParser#proctype.
    def exitProctype(self, ctx:PromelaParser.ProctypeContext):
        pass


    # Enter a parse tree produced by PromelaParser#init.
    def enterInit(self, ctx:PromelaParser.InitContext):
        pass

    # Exit a parse tree produced by PromelaParser#init.
    def exitInit(self, ctx:PromelaParser.InitContext):
        pass


    # Enter a parse tree produced by PromelaParser#inlineDecl.
    def enterInlineDecl(self, ctx:PromelaParser.InlineDeclContext):
        pass

    # Exit a parse tree produced by PromelaParser#inlineDecl.
    def exitInlineDecl(self, ctx:PromelaParser.InlineDeclContext):
        pass


    # Enter a parse tree produced by PromelaParser#sequence.
    def enterSequence(self, ctx:PromelaParser.SequenceContext):
        pass

    # Exit a parse tree produced by PromelaParser#sequence.
    def exitSequence(self, ctx:PromelaParser.SequenceContext):
        pass


    # Enter a parse tree produced by PromelaParser#step.
    def enterStep(self, ctx:PromelaParser.StepContext):
        pass

    # Exit a parse tree produced by PromelaParser#step.
    def exitStep(self, ctx:PromelaParser.StepContext):
        pass


    # Enter a parse tree produced by PromelaParser#SkipStmt.
    def enterSkipStmt(self, ctx:PromelaParser.SkipStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#SkipStmt.
    def exitSkipStmt(self, ctx:PromelaParser.SkipStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#BreakStmt.
    def enterBreakStmt(self, ctx:PromelaParser.BreakStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#BreakStmt.
    def exitBreakStmt(self, ctx:PromelaParser.BreakStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#LabeledStmt.
    def enterLabeledStmt(self, ctx:PromelaParser.LabeledStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#LabeledStmt.
    def exitLabeledStmt(self, ctx:PromelaParser.LabeledStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#GotoStmt.
    def enterGotoStmt(self, ctx:PromelaParser.GotoStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#GotoStmt.
    def exitGotoStmt(self, ctx:PromelaParser.GotoStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#ExprStmt.
    def enterExprStmt(self, ctx:PromelaParser.ExprStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#ExprStmt.
    def exitExprStmt(self, ctx:PromelaParser.ExprStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#AssignStmt.
    def enterAssignStmt(self, ctx:PromelaParser.AssignStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#AssignStmt.
    def exitAssignStmt(self, ctx:PromelaParser.AssignStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#ArrayAssignStmt.
    def enterArrayAssignStmt(self, ctx:PromelaParser.ArrayAssignStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#ArrayAssignStmt.
    def exitArrayAssignStmt(self, ctx:PromelaParser.ArrayAssignStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#FieldAssignStmt.
    def enterFieldAssignStmt(self, ctx:PromelaParser.FieldAssignStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#FieldAssignStmt.
    def exitFieldAssignStmt(self, ctx:PromelaParser.FieldAssignStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#IfStmt.
    def enterIfStmt(self, ctx:PromelaParser.IfStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#IfStmt.
    def exitIfStmt(self, ctx:PromelaParser.IfStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#DoStmt.
    def enterDoStmt(self, ctx:PromelaParser.DoStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#DoStmt.
    def exitDoStmt(self, ctx:PromelaParser.DoStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#AtomicStmt.
    def enterAtomicStmt(self, ctx:PromelaParser.AtomicStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#AtomicStmt.
    def exitAtomicStmt(self, ctx:PromelaParser.AtomicStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#DstepStmt.
    def enterDstepStmt(self, ctx:PromelaParser.DstepStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#DstepStmt.
    def exitDstepStmt(self, ctx:PromelaParser.DstepStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#BlockStmt.
    def enterBlockStmt(self, ctx:PromelaParser.BlockStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#BlockStmt.
    def exitBlockStmt(self, ctx:PromelaParser.BlockStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#PrintfStmt.
    def enterPrintfStmt(self, ctx:PromelaParser.PrintfStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#PrintfStmt.
    def exitPrintfStmt(self, ctx:PromelaParser.PrintfStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#PrintmStmt.
    def enterPrintmStmt(self, ctx:PromelaParser.PrintmStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#PrintmStmt.
    def exitPrintmStmt(self, ctx:PromelaParser.PrintmStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#AssertStmt.
    def enterAssertStmt(self, ctx:PromelaParser.AssertStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#AssertStmt.
    def exitAssertStmt(self, ctx:PromelaParser.AssertStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#SendStmt.
    def enterSendStmt(self, ctx:PromelaParser.SendStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#SendStmt.
    def exitSendStmt(self, ctx:PromelaParser.SendStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#ReceiveStmt.
    def enterReceiveStmt(self, ctx:PromelaParser.ReceiveStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#ReceiveStmt.
    def exitReceiveStmt(self, ctx:PromelaParser.ReceiveStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#ReceivePollStmt.
    def enterReceivePollStmt(self, ctx:PromelaParser.ReceivePollStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#ReceivePollStmt.
    def exitReceivePollStmt(self, ctx:PromelaParser.ReceivePollStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#RunStmt.
    def enterRunStmt(self, ctx:PromelaParser.RunStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#RunStmt.
    def exitRunStmt(self, ctx:PromelaParser.RunStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#InlineCallStmt.
    def enterInlineCallStmt(self, ctx:PromelaParser.InlineCallStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#InlineCallStmt.
    def exitInlineCallStmt(self, ctx:PromelaParser.InlineCallStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#options.
    def enterOptions(self, ctx:PromelaParser.OptionsContext):
        pass

    # Exit a parse tree produced by PromelaParser#options.
    def exitOptions(self, ctx:PromelaParser.OptionsContext):
        pass


    # Enter a parse tree produced by PromelaParser#option.
    def enterOption(self, ctx:PromelaParser.OptionContext):
        pass

    # Exit a parse tree produced by PromelaParser#option.
    def exitOption(self, ctx:PromelaParser.OptionContext):
        pass


    # Enter a parse tree produced by PromelaParser#StringExpr.
    def enterStringExpr(self, ctx:PromelaParser.StringExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#StringExpr.
    def exitStringExpr(self, ctx:PromelaParser.StringExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#TrueExpr.
    def enterTrueExpr(self, ctx:PromelaParser.TrueExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#TrueExpr.
    def exitTrueExpr(self, ctx:PromelaParser.TrueExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#BitwiseOrExpr.
    def enterBitwiseOrExpr(self, ctx:PromelaParser.BitwiseOrExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#BitwiseOrExpr.
    def exitBitwiseOrExpr(self, ctx:PromelaParser.BitwiseOrExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#EnabledExpr.
    def enterEnabledExpr(self, ctx:PromelaParser.EnabledExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#EnabledExpr.
    def exitEnabledExpr(self, ctx:PromelaParser.EnabledExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#EmptyExpr.
    def enterEmptyExpr(self, ctx:PromelaParser.EmptyExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#EmptyExpr.
    def exitEmptyExpr(self, ctx:PromelaParser.EmptyExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#RelationalExpr.
    def enterRelationalExpr(self, ctx:PromelaParser.RelationalExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#RelationalExpr.
    def exitRelationalExpr(self, ctx:PromelaParser.RelationalExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#LogicalAndExpr.
    def enterLogicalAndExpr(self, ctx:PromelaParser.LogicalAndExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#LogicalAndExpr.
    def exitLogicalAndExpr(self, ctx:PromelaParser.LogicalAndExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#PostIncrementExpr.
    def enterPostIncrementExpr(self, ctx:PromelaParser.PostIncrementExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#PostIncrementExpr.
    def exitPostIncrementExpr(self, ctx:PromelaParser.PostIncrementExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#FalseExpr.
    def enterFalseExpr(self, ctx:PromelaParser.FalseExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#FalseExpr.
    def exitFalseExpr(self, ctx:PromelaParser.FalseExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#PreIncrementExpr.
    def enterPreIncrementExpr(self, ctx:PromelaParser.PreIncrementExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#PreIncrementExpr.
    def exitPreIncrementExpr(self, ctx:PromelaParser.PreIncrementExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#EqualityExpr.
    def enterEqualityExpr(self, ctx:PromelaParser.EqualityExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#EqualityExpr.
    def exitEqualityExpr(self, ctx:PromelaParser.EqualityExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#NonProgressExpr.
    def enterNonProgressExpr(self, ctx:PromelaParser.NonProgressExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#NonProgressExpr.
    def exitNonProgressExpr(self, ctx:PromelaParser.NonProgressExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#PostDecrementExpr.
    def enterPostDecrementExpr(self, ctx:PromelaParser.PostDecrementExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#PostDecrementExpr.
    def exitPostDecrementExpr(self, ctx:PromelaParser.PostDecrementExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#NumberExpr.
    def enterNumberExpr(self, ctx:PromelaParser.NumberExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#NumberExpr.
    def exitNumberExpr(self, ctx:PromelaParser.NumberExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#BitwiseNotExpr.
    def enterBitwiseNotExpr(self, ctx:PromelaParser.BitwiseNotExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#BitwiseNotExpr.
    def exitBitwiseNotExpr(self, ctx:PromelaParser.BitwiseNotExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#FieldAccessExpr.
    def enterFieldAccessExpr(self, ctx:PromelaParser.FieldAccessExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#FieldAccessExpr.
    def exitFieldAccessExpr(self, ctx:PromelaParser.FieldAccessExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#NfullExpr.
    def enterNfullExpr(self, ctx:PromelaParser.NfullExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#NfullExpr.
    def exitNfullExpr(self, ctx:PromelaParser.NfullExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#ShiftExpr.
    def enterShiftExpr(self, ctx:PromelaParser.ShiftExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#ShiftExpr.
    def exitShiftExpr(self, ctx:PromelaParser.ShiftExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#BitwiseAndExpr.
    def enterBitwiseAndExpr(self, ctx:PromelaParser.BitwiseAndExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#BitwiseAndExpr.
    def exitBitwiseAndExpr(self, ctx:PromelaParser.BitwiseAndExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#NemptyExpr.
    def enterNemptyExpr(self, ctx:PromelaParser.NemptyExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#NemptyExpr.
    def exitNemptyExpr(self, ctx:PromelaParser.NemptyExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#IdExpr.
    def enterIdExpr(self, ctx:PromelaParser.IdExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#IdExpr.
    def exitIdExpr(self, ctx:PromelaParser.IdExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#ArrayAccessExpr.
    def enterArrayAccessExpr(self, ctx:PromelaParser.ArrayAccessExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#ArrayAccessExpr.
    def exitArrayAccessExpr(self, ctx:PromelaParser.ArrayAccessExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#PreDecrementExpr.
    def enterPreDecrementExpr(self, ctx:PromelaParser.PreDecrementExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#PreDecrementExpr.
    def exitPreDecrementExpr(self, ctx:PromelaParser.PreDecrementExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#LenExpr.
    def enterLenExpr(self, ctx:PromelaParser.LenExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#LenExpr.
    def exitLenExpr(self, ctx:PromelaParser.LenExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#LogicalNotExpr.
    def enterLogicalNotExpr(self, ctx:PromelaParser.LogicalNotExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#LogicalNotExpr.
    def exitLogicalNotExpr(self, ctx:PromelaParser.LogicalNotExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#FullExpr.
    def enterFullExpr(self, ctx:PromelaParser.FullExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#FullExpr.
    def exitFullExpr(self, ctx:PromelaParser.FullExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#LogicalOrExpr.
    def enterLogicalOrExpr(self, ctx:PromelaParser.LogicalOrExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#LogicalOrExpr.
    def exitLogicalOrExpr(self, ctx:PromelaParser.LogicalOrExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#TimeoutExpr.
    def enterTimeoutExpr(self, ctx:PromelaParser.TimeoutExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#TimeoutExpr.
    def exitTimeoutExpr(self, ctx:PromelaParser.TimeoutExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#MulDivModExpr.
    def enterMulDivModExpr(self, ctx:PromelaParser.MulDivModExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#MulDivModExpr.
    def exitMulDivModExpr(self, ctx:PromelaParser.MulDivModExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#UnaryPlusExpr.
    def enterUnaryPlusExpr(self, ctx:PromelaParser.UnaryPlusExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#UnaryPlusExpr.
    def exitUnaryPlusExpr(self, ctx:PromelaParser.UnaryPlusExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#ParenExpr.
    def enterParenExpr(self, ctx:PromelaParser.ParenExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#ParenExpr.
    def exitParenExpr(self, ctx:PromelaParser.ParenExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#BitwiseXorExpr.
    def enterBitwiseXorExpr(self, ctx:PromelaParser.BitwiseXorExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#BitwiseXorExpr.
    def exitBitwiseXorExpr(self, ctx:PromelaParser.BitwiseXorExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#AddSubExpr.
    def enterAddSubExpr(self, ctx:PromelaParser.AddSubExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#AddSubExpr.
    def exitAddSubExpr(self, ctx:PromelaParser.AddSubExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#UnaryMinusExpr.
    def enterUnaryMinusExpr(self, ctx:PromelaParser.UnaryMinusExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#UnaryMinusExpr.
    def exitUnaryMinusExpr(self, ctx:PromelaParser.UnaryMinusExprContext):
        pass



del PromelaParser