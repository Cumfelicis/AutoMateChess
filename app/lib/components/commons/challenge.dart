import 'dart:io';

import 'package:auto_mate_chess/components/clock.dart';
import 'package:auto_mate_chess/components/commons/custom_challenge.dart';
import 'package:auto_mate_chess/components/utils/responsive_text.dart';
import 'package:auto_mate_chess/constants/tint.dart';
import 'package:auto_mate_chess/constants/font.dart';
import 'package:flutter/material.dart';
import '../utils/responsive_utils.dart';
import '../../api_endpoint/api_call.dart' as api;
import '../../api_endpoint/WebSocket.dart' as socket;

class Challenge extends StatefulWidget {
  final int time;
  final int increment;
  final String mode;
  const Challenge(
      {super.key,
      required this.time,
      required this.increment,
      required this.mode});

  @override
  State<Challenge> createState() => _ChallengeState();
}

class _ChallengeState extends State<Challenge> {
  late int _time;
  late int _increment;

  @override
  void initState() {
    _time = widget.time ~/ 60; // Integer division
    _increment = widget.increment;
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        print('started game');
        Navigator.of(context).push(MaterialPageRoute(
            builder: (context) => CustomChallenge(
                time: widget.time,
                increment: widget.increment,
                title: 'New Game')));
      },
      child: Padding(
        padding: EdgeInsets.all(responsiveHeight(5, context)),
        child: SizedBox(
          height: responsiveHeight(65, context),
          width: responsiveWidth(65, context),
          child: Container(
            decoration: const BoxDecoration(
                color: Tint.primary,
                boxShadow: [BoxShadow()],
                borderRadius: BorderRadius.all(Radius.circular(5))),
            child: Column(
              children: [
                Padding(
                  padding: EdgeInsets.symmetric(
                      vertical: responsiveHeight(10, context), horizontal: 0.0),
                  child: ResponsiveText(
                    '$_time + $_increment',
                    style: Font.h1,
                  ),
                ),
                ResponsiveText(
                  widget.mode,
                  style: Font.body1,
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
