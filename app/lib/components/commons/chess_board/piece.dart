import 'package:auto_mate_chess/components/commons/chess_board/choose_piece.dart';
import 'package:flutter/material.dart';

Map<String, String> images = {
  'R': 'lib/assets/images/wR.png',
  'K': 'lib/assets/images/wK.png',
  'Q': 'lib/assets/images/wQ.png',
  'P': 'lib/assets/images/wP.png',
  'N': 'lib/assets/images/wN.png',
  'B': 'lib/assets/images/wB.png',
  'r': 'lib/assets/images/bR.png',
  'k': 'lib/assets/images/bK.png',
  'q': 'lib/assets/images/bQ.png',
  'p': 'lib/assets/images/bP.png',
  'n': 'lib/assets/images/bN.png',
  'b': 'lib/assets/images/bB.png',
};

class Piece extends StatefulWidget {
  final String? pieceName;
  final int index;
  final void Function(BuildContext context, int index, String? name) onTap;
  final void Function(BuildContext context, int index, String? name)
      onSelection;
  final bool interactable;
  final bool selectable;
  const Piece(
      {super.key,
      required this.pieceName,
      required this.index,
      required this.onTap,
      required this.interactable,
      required this.selectable,
      required this.onSelection});

  @override
  State<Piece> createState() => _PieceState();
}

class _PieceState extends State<Piece> {
  @override
  Widget build(BuildContext context) {
    return GestureDetector(
        onTap: widget.interactable == true
            ? () {
                showGeneralDialog(
                    context: context,
                    pageBuilder: (context, animation, secondasryAnimation) {
                      return ChoosePiece(
                        onSelection: widget.onTap,
                        index: widget.index,
                      );
                    });
              }
            : widget.selectable == true
                ? () {
                    widget.onSelection(context, widget.index, widget.pieceName);
                  }
                : null,
        child: widget.pieceName == null
            ? Container(color: Colors.transparent)
            : Image.asset(
                images[widget.pieceName]!,
              ));
  }
}
