import 'package:auto_mate_chess/components/utils/responsive_utils.dart';
import 'package:flutter/material.dart';

import 'piece.dart';

class ChoosePiece extends StatelessWidget {
  final int index;
  final void Function(BuildContext context, int index, String? name)
      onSelection;
  const ChoosePiece(
      {super.key, required this.onSelection, required this.index});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: responsiveWidth(300, context),
      height: responsiveHeight(650, context),
      child: Row(children: [
        Expanded(
          child: Column(children: [
            Expanded(
              child: Piece(
                index: index,
                pieceName: 'K',
                onTap: onSelection,
                onSelection: onSelection,
                interactable: false,
                selectable: true,
              ),
            ),
            Expanded(
              child: Piece(
                index: index,
                pieceName: 'Q',
                onTap: onSelection,
                onSelection: onSelection,
                interactable: false,
                selectable: true,
              ),
            ),
            Expanded(
              child: Piece(
                index: index,
                pieceName: 'R',
                onTap: onSelection,
                onSelection: onSelection,
                interactable: false,
                selectable: true,
              ),
            ),
            Expanded(
              child: Piece(
                index: index,
                pieceName: 'B',
                onTap: onSelection,
                onSelection: onSelection,
                interactable: false,
                selectable: true,
              ),
            ),
            Expanded(
              child: Piece(
                index: index,
                pieceName: 'N',
                onTap: onSelection,
                onSelection: onSelection,
                interactable: false,
                selectable: true,
              ),
            ),
            Expanded(
              child: Piece(
                index: index,
                pieceName: 'P',
                onTap: onSelection,
                onSelection: onSelection,
                interactable: false,
                selectable: true,
              ),
            ),
            Expanded(
                child: IconButton(
                    onPressed: () => Navigator.of(context).pop(),
                    icon: const Icon(Icons.close)))
          ]),
        ),
        Expanded(
          child: Column(
            children: [
              Expanded(
                child: Piece(
                  index: index,
                  pieceName: 'k',
                  onTap: onSelection,
                  onSelection: onSelection,
                  interactable: false,
                  selectable: true,
                ),
              ),
              Expanded(
                child: Piece(
                  index: index,
                  pieceName: 'q',
                  onTap: onSelection,
                  onSelection: onSelection,
                  interactable: false,
                  selectable: true,
                ),
              ),
              Expanded(
                child: Piece(
                  index: index,
                  pieceName: 'r',
                  onTap: onSelection,
                  onSelection: onSelection,
                  interactable: false,
                  selectable: true,
                ),
              ),
              Expanded(
                child: Piece(
                  index: index,
                  pieceName: 'b',
                  onTap: onSelection,
                  onSelection: onSelection,
                  interactable: false,
                  selectable: true,
                ),
              ),
              Expanded(
                child: Piece(
                  index: index,
                  pieceName: 'n',
                  onTap: onSelection,
                  onSelection: onSelection,
                  interactable: false,
                  selectable: true,
                ),
              ),
              Expanded(
                child: Piece(
                  index: index,
                  pieceName: 'p',
                  onTap: onSelection,
                  onSelection: onSelection,
                  interactable: false,
                  selectable: true,
                ),
              ),
              Expanded(
                  child: Stack(children: [
                const Icon(Icons.delete),
                Piece(
                  index: index,
                  pieceName: null,
                  onTap: onSelection,
                  onSelection: onSelection,
                  interactable: false,
                  selectable: true,
                ),
              ]))
            ],
          ),
        )
      ]),
    );
  }
}
