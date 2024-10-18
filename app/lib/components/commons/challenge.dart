import 'package:auto_mate_chess/components/utils/responsive_text.dart';
import 'package:auto_mate_chess/constants/tint.dart';
import 'package:auto_mate_chess/constants/font.dart';
import 'package:flutter/material.dart';
import '../utils/responsive_utils.dart';

class Challenge extends StatefulWidget {
  final String timeControl;
  final String mode;
  const Challenge({super.key, required this.timeControl, required this.mode});

  @override
  State<Challenge> createState() => _ChallengeState();
}

class _ChallengeState extends State<Challenge> {
  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => print('test'),
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
                    '1 + 0',
                    style: Font.h1,
                  ),
                ),
                ResponsiveText(
                  'Bullet',
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
