import 'package:auto_mate_chess/api_endpoint/WebSocket.dart';
import 'package:auto_mate_chess/components/clock.dart';
import 'package:auto_mate_chess/components/commons/add_position.dart';
import 'package:auto_mate_chess/components/commons/drobdown_menu.dart';
import 'package:auto_mate_chess/components/commons/standard_fab.dart';
import 'package:auto_mate_chess/components/commons/time_selector.dart';
import 'package:auto_mate_chess/components/utils/responsive_text.dart';
import 'package:auto_mate_chess/components/utils/util_functions.dart';
import 'package:flutter/material.dart';
import 'package:hive/hive.dart';

import '../../constants/font.dart';
import '../../constants/tint.dart';
import '../utils/responsive_utils.dart';

class CustomChallenge extends StatefulWidget {
  final int time; // Time in seconds
  final int increment; // Increment in seconds
  final String title;

  const CustomChallenge(
      {super.key,
      required this.time,
      required this.increment,
      required this.title});

  @override
  State<CustomChallenge> createState() => _CustomChallengeState();
}

class _CustomChallengeState extends State<CustomChallenge> {
  late double selectedTime; // Time in seconds
  late double selectedIncrement; // Increment in seconds
  bool onTime = true;
  bool smartTime = true;
  final WebSocket socket = SOCKET;
  String? opponent = 'Stockfish';
  dynamic
      startingPosition = // needs to be dynamic since hive provides dynamic vlaues as it is not aware of type
      'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'; //default to default chess position
  String? customStartingPosition;
  List savedStartingPositions = [];
  @override
  void initState() {
    super.initState();
    selectedTime = widget.time.toDouble();
    selectedIncrement = widget.increment.toDouble();
    loadStartingPositionsFromHive();
  }

  void loadStartingPositionsFromHive() {
    // Load items from Hive database
    final box = Hive.box('starting_positions');
    setState(() {
      savedStartingPositions = box.values.toList();
    });
  }

