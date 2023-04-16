from pyteal import *

#[1, 2, 3], [4, 5, 6], [7, 8, 9],  # Rows
#[1, 4, 7], [2, 5, 8], [3, 6, 9],  # Columns
#[1, 5, 9], [3, 5, 7]              # Diagonals
@Subroutine(TealType.uint64)
def check_win(player, pos1: ScratchVar, pos2: ScratchVar, pos3: ScratchVar, pos4: ScratchVar, pos5: ScratchVar, pos6: ScratchVar, pos7: ScratchVar, pos8: ScratchVar, pos9: ScratchVar):
    return Or(And(pos1.load() == player, pos2.load() == player, pos3.load() == player),
       And(pos4.load() == player, pos5.load() == player, pos6.load() == player),
       And(pos7.load() == player, pos8.load() == player, pos9.load() == player),
       And(pos1.load() == player, pos4.load() == player, pos7.load() == player),
       And(pos2.load() == player, pos5.load() == player, pos8.load() == player),
       And(pos3.load() == player, pos6.load() == player, pos9.load() == player),
       And(pos1.load() == player, pos5.load() == player, pos9.load() == player),
       And(pos3.load() == player, pos5.load() == player, pos7.load() == player))
    

def tic_tac_toe():
    player_moves = Txn.application_args[0]
    status = ScratchVar(TealType.bytes, 0)

    pos1 = ScratchVar(TealType.uint64, 1)
    pos2 = ScratchVar(TealType.uint64, 2)
    pos3 = ScratchVar(TealType.uint64, 3)
    pos4 = ScratchVar(TealType.uint64, 4)
    pos5 = ScratchVar(TealType.uint64, 5)
    pos6 = ScratchVar(TealType.uint64, 6)
    pos7 = ScratchVar(TealType.uint64, 7)
    pos8 = ScratchVar(TealType.uint64, 8)
    pos9 = ScratchVar(TealType.uint64, 9)
    i = ScratchVar(TealType.uint64)
    moved = ScratchVar(TealType.uint64)
    op_corner = ScratchVar(TealType.uint64)
    tmp_pos = ScratchVar(TealType.uint64)
    pos = DynamicScratchVar(TealType.uint64)
    return Seq(
        status.store(Bytes("playing")),
        pos1.store(Int(0)),
        pos2.store(Int(0)),
        pos3.store(Int(0)),
        pos4.store(Int(0)),
        pos5.store(Int(0)),
        pos6.store(Int(0)),
        pos7.store(Int(0)),
        pos8.store(Int(0)),
        pos9.store(Int(0)),
        moved.store(Int(0)),
        op_corner.store(Int(0)),
        For(i.store(Int(0)), i.load() < Len(player_moves), i.store(i.load() + Int(1))).Do(
            # Player moves
            If(GetByte(player_moves, i.load()) == Int(1)).Then(pos.set_index(pos1), op_corner.store(Int(9)))
            .ElseIf(GetByte(player_moves, i.load()) == Int(2)).Then(pos.set_index(pos2))
            .ElseIf(GetByte(player_moves, i.load()) == Int(3)).Then(pos.set_index(pos3), op_corner.store(Int(7)))
            .ElseIf(GetByte(player_moves, i.load()) == Int(4)).Then(pos.set_index(pos4))
            .ElseIf(GetByte(player_moves, i.load()) == Int(5)).Then(pos.set_index(pos5))
            .ElseIf(GetByte(player_moves, i.load()) == Int(6)).Then(pos.set_index(pos6))
            .ElseIf(GetByte(player_moves, i.load()) == Int(7)).Then(pos.set_index(pos7), op_corner.store(Int(3)))
            .ElseIf(GetByte(player_moves, i.load()) == Int(8)).Then(pos.set_index(pos8))
            .ElseIf(GetByte(player_moves, i.load()) == Int(9)).Then(pos.set_index(pos9), op_corner.store(Int(1)))
            .Else(status.store(Bytes("bad move")), Break()),
            If(Not(pos.load())).Then(pos.store(Int(1))).Else(
                status.store(Bytes("bad move")), 
                Break()
            ),
            If(check_win(Int(1), pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8, pos9)).Then(
                status.store(Bytes("player won")),
                Break()
            ),
            If(i.load() == Int(4)).Then(status.store(Bytes("draw")), Break()),
            
            # Contract moves
            # 1: If contract has two in a row -> win
            tmp_pos.store(Int(2)),
            If(And(Not(pos1.load()),
                   check_win(Int(2), tmp_pos, pos2, pos3, pos4, pos5, pos6, pos7, pos8, pos9))).Then(
                pos1.store(Int(2)),
                status.store(Bytes("contract wins")),
                Break()
            ).ElseIf(And(Not(pos2.load()),
                   check_win(Int(2), pos1, tmp_pos, pos3, pos4, pos5, pos6, pos7, pos8, pos9))).Then(
                pos2.store(Int(2)),
                status.store(Bytes("contract wins")),
                Break()
            ).ElseIf(And(Not(pos3.load()),
                   check_win(Int(2), pos1, pos2, tmp_pos, pos4, pos5, pos6, pos7, pos8, pos9))).Then(
                pos3.store(Int(2)),
                status.store(Bytes("contract wins")),
                Break()
            ).ElseIf(And(Not(pos4.load()),
                   check_win(Int(2), pos1, pos2, pos3, tmp_pos, pos5, pos6, pos7, pos8, pos9))).Then(
                pos4.store(Int(2)),
                status.store(Bytes("contract wins")),
                Break()
            ).ElseIf(And(Not(pos5.load()),
                   check_win(Int(2), pos1, pos2, pos3, pos4, tmp_pos, pos6, pos7, pos8, pos9))).Then(
                pos5.store(Int(2)),
                status.store(Bytes("contract wins")),
                Break()
            ).ElseIf(And(Not(pos6.load()),
                   check_win(Int(2), pos1, pos2, pos3, pos4, pos5, tmp_pos, pos7, pos8, pos9))).Then(
                pos6.store(Int(2)),
                status.store(Bytes("contract wins")),
                Break()
            ).ElseIf(And(Not(pos7.load()),
                   check_win(Int(2), pos1, pos2, pos3, pos4, pos5, pos6, tmp_pos, pos8, pos9))).Then(
                pos7.store(Int(2)),
                status.store(Bytes("contract wins")),
                Break()
            ).ElseIf(And(Not(pos8.load()),
                   check_win(Int(2), pos1, pos2, pos3, pos4, pos5, pos6, pos7, tmp_pos, pos9))).Then(
                pos8.store(Int(2)),
                status.store(Bytes("contract wins")),
                Break()
            ).ElseIf(And(Not(pos9.load()),
                   check_win(Int(2), pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8, tmp_pos))).Then(
                pos9.store(Int(2)),
                status.store(Bytes("contract wins")),
                Break()
            ),
            
            # 2: If player has two in a row -> block
            tmp_pos.store(Int(1)),
            If(And(Not(pos1.load()),
                check_win(Int(1), tmp_pos, pos2, pos3, pos4, pos5, pos6, pos7, pos8, pos9))).Then(
                pos1.store(Int(2)),
                moved.store(Int(1))
            ).ElseIf(And(Not(pos2.load()),
                check_win(Int(1), pos1, tmp_pos, pos3, pos4, pos5, pos6, pos7, pos8, pos9))).Then(
                pos2.store(Int(2)),
                moved.store(Int(1))
            ).ElseIf(And(Not(pos3.load()),
                check_win(Int(1), pos1, pos2, tmp_pos, pos4, pos5, pos6, pos7, pos8, pos9))).Then(
                pos3.store(Int(2)),
                moved.store(Int(1))
            ).ElseIf(And(Not(pos4.load()),
                check_win(Int(1), pos1, pos2, pos3, tmp_pos, pos5, pos6, pos7, pos8, pos9))).Then(
                pos4.store(Int(2)),
                moved.store(Int(1))
            ).ElseIf(And(Not(pos5.load()),
                check_win(Int(1), pos1, pos2, pos3, pos4, tmp_pos, pos6, pos7, pos8, pos9))).Then(
                pos5.store(Int(2)),
                moved.store(Int(1))
            ).ElseIf(And(Not(pos6.load()),
                check_win(Int(1), pos1, pos2, pos3, pos4, pos5, tmp_pos, pos7, pos8, pos9))).Then(
                pos6.store(Int(2)),
                moved.store(Int(1))
            ).ElseIf(And(Not(pos7.load()),
                check_win(Int(1), pos1, pos2, pos3, pos4, pos5, pos6, tmp_pos, pos8, pos9))).Then(
                pos7.store(Int(2)),
                moved.store(Int(1))
            ).ElseIf(And(Not(pos8.load()),
                check_win(Int(1), pos1, pos2, pos3, pos4, pos5, pos6, pos7, tmp_pos, pos9))).Then(
                pos8.store(Int(2)),
                moved.store(Int(1))
            ).ElseIf(And(Not(pos9.load()),
                check_win(Int(1), pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8, tmp_pos))).Then(
                pos9.store(Int(2)),
                moved.store(Int(1))
            ),

            # 3: If the center is open -> fill pos5
            If(Not(moved.load())).Then(
                If(Not(pos5.load())).Then(
                    pos5.store(Int(2)),
                    moved.store(Int(1))
                )
            ),

            # 4: If player fills a corner -> fill opposite corner: 1<->9, 3<->7
            If(Not(moved.load())).Then(
                If(Not(op_corner.load())).Then(
                    If(op_corner.load() == Int(1)).Then(pos1.store(Int(2)))
                    .ElseIf(op_corner.load() == Int(3)).Then(pos3.store(Int(2)))
                    .ElseIf(op_corner.load() == Int(7)).Then(pos7.store(Int(2)))
                    .ElseIf(op_corner.load() == Int(9)).Then(pos9.store(Int(2))),
                    moved.store(Int(1))
                )
            ),

            # 5: Fill any corner.
            If(Not(moved.load())).Then(
                If(Not(pos1.load())).Then(
                    pos1.store(Int(2)),
                    moved.store(Int(1))
                ).ElseIf(Not(pos3.load())).Then(
                    pos3.store(Int(2)),
                    moved.store(Int(1))
                ).ElseIf(Not(pos7.load())).Then(
                    pos7.store(Int(2)),
                    moved.store(Int(1))
                ).ElseIf(Not(pos9.load())).Then(
                    pos9.store(Int(2)),
                    moved.store(Int(1))
                )
            ),

            # 6: Fill any of the remaining slots
            If(Not(moved.load())).Then(
                If(Not(pos2.load())).Then(
                    pos2.store(Int(2)),
                    moved.store(Int(1))
                ).ElseIf(Not(pos4.load())).Then(
                    pos4.store(Int(2)),
                    moved.store(Int(1))
                ).ElseIf(Not(pos6.load())).Then(
                    pos6.store(Int(2)),
                    moved.store(Int(1))
                ).ElseIf(Not(pos8.load())).Then(
                    pos8.store(Int(2)),
                    moved.store(Int(1))
                )
            ),

            Assert(moved.load()),

            # Clean temp vars
            moved.store(Int(0)),
            op_corner.store(Int(0))
        ),
        Int(0)
    )

if __name__ == "__main__":
    program = tic_tac_toe()
    with open("contracts/approval_program.teal", "w") as f:
        compiled = compileTeal(program, mode=Mode.Application, version=5)
        f.write(compiled)
