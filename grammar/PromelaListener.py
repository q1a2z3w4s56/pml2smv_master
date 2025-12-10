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


    # Enter a parse tree produced by PromelaParser#skipStmt.
    def enterSkipStmt(self, ctx:PromelaParser.SkipStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#skipStmt.
    def exitSkipStmt(self, ctx:PromelaParser.SkipStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#breakStmt.
    def enterBreakStmt(self, ctx:PromelaParser.BreakStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#breakStmt.
    def exitBreakStmt(self, ctx:PromelaParser.BreakStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#labeledStmt.
    def enterLabeledStmt(self, ctx:PromelaParser.LabeledStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#labeledStmt.
    def exitLabeledStmt(self, ctx:PromelaParser.LabeledStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#gotoStmt.
    def enterGotoStmt(self, ctx:PromelaParser.GotoStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#gotoStmt.
    def exitGotoStmt(self, ctx:PromelaParser.GotoStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#exprStmt.
    def enterExprStmt(self, ctx:PromelaParser.ExprStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#exprStmt.
    def exitExprStmt(self, ctx:PromelaParser.ExprStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#assignStmt.
    def enterAssignStmt(self, ctx:PromelaParser.AssignStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#assignStmt.
    def exitAssignStmt(self, ctx:PromelaParser.AssignStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#arrayAssignStmt.
    def enterArrayAssignStmt(self, ctx:PromelaParser.ArrayAssignStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#arrayAssignStmt.
    def exitArrayAssignStmt(self, ctx:PromelaParser.ArrayAssignStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#fieldAssignStmt.
    def enterFieldAssignStmt(self, ctx:PromelaParser.FieldAssignStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#fieldAssignStmt.
    def exitFieldAssignStmt(self, ctx:PromelaParser.FieldAssignStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#ifStmt.
    def enterIfStmt(self, ctx:PromelaParser.IfStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#ifStmt.
    def exitIfStmt(self, ctx:PromelaParser.IfStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#doStmt.
    def enterDoStmt(self, ctx:PromelaParser.DoStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#doStmt.
    def exitDoStmt(self, ctx:PromelaParser.DoStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#atomicStmt.
    def enterAtomicStmt(self, ctx:PromelaParser.AtomicStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#atomicStmt.
    def exitAtomicStmt(self, ctx:PromelaParser.AtomicStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#dstepStmt.
    def enterDstepStmt(self, ctx:PromelaParser.DstepStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#dstepStmt.
    def exitDstepStmt(self, ctx:PromelaParser.DstepStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#blockStmt.
    def enterBlockStmt(self, ctx:PromelaParser.BlockStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#blockStmt.
    def exitBlockStmt(self, ctx:PromelaParser.BlockStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#assertStmt.
    def enterAssertStmt(self, ctx:PromelaParser.AssertStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#assertStmt.
    def exitAssertStmt(self, ctx:PromelaParser.AssertStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#printfStmt.
    def enterPrintfStmt(self, ctx:PromelaParser.PrintfStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#printfStmt.
    def exitPrintfStmt(self, ctx:PromelaParser.PrintfStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#printmStmt.
    def enterPrintmStmt(self, ctx:PromelaParser.PrintmStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#printmStmt.
    def exitPrintmStmt(self, ctx:PromelaParser.PrintmStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#sendStmt.
    def enterSendStmt(self, ctx:PromelaParser.SendStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#sendStmt.
    def exitSendStmt(self, ctx:PromelaParser.SendStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#receiveStmt.
    def enterReceiveStmt(self, ctx:PromelaParser.ReceiveStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#receiveStmt.
    def exitReceiveStmt(self, ctx:PromelaParser.ReceiveStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#receivePollStmt.
    def enterReceivePollStmt(self, ctx:PromelaParser.ReceivePollStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#receivePollStmt.
    def exitReceivePollStmt(self, ctx:PromelaParser.ReceivePollStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#receiveArrowStmt.
    def enterReceiveArrowStmt(self, ctx:PromelaParser.ReceiveArrowStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#receiveArrowStmt.
    def exitReceiveArrowStmt(self, ctx:PromelaParser.ReceiveArrowStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#runStmt.
    def enterRunStmt(self, ctx:PromelaParser.RunStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#runStmt.
    def exitRunStmt(self, ctx:PromelaParser.RunStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#inlineCallStmt.
    def enterInlineCallStmt(self, ctx:PromelaParser.InlineCallStmtContext):
        pass

    # Exit a parse tree produced by PromelaParser#inlineCallStmt.
    def exitInlineCallStmt(self, ctx:PromelaParser.InlineCallStmtContext):
        pass


    # Enter a parse tree produced by PromelaParser#optionLists.
    def enterOptionLists(self, ctx:PromelaParser.OptionListsContext):
        pass

    # Exit a parse tree produced by PromelaParser#optionLists.
    def exitOptionLists(self, ctx:PromelaParser.OptionListsContext):
        pass


    # Enter a parse tree produced by PromelaParser#option.
    def enterOption(self, ctx:PromelaParser.OptionContext):
        pass

    # Exit a parse tree produced by PromelaParser#option.
    def exitOption(self, ctx:PromelaParser.OptionContext):
        pass


    # Enter a parse tree produced by PromelaParser#lenExpr.
    def enterLenExpr(self, ctx:PromelaParser.LenExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#lenExpr.
    def exitLenExpr(self, ctx:PromelaParser.LenExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#trueExpr.
    def enterTrueExpr(self, ctx:PromelaParser.TrueExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#trueExpr.
    def exitTrueExpr(self, ctx:PromelaParser.TrueExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#fieldAccessExpr.
    def enterFieldAccessExpr(self, ctx:PromelaParser.FieldAccessExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#fieldAccessExpr.
    def exitFieldAccessExpr(self, ctx:PromelaParser.FieldAccessExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#numberExpr.
    def enterNumberExpr(self, ctx:PromelaParser.NumberExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#numberExpr.
    def exitNumberExpr(self, ctx:PromelaParser.NumberExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#bitwiseOrExpr.
    def enterBitwiseOrExpr(self, ctx:PromelaParser.BitwiseOrExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#bitwiseOrExpr.
    def exitBitwiseOrExpr(self, ctx:PromelaParser.BitwiseOrExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#nrPrExpr.
    def enterNrPrExpr(self, ctx:PromelaParser.NrPrExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#nrPrExpr.
    def exitNrPrExpr(self, ctx:PromelaParser.NrPrExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#bitwiseAndExpr.
    def enterBitwiseAndExpr(self, ctx:PromelaParser.BitwiseAndExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#bitwiseAndExpr.
    def exitBitwiseAndExpr(self, ctx:PromelaParser.BitwiseAndExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#mulDivModExpr.
    def enterMulDivModExpr(self, ctx:PromelaParser.MulDivModExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#mulDivModExpr.
    def exitMulDivModExpr(self, ctx:PromelaParser.MulDivModExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#bitwiseNotExpr.
    def enterBitwiseNotExpr(self, ctx:PromelaParser.BitwiseNotExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#bitwiseNotExpr.
    def exitBitwiseNotExpr(self, ctx:PromelaParser.BitwiseNotExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#timeoutExpr.
    def enterTimeoutExpr(self, ctx:PromelaParser.TimeoutExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#timeoutExpr.
    def exitTimeoutExpr(self, ctx:PromelaParser.TimeoutExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#parenExpr.
    def enterParenExpr(self, ctx:PromelaParser.ParenExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#parenExpr.
    def exitParenExpr(self, ctx:PromelaParser.ParenExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#stringExpr.
    def enterStringExpr(self, ctx:PromelaParser.StringExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#stringExpr.
    def exitStringExpr(self, ctx:PromelaParser.StringExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#logicalNotExpr.
    def enterLogicalNotExpr(self, ctx:PromelaParser.LogicalNotExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#logicalNotExpr.
    def exitLogicalNotExpr(self, ctx:PromelaParser.LogicalNotExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#nemptyExpr.
    def enterNemptyExpr(self, ctx:PromelaParser.NemptyExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#nemptyExpr.
    def exitNemptyExpr(self, ctx:PromelaParser.NemptyExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#enabledExpr.
    def enterEnabledExpr(self, ctx:PromelaParser.EnabledExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#enabledExpr.
    def exitEnabledExpr(self, ctx:PromelaParser.EnabledExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#arrayAccessExpr.
    def enterArrayAccessExpr(self, ctx:PromelaParser.ArrayAccessExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#arrayAccessExpr.
    def exitArrayAccessExpr(self, ctx:PromelaParser.ArrayAccessExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#unaryMinusExpr.
    def enterUnaryMinusExpr(self, ctx:PromelaParser.UnaryMinusExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#unaryMinusExpr.
    def exitUnaryMinusExpr(self, ctx:PromelaParser.UnaryMinusExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#postDecrExpr.
    def enterPostDecrExpr(self, ctx:PromelaParser.PostDecrExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#postDecrExpr.
    def exitPostDecrExpr(self, ctx:PromelaParser.PostDecrExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#falseExpr.
    def enterFalseExpr(self, ctx:PromelaParser.FalseExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#falseExpr.
    def exitFalseExpr(self, ctx:PromelaParser.FalseExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#addSubExpr.
    def enterAddSubExpr(self, ctx:PromelaParser.AddSubExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#addSubExpr.
    def exitAddSubExpr(self, ctx:PromelaParser.AddSubExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#bitwiseXorExpr.
    def enterBitwiseXorExpr(self, ctx:PromelaParser.BitwiseXorExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#bitwiseXorExpr.
    def exitBitwiseXorExpr(self, ctx:PromelaParser.BitwiseXorExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#logicalAndExpr.
    def enterLogicalAndExpr(self, ctx:PromelaParser.LogicalAndExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#logicalAndExpr.
    def exitLogicalAndExpr(self, ctx:PromelaParser.LogicalAndExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#nfullExpr.
    def enterNfullExpr(self, ctx:PromelaParser.NfullExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#nfullExpr.
    def exitNfullExpr(self, ctx:PromelaParser.NfullExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#nonProgressExpr.
    def enterNonProgressExpr(self, ctx:PromelaParser.NonProgressExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#nonProgressExpr.
    def exitNonProgressExpr(self, ctx:PromelaParser.NonProgressExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#pidExpr.
    def enterPidExpr(self, ctx:PromelaParser.PidExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#pidExpr.
    def exitPidExpr(self, ctx:PromelaParser.PidExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#fullExpr.
    def enterFullExpr(self, ctx:PromelaParser.FullExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#fullExpr.
    def exitFullExpr(self, ctx:PromelaParser.FullExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#relationalExpr.
    def enterRelationalExpr(self, ctx:PromelaParser.RelationalExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#relationalExpr.
    def exitRelationalExpr(self, ctx:PromelaParser.RelationalExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#shiftExpr.
    def enterShiftExpr(self, ctx:PromelaParser.ShiftExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#shiftExpr.
    def exitShiftExpr(self, ctx:PromelaParser.ShiftExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#logicalOrExpr.
    def enterLogicalOrExpr(self, ctx:PromelaParser.LogicalOrExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#logicalOrExpr.
    def exitLogicalOrExpr(self, ctx:PromelaParser.LogicalOrExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#emptyExpr.
    def enterEmptyExpr(self, ctx:PromelaParser.EmptyExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#emptyExpr.
    def exitEmptyExpr(self, ctx:PromelaParser.EmptyExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#postIncrExpr.
    def enterPostIncrExpr(self, ctx:PromelaParser.PostIncrExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#postIncrExpr.
    def exitPostIncrExpr(self, ctx:PromelaParser.PostIncrExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#unaryPlusExpr.
    def enterUnaryPlusExpr(self, ctx:PromelaParser.UnaryPlusExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#unaryPlusExpr.
    def exitUnaryPlusExpr(self, ctx:PromelaParser.UnaryPlusExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#equalityExpr.
    def enterEqualityExpr(self, ctx:PromelaParser.EqualityExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#equalityExpr.
    def exitEqualityExpr(self, ctx:PromelaParser.EqualityExprContext):
        pass


    # Enter a parse tree produced by PromelaParser#idExpr.
    def enterIdExpr(self, ctx:PromelaParser.IdExprContext):
        pass

    # Exit a parse tree produced by PromelaParser#idExpr.
    def exitIdExpr(self, ctx:PromelaParser.IdExprContext):
        pass



del PromelaParser