  String formatTime(double seconds) {
    final minutes = seconds ~/ 60;
    final secs = seconds % 60;
    return '$minutes:${secs.toInt().toString().padLeft(2, '0')}';
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      color: Tint.primary,
      margin: EdgeInsets.symmetric(
          horizontal: responsiveWidth(35, context),
          vertical: responsiveHeight(75, context)),
      child: Padding(
        padding: EdgeInsets.all(responsiveHeight(5, context)),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            SizedBox(
              height: responsiveHeight(65, context),
              width: responsiveWidth(double.infinity, context),
              child: Container(
                decoration: const BoxDecoration(
                  color: Tint.primary,
                  boxShadow: [BoxShadow()],
                  borderRadius: BorderRadius.all(
                    Radius.circular(5),
                  ),
                ),
                child: Center(
                  child: ResponsiveText(
                    widget.title,
                    style: Font.h1,
                  ),
                ),
              ),
            ),
            Row(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                const Spacer(
                  flex: 3,
                ),
                ResponsiveText(
                  'On Time:',
                  style: Font.body1,
                ),
                const Spacer(),
                Switch(
                    trackOutlineColor:
                        const WidgetStatePropertyAll(Tint.background),
                    inactiveThumbColor: Tint.primary,
                    activeColor: Tint.background,
                    inactiveTrackColor: Tint.background,
                    activeTrackColor: Tint.primary,
                    value: onTime,
                    onChanged: (value) {
                      setState(() {
                        onTime = value;
                      });
                    }),
                const Spacer(
                  flex: 3,
                ),
              ],
            ),
            Column(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Container(
                  decoration: BoxDecoration(
                      borderRadius:
                          BorderRadius.circular(responsiveHeight(5, context)),
                      color: Tint.primary),
                  child: Padding(
                    padding: EdgeInsets.symmetric(
                        horizontal: responsiveWidth(5, context),
                        vertical: responsiveHeight(8, context)),
                    child: ResponsiveText(
                      onTime
                          ? 'Time per Player: ${formatTime(selectedTime)}'
                          : 'Time per Player: - ',
                      style: Font.h1,
                    ),
                  ),
                ),
                onTime
                    ? TimeSelector(
                        divisions: 570, // 10 seconds intervals
                        max: 6000, // 100 minutes
                        min: 300, // 5 minutes
                        onChange: (value) {
                          setState(() {
                            selectedTime = value;
                          });
                        },
                        value: selectedTime)
                    : Container(),
                Container(
                  decoration: BoxDecoration(
                      borderRadius:
                          BorderRadius.circular(responsiveHeight(5, context)),
                      color: Tint.primary),
                  child: Padding(
                    padding: EdgeInsets.symmetric(
                        horizontal: responsiveWidth(5, context),
                        vertical: responsiveHeight(8, context)),
                    child: ResponsiveText(
                      onTime
                          ? 'Increment: ${formatTime(selectedIncrement)}'
                          : 'Increment: -',
                      style: Font.h1,
                    ),
                  ),
                ),
                onTime
                    ? TimeSelector(
                        divisions: 60,
                        max: 60,
                        min: 0,
                        onChange: (value) {
                          setState(() {
                            selectedIncrement = value;
                          });
                        },
                        value: selectedIncrement)
                    : Container(),
                DrobdownMenu(
                    value: opponent,
                    onChange: (value) {
                      setState(() {
                        opponent = value;
                      });
                    },
                    items: [
                      DropdownMenuItem(
                          value: 'Stockfish',
                          child: ResponsiveText(
                            'Stockfish',
                            style: Font.body1,
                          )),
                      DropdownMenuItem(
                          value: 'MAYA',
                          child: ResponsiveText(
                            'MAYA',
                            style: Font.body1,
                          )),
                      DropdownMenuItem(
                        value: 'Online',
                        child: ResponsiveText(
                          'Online',
                          style: Font.body1,
                        ),
                      ),
                    ]),
              ],
            ),
            Row(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                const Spacer(
                  flex: 3,
                ),
                ResponsiveText(
                  'Smart Time Managment:',
                  style: Font.body1,
                ),
                const Spacer(),
                Switch(
                  trackOutlineColor:
                      const WidgetStatePropertyAll(Tint.background),
                  inactiveThumbColor: Tint.primary,
                  activeColor: Tint.background,
                  inactiveTrackColor: Tint.background,
                  activeTrackColor: Tint.primary,
                  value: onTime ? smartTime : false,
                  onChanged: onTime
                      ? (value) {
                          setState(() {
                            smartTime = value;
                          });
                        }
                      : null,
                ),
                const Spacer(
                  flex: 3,
                ),
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                DrobdownMenu(
                    value: customStartingPosition ?? startingPosition,
                    onChange: (value) {
                      setState(() {
                        startingPosition = value;
                      });
                    },
                    items: customStartingPosition == null
                        ? savedStartingPositions.map(
                            (e) {
                              return DropdownMenuItem(
                                value: e.fen,
                                child: ResponsiveText(
                                  e.name,
                                  style: Font.body1,
                                ),
                              );
                            },
                          ).toList()
                        : [
                            DropdownMenuItem(
                              key: ValueKey(
                                  customStartingPosition), // forces rebuild after custom starting position is added
                              value: customStartingPosition,
                              child: ResponsiveText('Selected Position',
                                  style: Font.body1),
                            ),
                          ]),
                StandardFab(
                  herotag: 'Other',
                  onPressed: () {
                    showGeneralDialog(
                      context: context,
                      pageBuilder: (context, animation, secondaryAnimation) =>
                          AddPosition(
                              onDone: (fen) {
                                setState(() {
                                  customStartingPosition = fen;
                                  startingPosition = fen;
                                });
                              },
                              onSave: (fen) {
                                setState(() {
                                  startingPosition = fen;
                                });
                              },
                              fen: startingPosition),
                    );
                  },
                  child: ResponsiveText(
                    'Other',
                    style: Font.body1Primary,
                  ),
                ),
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                StandardFab(
                  herotag: 'start_game',
                  backgroundColor: Tint.primary,
                  onPressed: () {
                    print(startingPosition);
                    socket.startGame(createGameConfig(
                        true,
                        startingPosition,
                        smartTime,
                        onTime,
                        selectedTime.toInt(),
                        selectedIncrement.toInt()));
                    Navigator.of(context).push(
                      MaterialPageRoute(
                        builder: (context) => Clock(
                          color: true,
                          time: selectedTime.toInt(),
                          increment: selectedIncrement.toInt(),
                        ),
                      ),
                    );
                  },
                  child: ResponsiveText(
                    'Start Game',
                    style: Font.body1,
                  ),
                ),
              ],
            )
          ],
        ),
      ),
    );
  }
}
