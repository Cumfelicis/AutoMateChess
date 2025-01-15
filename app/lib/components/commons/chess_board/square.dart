import 'package:auto_mate_chess/components/commons/chess_board/piece.dart';
import 'package:auto_mate_chess/constants/tint.dart';
import 'package:flutter/material.dart';

import '../../utils/responsive_utils.dart';

class Square extends StatefulWidget {
  final Piece piece;
  final bool color;
  const Square({super.key, required this.piece, required this.color});

  @override
  State<Square> createState() => _SquareState();
}

class _SquareState extends State<Square> {
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(responsiveWidth(2, context)),
      child: GestureDetector(
        child: Container(
          decoration: BoxDecoration(
            color: widget.color ? Tint.whiteSquare : Tint.blackSquare,
          ),
          child: widget.piece,
        ),
      ),
    );
  }
}
