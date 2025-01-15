import 'package:auto_mate_chess/components/commons/chess_board/board.dart';
import 'package:auto_mate_chess/components/commons/choose_name.dart';
import 'package:auto_mate_chess/components/commons/standard_fab.dart';
import 'package:auto_mate_chess/components/utils/responsive_text.dart';
import 'package:auto_mate_chess/components/utils/responsive_utils.dart';
import 'package:auto_mate_chess/constants/font.dart';
import 'package:auto_mate_chess/constants/tint.dart';
import 'package:auto_mate_chess/database/position.dart';
import 'package:flutter/material.dart';
import 'package:hive/hive.dart';

class AddPosition extends StatefulWidget {
  const AddPosition(
      {super.key,
      required this.onDone,
      required this.fen,
      required this.onSave});
  final String fen;
  final Function(String) onDone;
  final Function(String) onSave;

  @override
  State<AddPosition> createState() => _AddPositionState();
}

class _AddPositionState extends State<AddPosition> {
  late String fen;
  late Widget board;
  late TextEditingController _controller;
  String? name;

  @override
  void initState() {
    fen = widget.fen;
    _controller = TextEditingController(text: fen);
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return ConstrainedBox(
      constraints: BoxConstraints(
          maxHeight: responsiveHeight(550, context),
          maxWidth: responsiveWidth(300, context)),
      child: ClipRect(
        child: Card(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              SizedBox(
                height: responsiveHeight(425, context),
                width: responsiveWidth(double.infinity, context),
                child: Board(
                    key: ValueKey(fen), // forces rebuild when fen is updated
                    fen: fen,
                    onChange: (newFen) {
                      setState(() {
                        fen = newFen;
                        _controller.text = fen;
                      });
                    }),
              ),
              Padding(
                padding: EdgeInsets.only(top: responsiveHeight(5, context)),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Spacer(),
                    Expanded(
                      flex: 3,
                      child: TextField(
                        controller: _controller,
                        onSubmitted: (value) {
                          setState(() {
                            fen = value;
                          });
                        },
                      ),
                    ),
                    const Spacer()
                  ],
                ),
              ),
              Padding(
                padding: EdgeInsets.symmetric(
                    vertical: responsiveHeight(15, context)),
                child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      StandardFab(
                        backgroundColor: Tint.primary,
                        child: ResponsiveText(
                          'Save',
                          style: Font.body1,
                        ),
                        onPressed: () async {
                          await showGeneralDialog(
                            context: context,
                            pageBuilder:
                                (context, animation, secondaryAnimation) {
                              return ChooseName(onDecision: (newName) {
                                setState(() {
                                  name = newName;
                                });
                              });
                            },
                          );
                          Hive.box('starting_positions')
                              .add(Position(name: name!, fen: fen));
                          widget.onSave(fen);
                          Navigator.of(context).pop();
                        },
                      ),
                      StandardFab(
                        backgroundColor: Tint.primary,
                        child: ResponsiveText('Use', style: Font.body1),
                        onPressed: () {
                          print(fen);
                          widget.onDone(fen);
                          Navigator.of(context).pop();
                        },
                      )
                    ]),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
