import 'package:auto_mate_chess/components/commons/chess_board/piece.dart';
import 'package:auto_mate_chess/components/commons/chess_board/square.dart';
import 'package:auto_mate_chess/components/utils/responsive_utils.dart';
import 'package:auto_mate_chess/constants/tint.dart';
import 'package:flutter/material.dart';

import '../../utils/util_functions.dart';

class Board extends StatefulWidget {
  final String fen;
  const Board({super.key, required this.fen});

  @override
  State<Board> createState() => _BoardState();
}

class _BoardState extends State<Board> {
  late List<String?> pieceNames;
  List<String?> setup(String fen) {
    List<String?> setup = List.filled(64, null);
    int row = 0;
    int column = 0;
    for (var char in fen.split('')) {
      if (row <= 7) {
        if (char == '/') {
          row++;
          column = 0;
        } else if (isNumeric(char)) {
          column += int.tryParse(char)!;
        } else if (char != ' ') {
          setup[(8 * row) + column] = char;
          column++;
        } else {
          row = 8;
        }
      }
    }
    return setup;
  }

  void updateBoard(BuildContext context, int index, String? name) {
    setState(() {
      pieceNames[index] = name;
    });
    Navigator.of(context).pop();
  }

  @override
  void initState() {
    pieceNames = setup(widget.fen);
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    print(pieceNames.indexed);
    List<Piece> pieces = pieceNames.indexed
        .map((name) => Piece(
              pieceName: name.$2,
              index: name.$1,
              onTap: updateBoard,
              interactable: true,
              onSelection: (context, index, name) {},
              selectable: false,
            ))
        .toList();
    List<bool> squareColors = List.generate(64,
        (index) => (index ~/ 8) % 2 == 0 ? index % 2 == 0 : !(index % 2 == 0));
    return Padding(
      padding: EdgeInsets.symmetric(
          vertical: responsiveHeight(30, context),
          horizontal: responsiveWidth(10, context)),
      child: GridView.count(
        crossAxisCount: 8,
        primary: false,
        children: squareColors.indexed.map((value) {
          return Square(piece: pieces[value.$1], color: value.$2);
        }).toList(),
      ),
    );
  }
}
